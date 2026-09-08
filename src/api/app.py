from fastapi import FastAPI
from src.config import settings
from src.services.logger import get_logger
from src.rag_service import initialize_rag,ask_question
from pydantic import BaseModel

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

class QuestionResponse(BaseModel):
    answer: str
    sources: list[Source]

class QuestionRequest(BaseModel):
    question :str

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

    result = ask_question(request.question)

    return result