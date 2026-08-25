from fastapi import FastAPI
from src.config import settings
from src.services.logger import get_logger

logger =get_logger(__name__)

app =FastAPI (
    title=settings.APP_NAME,
    description="Enterprise knowledge and Document Intelligence platform",
    version=settings.APP_VERSION

)

@app.on_event("startup")
def startup_event():
    logger.info(
        "Startingn %s in %s enviroment",
        settings.APP_NAME,settings.APP_ENV
    )


@app.get("/health")
def health_check():
    logger.info("Health check requested !!!")
    return{
        "status":"healthy",
        "service":settings.APP_NAME,
        "enviroment":settings.APP_ENV
    }