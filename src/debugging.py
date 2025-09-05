import logging

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from notification_handling import set_notifications

logger = logging.getLogger(__name__)

async def test_notifications(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("testing notifications")
    context.user_data['send_notifications_flag'] = True
    context.user_data['notification_subnets'] = [3, 56, 64]
    context.user_data['notification_frequency'] = 1
    set_notifications(update, context)