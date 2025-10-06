import logging

from telegram import Update
from telegram.ext import ContextTypes

from taostats_calls import get_subnets_info_text


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


async def set_notifications(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Clean up previous notification job
    if context.user_data.get('notification_job'):
        context.user_data['notification_job'].schedule_removal()
        del context.user_data['notification_job']
        logger.debug(f"user_id:{update.effective_user.id} - removed notification job")

    # If user enables notifications create new notification job
    if context.user_data['send_notifications_flag']:
        logger.info(f"user_id:{update.effective_user.id} - set notifications")
        interval = context.user_data['notification_frequency']
        interval_s = interval * 60 ** 2

        try:
            # Create repeating notification job
            notification_job = context.job_queue.run_repeating(
                send_notification,
                chat_id=update.effective_message.chat_id,
                interval=interval_s,
                first=interval_s,
                data=context.user_data
            )
        except Exception as e:
            logger.error(
                f"user_id:{update.effective_user.id} - Failed to create notification job: {e}",
                exc_info=True
            )
            await update.message.reply_text("Failed, please try again later")
        else:
            logger.debug(f"user_id:{update.effective_user.id} - notification job created")
            context.user_data['notification_job'] = notification_job # Store job in user data


async def send_notification(context: ContextTypes.DEFAULT_TYPE):
    message = "<b>Alpha Price Update</b> 📈\n" # Start message
    subnets = context.job.data.get('notification_subnets', [])

    if not subnets:
        message += "No subnets selected ❌.\n"
        logger.debug(f"user_id:{context.job.chat_id} - No subnets selected")
    else:
        try:
            subnets_info_text = get_subnets_info_text(subnets)

        except Exception as e:
            logger.error(
                f"user_id:{context.job.chat_id} - API call failed: {e}",
                exc_info=True
            )
            message += "Failed to connect to tao stats 😓\n\n"

        else:
            message += subnets_info_text

    message += "\n ℹ️ /show_commands" # Finish message with show commands prompt
    try:
        await context.bot.send_message(chat_id=context.job.chat_id, text=message, parse_mode="HTML")
    except Exception as e:
        logger.error(f"user_id:{context.job.chat_id} - notifcation failed to send")
    else:
        logger.info(f"user_id:{context.job.chat_id} - notifcation sent")