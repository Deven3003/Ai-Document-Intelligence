import os

from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME:str =os.getenv(
        "APP_NAME",
        "AI Document Intelligence API"
    )

    APP_VERSION:str =os.getenv(
        "APP_VERSION",
        "0.1.0"
    )

    APP_ENV:str =os.getenv(
        "APP_ENV",
        "development"
    )

    LOG_LEVEL:str =os.getenv(
        "LOG_LEVEL",
        "INFO"
    )

    VETOR_STORE_PATH: str =os.getenv(
        "VETOR_STORE_PATH",
        "data/vector_store"
    )

    DOCUMENTS_PATH: str =os.getenv(
        "DOUMENTS_PATH",
        "data/documents"
    )

    GROQ_API_KEY: str =os.getenv(
        "GROQ_API_KEY",
        ""
    )

    GROQ_MODEL: str =os.getenv(
        "GROQ_MODEL",
        "openai/gpt-oss-20b"
    )

    POSTGRES_HOST: str =os.getenv("POSTGRES_HOST","localhost")
    POSTGRES_PORT: int =int(os.getenv("POSTGRES_PORT","5432"))
    POSTGRES_DB: str = os.getenv("POSTGRES_DB","ai_document_intelligence")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER","postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD","Devpingale@123")
    
settings =Settings()