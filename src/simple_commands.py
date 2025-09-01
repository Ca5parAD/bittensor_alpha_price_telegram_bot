import logging

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from messages import START_MESSAGE, HELP_MESSAGE
from utils import SELECT_COMMAND


logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("start command")
    await update.message.reply_text(START_MESSAGE)
    return SELECT_COMMAND

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("help command")
    await update.message.reply_text(HELP_MESSAGE)
    return SELECT_COMMAND

async def handle_unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("Unknown message")
    await update.message.reply_text("Sorry, i have no idea what your saying brev\nPlzzzzz try again")
