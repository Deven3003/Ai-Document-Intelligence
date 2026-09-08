import os

from src.config import settings
from src.ingestion.pdf_loader import load_pdf
from src.ingestion.chunker import create_chunks
from src.embeddings.embeddings_service import create_embeddings
from src.retrieval.vector_store import create_index, add_embeddings
from src.generation.prompt_builder import build_prompt
from src.generation.llm_service import generate_answer
from src.retrieval.retriever import retrieve_chunks

print("inside RAG Service")
#we are creating this variables so that we can hide our chunks and index from FAST API
global rag_index,rag_chunks
#Rag Knowledge base
rag_index = None
rag_chunks = None

def initialize_rag():
    #we are creating this variables so that we can hide our chunks and index from FAST API
    global rag_index,rag_chunks

    #we have to do first part in RAG Ingestion
    print("****inside initialize RAG****")

    file_path =os.path.join(
        settings.DOCUMENTS_PATH,
        "corporate",
        "employee-handbook.pdf"
    )

    pages =load_pdf(file_path)

    chunks =create_chunks(pages,
                         "Employee Handbook",
                         "employee-handbook.pdf"
                         )

    #create embeddings

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

    print("RAG Pipeline Initialized.")
    print("pages:",len(pages))
    print("chunks:",len(chunks))
    print("Vector:",index.ntotal)


def ask_question(question,top_k=5):
    if rag_index is None or rag_chunks is None:
        raise RuntimeError(
            "Rag service is not initialized.."
            "call initialize_rag() first."
        )    

    retrieved_chunks =retrieve_chunks(
        rag_index,
        rag_chunks,
        question,
        top_k=top_k
    )

    # Build prompt

    prompt =build_prompt(
        question,
        retrieved_chunks
    )

    #3 Genrate answer
    answer =generate_answer(prompt)

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