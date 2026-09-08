import faiss
import numpy as np

print("inside FAISS")

Dimensions= 384

def create_index():
    index =faiss.IndexFlatIP(Dimensions)

    return index

Index =create_index()

print("Index is ::",Index)

def add_embeddings(index, embeddings):
    vectors = np.array(embeddings).astype("float32")

    faiss.normalize_L2(vectors)

    index.add(vectors)

    return index

def search_index(index, query_embedding, top_k=3):

    query_vector =np.array([query_embedding]).astype("float32")

    faiss.normalize_L2(query_vector)

    scores , indices =index.search(query_vector, top_k)

    return scores, indices

