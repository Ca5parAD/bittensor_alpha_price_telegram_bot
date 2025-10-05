import logging
from logging.handlers import RotatingFileHandler

from config import LOG_FILE_PATH


def setup_root_logger() -> None:
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # Main log file with rotation
    file_handler = RotatingFileHandler(
        LOG_FILE_PATH,
        maxBytes=5*1024*1024, # 5MB
        backupCount=3  # 3 backups
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    ))
    root_logger.addHandler(file_handler)

    # Stream handler for all levels
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter("%(name)s - %(levelname)s - %(message)s"))
    root_logger.addHandler(stream_handler)

    # Explicitly set levels for program modules
    logging.getLogger('simple_commands').setLevel(logging.INFO)

    # Suppress API loggers
    logging.getLogger('httpcore.http11').setLevel(logging.WARNING)
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('telegram.ext').setLevel(logging.WARNING)
    logging.getLogger('apscheduler').setLevel(logging.WARNING)
