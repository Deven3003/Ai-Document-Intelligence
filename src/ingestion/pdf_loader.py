import os

from pypdf import PdfReader
from src.services.logger import get_logger

logger =get_logger(__name__)

#by strating rag service firstly we will call pdf loader to read the pages from document by passing the file path

def load_pdf(file_path : str):

    try:
        logger.info("Loading PDF: %s",file_path)

        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"PDF file not found :{file_path}"
            )
        
        reader =PdfReader(file_path)

        logger.info("PDF loaded successfully with %d pages",len(reader.pages))
        pages =[]

        for page_number, page in enumerate(reader.pages,start=1):   #pages , metadata are the methods or attributes design by pypdf developers
            text =page.extract_text()

            if text:
                pages.append({"text":text,
                            "page_number":page_number})
        logger.info(
            "Text extraction completed %d pages extracted",len(pages)
        )
        return pages

    except Exception:
        logger.exception("Failed to load or extract PDF:%s",file_path)
        raise