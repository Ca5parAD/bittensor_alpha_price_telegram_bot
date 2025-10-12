import logging
from typing import Dict

from telegram.ext import ContextTypes, Job

from utils import app
from taostats_calls import get_subnets_info_text


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Dict to store user_id and notification job
notification_jobs: Dict[int, Job] = dict()


# Doesnt need update and context as args, change these
# Use user_data instead context, therefore directly accessible and can be replicated from database function
async def set_notifications(user_id: int, user_data: Dict) -> bool:







    # Check this function - issue is the creating and storing notification job
    # i think it creates job fine, its the deleting previous and creating new that is an issue
    # seems odd as its the same as previous method except in dict not context.user_data









    # Clean up previous notification job
    if user_id in notification_jobs:
        notification_jobs[user_id].schedule_removal()
        del notification_jobs[user_id]
        logger.debug(f"user_id:{user_id} - removed notification job")


    # If user enables notifications, create new notification job
    if user_data['send_notifications_flag']:
        logger.info(f"user_id:{user_id} - set notifications")
        interval_hours = user_data['notification_frequency']
        interval_seconds = interval_hours * 60 ** 2

        try:
            # Create repeating notification job
            notification_job = app.job_queue.run_repeating(
                callback = send_notification,
                chat_id = user_id,
                interval = interval_seconds,
                first = interval_seconds,
                data = user_data
            )
        except Exception as e:
            logger.error(
                f"user_id:{user_id} - Failed to create notification job: {e}",
                exc_info=True
            )
            return False
        else:
            logger.debug(f"user_id:{user_id} - notification job created")
            notification_jobs[user_id] = notification_job # Store job in notification_jobs
            return True

























async def send_notification(context: ContextTypes.DEFAULT_TYPE):
    message = "<b>Alpha Price Update</b> 📈\n" # Start message

    # Unsure if a context is being created or need to use data which is being passed?
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