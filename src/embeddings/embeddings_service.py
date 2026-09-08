from sentence_transformers import SentenceTransformer

MODEL_NAME ="all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)

def create_embeddings(text : str):

    embeddings =model.encode(text)

    return embeddings