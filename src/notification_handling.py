import logging
from typing import Dict

from telegram.ext import ContextTypes, Job

from utils import app
from taostats_calls import get_subnets_info_text


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Dict to store user_id and notification job
notification_jobs: Dict[int, Job] = dict()


def set_notifications(user_id: int, user_data: Dict) -> bool:
    """Deletes previous notification job and creates new one"""
    # Delete and cleans up previous notification job
    if user_id in notification_jobs:
        notification_jobs[user_id].schedule_removal()
        del notification_jobs[user_id]
        logger.debug(f"user_id:{user_id} - removed notification job")

    # If user enables notifications, create new notification job
    if user_data['send_notifications']:
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
    """Formats and sends subnet price notification to user"""
    chat_id = context.job.chat_id
    subnets = context.job.data.get('notification_subnets', [])
    message = "<b>Alpha Price Update</b> 📈\n" # Title of message
    if not subnets: # If no subnets have been selected
        message += "No subnets selected ❌.\n"
        logger.debug(f"user_id:{chat_id} - No subnets selected")
    else:
        try: # Creates body of text 
            subnets_info_text = get_subnets_info_text(subnets)
        except Exception as e:
            logger.error(
                f"user_id:{chat_id} - API call failed: {e}",
                exc_info=True
            )
            message += "Failed to connect to tao stats 😓\n\n"
        else:
            message += subnets_info_text

    message += "\n ℹ️ /show_commands" # Finish message with show commands prompt
    try: # Sends message to user
        await context.bot.send_message(chat_id=chat_id, text=message, parse_mode="HTML")
    except Exception as e:
        logger.error(f"user_id:{chat_id} - notifcation failed to send")
    else:
        logger.info(f"user_id:{chat_id} - notifcation sent")