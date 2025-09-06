import logging

from telegram.ext import ConversationHandler

from logger_config import setup_root_logger
from simple_commands import start_command, universal_handlers, unknown_command_handler, unknown_message_handler, error
from conversation_handling import conversation_flow
from utils import app


setup_root_logger()
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info("program started")

    app.add_handler(conversation_flow)
    app.add_handler(ConversationHandler('start', start_command))
    app.add_handler(universal_handlers) # Catches commands outside of conversation flow
    app.add_handler(unknown_command_handler)
    app.add_handler(unknown_message_handler)
    
    app.add_error_handler(error)

    logger.info('polling...')
    app.run_polling()

