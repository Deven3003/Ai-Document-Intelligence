from src.ingestion.pdf_loader import load_pdf
from src.ingestion.chunker import create_chunks
from src.embeddings.embeddings_service import create_embeddings
from src.retrieval.vector_store import (
    create_index,
    add_embeddings,
    search_index
)

file_path ="data/documents/corporate/employee-handbook.pdf"

pages =load_pdf(file_path)

chunks = create_chunks(
    pages,
    "Employee-Handbook",
    "employee-handbook.pdf"
)

#print("pages",len(pages))
#print("chunks",len(chunks))
#print(type(chunks))
#print(type(chunks[0]))
#print(chunks[0])

embeddings =[]

for chunk in chunks:
    embedding =create_embeddings(chunk["text"])
    embeddings.append(embedding)

print("Embedding created::",len(embeddings))

#create index

index =create_index()

add_embeddings(index,embeddings)

print("vectors store in FAISS",index.ntotal)

question ="what is the employee leave policy ?"

query_embedding = create_embeddings(question)

#search FAISS
scores, indices =search_index(
    index,
    query_embedding,
    top_k=5
)

print("\nTop results")

for rank, (score, index_number) in enumerate(zip(scores[0], indices[0]),start=1):
    chunk =chunks[index_number]

    print(f"----Result {rank}------")
    print("Score",score)
    print("page",chunk["metadata"]["page_number"])
    print("Document",chunk["metadata"]["document_name"])
    print("Text:",chunk["text"][:300])
    print("\n")