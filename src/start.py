import logging

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from messages import START_MESSAGE


logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("start command")
    await update.message.reply_text(START_MESSAGE)

start_handler = CommandHandler('start', start_command)