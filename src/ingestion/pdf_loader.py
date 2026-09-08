from pypdf import PdfReader

#by strating rag service firstly we will call pdf loader to read the pages from document by passing the file path
print("@@@@@@@@@@inside pdf loader@@@@@@@@@@@")
def load_pdf(file_path : str):
    reader =PdfReader(file_path)

    pages =[]

    for page_number, page in enumerate(reader.pages,start=1):   #pages , metadata are the methods or attributes design by pypdf developers
        text =page.extract_text()

        pages.append({"text":text,
                     "page_number":page_number})

    return pages