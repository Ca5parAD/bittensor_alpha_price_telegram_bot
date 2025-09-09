import logging

from logger_config import setup_root_logger
from simple_commands import outside_conversation_handler, error
from conversation_handling import conversation_flow
from utils import app


setup_root_logger()
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info("program started")

    app.add_handler(conversation_flow)
    app.add_handler(outside_conversation_handler) # Catches commands outside of conversation flow
    app.add_error_handler(error)

    logger.info('polling...')
    app.run_polling()

