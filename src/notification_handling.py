import logging

from telegram import Update
from telegram.ext import Application, ContextTypes

from utils import app
from bittensor_calls import get_netuid_info

logger = logging.getLogger(__name__)


def set_notifications(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("set notification")
    if context.user_data.get('notification_job'):
        context.user_data['notification_job'].schedule_removal()
        del context.user_data['notification_job'] # Clean up notification job

    if context.user_data['send_notifications_flag']:
        interval_s = context.user_data['notification_frequency'] * 5
        notification_job = context.job_queue.run_repeating(
            send_notification,
            chat_id=update.effective_message.chat_id,
            interval=interval_s,
            first=3, # Little delay until first message
            data=context.user_data
        )
        context.user_data['notification_job'] = notification_job # Store job in user data  


async def send_notification(context: ContextTypes.DEFAULT_TYPE):
    logger.info("sending notification")
    logger.debug(f"notification settings: {context.job.data}")
    message = "<b>Subnet Price Update</b> 📈\n\n"

    subnets = context.job.data.get('notification_subnets', [])
    if not subnets:
        message += "No subnets selected 📌.\n"
    else:
        for i, netuid in enumerate(subnets):
            try:
                netuid_name, netuid_price = get_netuid_info(netuid)
                message += f"• ({netuid}) {netuid_name}: {netuid_price}\n"
            except Exception as e:
                logger.warning(f"Error retrieving netuid {netuid}: {e}")
                message += f"• ({netuid}) Error retrieving price ⚠️\n"

    message += "\nAdjust settings: /settings ⚙️\n"
    message += "Return: /back ↩️\n"
    message += "Need help: /help ❓"

    await context.bot.send_message(chat_id=context.job.chat_id, text=message, parse_mode="HTML")

