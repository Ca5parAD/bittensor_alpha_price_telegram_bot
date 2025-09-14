import logging

from telegram import Update
from telegram.ext import ContextTypes

from notification_handling import set_notifications

logger = logging.getLogger(__name__)

async def test_notifications(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("testing notifications")
    context.user_data['send_notifications_flag'] = True
    context.user_data['notification_netuids'] = [3, 56, 64]
    context.user_data['notification_frequency'] = 1
    set_notifications(update, context)

async def test_user_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("testing user data")
    print(context.user_data)
    await update.message.reply_text("done")
