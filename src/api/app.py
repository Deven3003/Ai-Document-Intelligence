from fastapi import FastAPI,HTTPException
from src.config import settings
from src.services.logger import get_logger
from src.rag_service import initialize_rag,ask_question
from src.repositories.conversation_repository import create_conversation,get_message,save_message
from pydantic import BaseModel,Field

logger =get_logger(__name__)

app =FastAPI (
    title=settings.APP_NAME,
    description="Enterprise knowledge and Document Intelligence platform",
    version=settings.APP_VERSION

)

class Source(BaseModel):
    document_name :str
    source:str
    page_number:int
    score:float

class ConversationMessage(BaseModel):
    role:str
    content:str

class QuestionResponse(BaseModel):
    answer: str
    sources: list[Source]

class QuestionRequest(BaseModel):
    conversation_id: int
    question :str =Field(...,min_length=1)
    #conversation_history:list[ConversationMessage] =Field(default_factory=list) /*commented*/

@app.on_event("startup")
def startup_event():
    logger.info(
        "Startingn %s in %s enviroment",
        settings.APP_NAME,settings.APP_ENV
    )
    initialize_rag()


@app.get("/health")
def health_check():
    logger.info("Health check requested !!!")
    return{
        "status":"healthy",
        "service":settings.APP_NAME,
        "enviroment":settings.APP_ENV
    }

@app.post("/ask",response_model=QuestionResponse)
def ask(request : QuestionRequest):
    logger.info(
        "Question Recived : %s:",
        request.question
    )

    try:
        conversation_history =get_message(
            request.conversation_id
        )
        result = ask_question(
            request.question,
            conversation_history)

        logger.info("Question Processed Successfully....")

        #save users question
        save_message(
            request.conversation_id,
            "user",
            request.question
        )

        #Save AI answer
        save_message(
            request.conversation_id,
            "assistant",
            result["answer"]
        )


        return result
    except:
        logger.exception("Error whille processing question")

        raise HTTPException(
            status_code=500,
            detail="An Interal server error occured while processing question "
        )

@app.post("/conversations")
def create_new_conversation():
    try:
        conversation_id =create_conversation(
            user_id=1,
            title='New Conversation'
        )

        logger.info(
            "conversation created successfully:%d",conversation_id
        )

        return{
            "conversation_id":conversation_id
        }

    except Exception:
        logger.exception("Failed to create conversation")
        raise HTTPException(
            status_code=500,
            detail="failed to create conversation"
        )