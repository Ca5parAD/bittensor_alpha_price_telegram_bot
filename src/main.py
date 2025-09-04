import logging

from telegram import Update
from telegram.ext import ContextTypes, _contexttypes, ConversationHandler, CommandHandler

from logger_config import setup_root_logger
from simple_commands import help_handler, unknown_command_handler, unknown_message_handler, error
from conversation_handling import conversation_flow
from utils import app

setup_root_logger()
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    logger.info("program started")

    app.add_handler(help_handler)
    app.add_handler(conversation_flow)
    app.add_handler(unknown_command_handler)
    app.add_handler(unknown_message_handler)
    
    app.add_error_handler(error)

    logger.info('polling...')
    app.run_polling()

