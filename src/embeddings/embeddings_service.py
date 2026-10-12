from sentence_transformers import SentenceTransformer
from src.services.logger import get_logger

logger =get_logger(__name__)

MODEL_NAME ="all-MiniLM-L6-v2"

logger.info("Loading Embedding Model...:%s:",MODEL_NAME)

try:
    model = SentenceTransformer(MODEL_NAME)
    logger.info("Embedding Model Loaded Successfully..")
except Exception:
    logger.info("Embedding model failed to load")
    raise

def create_embeddings(text : str):
    try:
        logger.debug("Embedding creation started")
        embeddings =model.encode(text)
        logger.debug("Sucessfully created embeddings :%d:",len(embeddings))
        return embeddings
    except Exception:
        logger.exception("Failed to create embeddings")
        raise