#pdf loader is responsible for make text from pdf
#and our chunker will create chunks from text

#in rag service we will call chunker after the pdf loader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.services.logger import get_logger

logger =get_logger(__name__)

print("$$$$$$$$$ inside chunker $$$$$$$$$$$$$")
def create_chunks(pages : list,document_name :str,source:str):
    try:
        logger.info("Starting document chunking :%s",document_name)
        logger.info("Recived %d pages for chunking ",len(pages))
        splitter =RecursiveCharacterTextSplitter(
            chunk_size =500,
            chunk_overlap=50
        )

        chunks =[]
        for page in pages:    #this first loop gets pdf page 
            page_chunker = splitter.split_text(page["text"])
            #print("\n############### Page Chunker ############### ")
            #print(page_chunker)

            for chunk in page_chunker: #this loop gets each chunk created from that page
                #print("\n chunk taken in for loop")
                #print(chunk)
                chunks.append({
                    "text": chunk,
                    "metadata": {
                        "document_name" :document_name,
                        "source":source,
                        "page_number" :page["page_number"]
                    }
                })

        logger.info("Document chunking completed... no of chunk created are :%d",len(chunks))
        return chunks

    except Exception:
        logger.exception("Failed to start chunking..")
        raise
