import logging

from logger_config import setup_root_logger
from utils import app
from conversation_handling import conversation_flow
from simple_commands import outside_conversation_handler, error


setup_root_logger()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if __name__ == '__main__':
    logger.info("program started")

    app.add_handler(conversation_flow)
    app.add_handler(outside_conversation_handler) # Catches commands outside of conversation flow
    app.add_error_handler(error)

    # Starts program polling
    app.run_polling()