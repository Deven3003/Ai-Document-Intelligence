from src.embeddings.embeddings_service import create_embeddings
from src.retrieval.vector_store import search_index
from src.services.logger import get_logger

logger =get_logger(__name__)

MIN_SIMILARITY_SCORE = 0.40

def retrieve_chunks(index, chunks, question, top_k=5):
    try:
        logger.info("Starting retrival for question")
        #chunks =list of all our  chunks
        #question =our question
        #index = index object
        query_embedding =create_embeddings(question)

        scores, indices = search_index(index,
                                       query_embedding,
                                       top_k=top_k)

        results =[]

        rejected_count = 0

        for score, index_number in zip(scores[0],indices[0]):  #we have taken score[0] and indices[0] beacuse faiss returns two dimensional array scores[[0.91,0.88,0.87]] i.e we are taking from 0th index so we are using scores[0] 
            #scores =[[0.98,0.88,0.78]]
            #indices =[[17,43,2,4]]

            #zip combine them in pairs (0.98,17)
            #                           (0.88,43)......and so on

        
            #now loop takes one pair at one time
            #take each (score,index) pair and put the first value into score and the second value into the
            #index_number
            if score < MIN_SIMILARITY_SCORE:
                rejected_count += 1
                continue

            chunk =chunks[index_number]

            results.append({
                "text":chunk["text"],
                "metadata":chunk["metadata"],
                "score":float(score)

            })
        logger.info(
            "retrival completed :%d accepted ,%d rejected",len(results),rejected_count
        )
        if results:
            logger.info(
                "TOP retrival score: %.4f",
                results[0]["score"]
            )
        return results

    except Exception:
        logger.exception("Retrieval failed")
        raise