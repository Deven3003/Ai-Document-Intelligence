import logging
import os
from src.config import settings
from logging.handlers import TimedRotatingFileHandler

LOG_DIRETORY ="logs"

os.makedirs(LOG_DIRETORY, exist_ok=True)



def get_logger(name:str) -> logging.Logger:
    root_logger =logging.getLogger()

    if not root_logger.handlers:
        log_format=(
                "%(asctime)s | "
                "%(levelname)s | "
                "%(name)s |"
                "%(message)s "
        )
        

        formatter =logging.Formatter(log_format)

        #console logging
        console_handler =logging.StreamHandler()
        console_handler.setFormatter(formatter)

        #file logging
        file_handler =TimedRotatingFileHandler(
            filename=os.path.join(LOG_DIRETORY,"app.log"),
            when="midnight",
            interval=1,
            backupCount=30,
            encoding="utf-8"
        )

        file_handler.setFormatter(formatter)


        root_logger.setLevel(
            getattr(
                logging,
                settings.LOG_LEVEL.upper(),
                logging.INFO
            )
        )

        root_logger.addHandler(console_handler)
        root_logger.addHandler(file_handler)


    return logging.getLogger(name)
