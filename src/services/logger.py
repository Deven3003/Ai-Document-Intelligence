import logging

from src.config import settings

def get_logger(name:str) -> logging.Logger:
    logger =logging.getLogger(name)

    if not logger.handlers:
        logging.basicConfig(
            level=getattr(logging,settings.LOG_LEVEL),
            format=(
                "%(asctime)s | "
                "%(levelname)s | "
                "%(name)s |"
                "%(message)s "
            )
        )

    return logger