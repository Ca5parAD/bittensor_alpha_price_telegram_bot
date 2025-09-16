import logging

from telegram import Update
from telegram.ext import ContextTypes

from bittensor_calls import get_netuid_info

logger = logging.getLogger(__name__)


async def set_notifications(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"user_id:{update.message.chat.id} - set notifications")
    if context.user_data.get('notification_job'):
        context.user_data['notification_job'].schedule_removal()
        del context.user_data['notification_job'] # Clean up notification job
        logger.debug(f"chat_id:{update.message.chat.id} - removed notification job")

    if context.user_data['send_notifications_flag']:
        interval = context.user_data['notification_frequency']
        interval_s = interval * 60 ** 2

        try:
            notification_job = context.job_queue.run_repeating(
                send_notification,
                chat_id=update.effective_message.chat_id,
                interval=interval_s,
                first=interval_s,
                data=context.user_data
            )
        except Exception as e:
            logger.error(f"user_id:{update.message.chat.id} - Failed to create notification job: {e}", exc_info=True)
            await update.message.reply_text("Failed, please try again later")
        else:
            logger.debug(f"user_id:{update.message.chat.id} - notification job created")
            context.user_data['notification_job'] = notification_job # Store job in user data


async def send_notification(context: ContextTypes.DEFAULT_TYPE):
    message = "<b>Subnet Price Update</b> 📈\n"
    subnets = context.job.data.get('notification_netuids', [])
    if not subnets:
        message += "No subnets selected 📌.\n"
    else:
        for i, netuid in enumerate(subnets):
            try:
                netuid_name, netuid_price = get_netuid_info(netuid)
                message += f"({netuid}) {netuid_name}: {netuid_price}\n"
            except Exception as e:
                logger.warning(f"failed to retrieve netuid {netuid}: {e}")
                message += f"({netuid}) Error retrieving price ⚠️\n"

    message += "\n ℹ️ /show_commands"
    try:
        await context.bot.send_message(chat_id=context.job.chat_id, text=message, parse_mode="HTML")
    except Exception as e:
        logger.error(f"user_id:{context.chat.id} - notifcation failed to send") # Need to access user id from context
    else:
        logger.info(f"user_id:{context.chat.id} - notifcation sent") # Need to access user id from context

