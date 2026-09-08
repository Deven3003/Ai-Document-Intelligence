from src.ingestion.chunker import create_chunks
from src.ingestion.pdf_loader import load_pdf
from src.services.logger import get_logger

print("[[[[[[[[inside test chunker]]]]]]]")
file_path ="data/documents/corporate/employee-handbook.pdf"

pages =load_pdf(file_path)


chunks = create_chunks(pages,"Employee-Handbook","employee-handbook.pdf")

print("number of Pages ::",len(pages))
print("NUMBER OF CHUNKS ::",len(chunks))

print("\nFirst chunk:")
print(chunks[0])

print("\nFirst chunk page::")
print(chunks[0]["metadata"]["page_number"])

print("\nDocument Name::")
print(chunks[0]["metadata"]["document_name"])

print("\nSource::")
print(chunks[0]["metadata"]["source"])