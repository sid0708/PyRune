# src/modules/logging.py
from loguru import logger

# Configure loguru
logger.add("pyrune.log", rotation="10 MB", level="INFO")

def log_info(message):
    logger.info(message)

def log_error(message):
    logger.error(message)

def log_debug(message):
    logger.debug(message)
