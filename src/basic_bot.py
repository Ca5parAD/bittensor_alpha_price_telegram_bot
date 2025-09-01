import logging

from telegram import Update
from telegram.ext import ContextTypes, _contexttypes, ConversationHandler, CommandHandler

from logger_config import setup_root_logger
from simple_commands import start_command
from conversation_handling import conversation_flow
from utils import app

setup_root_logger()
logger = logging.getLogger(__name__)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.exception(f"Update caused error: {context.error}")
    # Message to user about error
    # Way to reset conversation flow to user?


if __name__ == '__main__':
    # Test log to verify logging setup
    logger.info("program started")

    app.add_handler(conversation_flow)

    app.add_error_handler(error)

    logger.info('polling...')
    app.run_polling()
