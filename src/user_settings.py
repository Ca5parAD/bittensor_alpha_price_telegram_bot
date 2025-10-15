import logging
from typing import Dict

from data_persistance import search_database_for_user, update_database_user_settings


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Populates and sets users notification setings to default
async def setup_settings(user_id: int, user_data: Dict) -> None:
    """Populates user settings from database or to default settings"""
    # Search database for user, if exists returns settings, else returns false
    database_user_data = await search_database_for_user(user_id)

    if database_user_data:
        user_data.update(database_user_data)  # Update with database values
        logger.info(f"user_id:{user_id} - user settings found from database")

    else: # Default user settings
        user_data['send_notifications_flag'] = False
        user_data['notification_subnets'] = []
        user_data['notification_frequency'] = 24

        await update_database_user_settings(user_id, user_data) # Updates database with settings
        logger.info(f"user_id:{user_id} - user settings set to default")