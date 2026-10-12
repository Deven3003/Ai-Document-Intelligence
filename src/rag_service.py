import os

from src.config import settings
from src.ingestion.pdf_loader import load_pdf
from src.ingestion.chunker import create_chunks
from src.embeddings.embeddings_service import create_embeddings
from src.retrieval.vector_store import create_index, add_embeddings
from src.generation.prompt_builder import build_prompt
from src.generation.llm_service import generate_answer
from src.retrieval.retriever import retrieve_chunks
from src.services.logger import get_logger
from src.generation.query_rewritter import rewrite_question
from pathlib import Path


logger =get_logger(__name__)
#we are creating this variables so that we can hide our chunks and index from FAST API
global rag_index,rag_chunks
#Rag Knowledge base
rag_index = None
rag_chunks = None

def initialize_rag():
    try:
        #we are creating this variables so that we can hide our chunks and index from FAST API
        global rag_index,rag_chunks

        #we have to do first part in RAG Ingestion
        logger.info("****inside initialize RAG****")

        # file_path =os.path.join(
        #     settings.DOCUMENTS_PATH,
        #     "corporate",
        #     "employee-handbook.pdf"
        # )

        # pages =load_pdf(file_path)

        # logger.info("page loaded successfully..")

        # chunks =create_chunks(pages,
        #                     "Employee Handbook",
        #                     "employee-handbook.pdf"
        #                     )
        # logger.info("Chunks created sucssesfully..")
        #commented for multi-document ingestion
        #create embeddings
        documents_path =Path(settings.DOCUMENTS_PATH)

        #FIND ALL PDF FILES , INCLUDING IN SUBFOLDERS

        pdf_files = sorted(documents_path.rglob("*.pdf"))

        if not pdf_files:
            raise FileNotFoundError(
                f"No PDF file found in {documents_path}"
            )

        all_chunks =[]

        for pdf_file in pdf_files:
            logger.info("loading document: %s",pdf_file)

            pages =load_pdf(str(pdf_file))

            #Use the PDF filename as its documents name.
            document_name =pdf_file.stem
            source =pdf_file.name

            document_chunks =create_chunks(
                pages,
                document_name,
                source
            )

            all_chunks.extend(document_chunks)
            logger.info("Created $d chunks from %s",len(document_chunks),pdf_file.name)

        chunks =all_chunks

        embeddings =[]

        for chunk in chunks:
            embedding =create_embeddings(chunk["text"])
            embeddings.append(embedding)

        # create FAISS index
        index =create_index()

        rag_index = index
        rag_chunks = chunks

        #store embeddings in FAISS
        add_embeddings(index, embeddings)

        logger.info("RAG Pipeline Initialized.")
        logger.info("pages:%d",len(pages))
        logger.info("chunks:%d",len(chunks))
        logger.info("Vector:%d",index.ntotal)
    
    except Exception:
        logger.exception("failed to Initilized RAG.")


def ask_question(question,conversation_history,top_k=5):
    try:
        if rag_index is None or rag_chunks is None:
            raise RuntimeError(
                "Rag service is not initialized.."
                "call initialize_rag() first."
            )

        rewritten_question=rewrite_question(
            question,
            conversation_history
            )

        logger.info("Question rewritten for retrival:%s:",rewritten_question) 

        retrieved_chunks =retrieve_chunks(
            rag_index,
            rag_chunks,
            rewritten_question,
            top_k=top_k
        )

        print(f"\n==========Retrived chunks==============")
        for i,result in enumerate(retrieved_chunks,start=1):
            print(f"\n++++++chunk{i}+++++++++++")
            print(result["text"])
        print(f"\n=======================================")

        logger.info("Retrived %d chunks for Question",len(retrieved_chunks))



        if not retrieved_chunks:
            logger.warning("No relevant chunk found fot question")
            return {
                "answer":"I could find this information in document and not wasting your GROK Api call",
                "sources":[]
            }

        # Build prompt

        prompt =build_prompt(
            rewritten_question,
            retrieved_chunks
        )

        logger.info("prompt build successfully")
        print("======================prom sent to llm=====================")
        print(prompt)
        print("===========================END=============================")
        #3 Genrate answer
        answer =generate_answer(prompt)
        logger.info("Answer generate successfully")

        #adding source to the file which will give us clear idea from where answer comes from

        sources =[]

        for result in retrieved_chunks:
            metadata = result["metadata"]
            sources.append({
                            "document_name" :metadata["document_name"],
                            "source":metadata["source"], 
                            "page_number":metadata["page_number"],
                            "score": result["score"]
                            })

        return {
            "answer":answer,
            "sources":sources
        }
    except Exception:
        logger.exception("Failed to ASK Question..")
        raise