from src.embeddings.embeddings_service import create_embeddings
from src.retrieval.vector_store import (create_index,
                                        add_embeddings,
                                        search_index)

documents = [
    "Employee recives anual leave on by work policy",
    "Employees can work remotely by managers approval",
    "company reimburses approved buisness travel expense "
]

embeddings =[]

for document in documents:
    embedding =create_embeddings(document)
    embeddings.append(embedding)

index =create_index()

add_embeddings(index,embeddings)

query ="How many vacation days do employee get ?"

query_embedding =create_embeddings(query)

scores, indices =search_index(
    index,
    query_embedding,
    top_k=2
)

for score, index_number in zip(scores[0],indices[0]):
    print(
        "score:",score,"| Document:",documents[index_number]
    )