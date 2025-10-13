import logging
from typing import Dict

from telegram.ext import ContextTypes, Job

from notification_handling import notification_jobs
from data_persistance import search_database_for_user, update_database_user_settings


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Populates and sets users notification setings to default
async def setup_settings(user_id: int, user_data: Dict) -> None:
    # Search database for user, if exists get settings
    database_user_data = await search_database_for_user(user_id)

    if database_user_data:
        # shouldnt be needed, nothing in there yet: user_data.clear()  # Clear existing data
        user_data.update(database_user_data)  # Update with database values
        logger.info(f"user_id:{user_id} - settings found from database")

    else:
        user_data['send_notifications_flag'] = False
        user_data['notification_subnets'] = []
        user_data['notification_frequency'] = 24

        await update_database_user_settings(user_id, user_data)

        logger.info(f"user_id:{user_id} - settings set to default")