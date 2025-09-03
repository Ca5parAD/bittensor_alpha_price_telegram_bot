import logging

from telegram import Update
from telegram.ext import Application, ContextTypes

from utils import app
from bittensor_calls import get_netuid_info

logger = logging.getLogger(__name__)


def set_notifications(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("set notification")
    if context.user_data['send_notifications_flag']:
        interval_s = context.user_data['notification_frequency'] * 5
        context.job_queue.run_repeating(
            send_notification,
            chat_id=update.effective_message.chat_id,
            interval=interval_s,
            first=interval_s,
            data=context.user_data
        )
        


async def send_notification(context: ContextTypes.DEFAULT_TYPE):
    logger.info("sending notification")
    logger.debug(f"notification settings: {context.job.data}")
    message = f"Your subnets:\n"

    for i, netuid in enumerate(context.job.data['notification_subnets']):
        netuid_name, netuid_price = get_netuid_info(netuid)
        message += f"({i}) {netuid_name} -> {netuid_price}\n"


    await context.bot.send_message(chat_id=context.job.chat_id, text=message)

