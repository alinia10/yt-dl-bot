import logging
import os
from datetime import datetime

from jsonformatter import JsonFormatter  # type: ignore

LOGGER_NAME = "dl"


class LoggingLevel:
    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    

def get_logger():
    # Check if 'results' folder exists, if not, create it
    results_folder = "./results"
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)  # Create the folder if it doesn't exist

    # Create a custom logger
    logger = logging.getLogger(LOGGER_NAME)
    if logger.handlers:  # If the logger has handlers, it is already set up
        return logger
    logger.propagate = False  # Disable propagation of log messages to parent loggers
    logger.setLevel(logging.INFO)  # Set default log level to INFO

    # Create file handler to log to a file within 'results' folder
    file_handler = logging.FileHandler(f"{results_folder}/dl.log", encoding="utf8")
    
    # Create stream handler to log to console
    stream_handler = logging.StreamHandler()

    # Set the format of the log messages to JSON format
    formatter = JsonFormatter(
        ensure_ascii=False,  # Allow non-ASCII characters
        mix_extra=True,  # Include extra fields in the log output
        mix_extra_position="head",  # Place extra fields at the beginning
    )

    # Apply formatter to handlers
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger


def simple_logger(message, log_level=LoggingLevel.INFO):
    # Get the logger and log the message
    logger = get_logger()
    logger.log(
        log_level,  # Log message with specified level
        message,  # The actual log message
        extra={  # Include additional information in the log entry
            "logtime": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),  # Include timestamp in the log
        },
    )
