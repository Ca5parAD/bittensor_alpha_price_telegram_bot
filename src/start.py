import logging

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from messages import START_MESSAGE


logger = logging.getLogger(__name__)


async def set_defaults(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['send_notifications_flag'] = False
    context.user_data['notification_subnets'] = []
    context.user_data['notification_frequency'] = 24

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("start command")
    await set_defaults(update, context)
    await update.message.reply_text(START_MESSAGE)

start_handler = CommandHandler('start', start_command)