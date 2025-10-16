'''
Module is not necessary for normal operation and is used only for debugging purposes
As such there is not prompting to user for these commands and lack the typical logging format
'''
import logging

from telegram import Update
from telegram.ext import ContextTypes

from notification_handling import set_notifications


logger = logging.getLogger(__name__)


# Quick command to test notifications
async def test_notifications(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("testing notifications")
    context.user_data['send_notifications'] = True
    context.user_data['notification_subnets'] = [3, 56, 64]
    context.user_data['notification_frequency'] = 0.015
    await set_notifications(update.effective_user.id, context.user_data)

# Prints user_data object to std out
async def test_user_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("testing user data")
    print(context.user_data)
    await update.message.reply_text("done")