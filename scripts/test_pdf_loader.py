from src.ingestion.pdf_loader import load_pdf

file_path ="data/documents/corporate/employee-handbook.pdf"

pages =load_pdf(file_path)

print("number of pages :", len(pages))

print("\n First Page:")
print(pages[0])