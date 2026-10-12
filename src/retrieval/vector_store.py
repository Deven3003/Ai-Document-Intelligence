import faiss
import numpy as np
from src.services.logger import get_logger

logger =get_logger(__name__)
logger.info("Entered inside Vector_Store")

Dimensions= 384

def create_index():
    try:
        logger.info("Creating FAISS indes using %d Dimensions",Dimensions)
        index =faiss.IndexFlatIP(Dimensions)
        logger.info("FAISS Index created successfully")
        return index

    except Exception:
        logger.exception("Failed to create FAISS Index")
        raise
        

def add_embeddings(index, embeddings):
    try:
        logger.info("Adding %d Embeddings to FAISS Index",embeddings)
        vectors = np.array(embeddings).astype("float32")

        faiss.normalize_L2(vectors)

        index.add(vectors)
        logger.info("successfully added %d vectors to FAISS index",len(vectors))
        return index

    except Exception:
        logger.exception("Failed to add embeddings to FAISS index")
        raise

def search_index(index, query_embedding, top_k=3):
    try:
        logger.info("Stared searching index using query embeddings")

        query_vector =np.array([query_embedding]).astype("float32")

        faiss.normalize_L2(query_vector)

        scores , indices =index.search(query_vector, top_k)

        logger.info("successfully generated scores and indices inside search index")
        logger.info("FAISS similarity search completed successfully...")
        return scores, indices

    except Exception:
        logger.exception("Failed to search index using query embeddings")
        raise

