import logging

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from messages import HELP_MESSAGE


logger = logging.getLogger(__name__)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("help command")
    await update.message.reply_text(HELP_MESSAGE)

help_handler = CommandHandler('help', help_command)