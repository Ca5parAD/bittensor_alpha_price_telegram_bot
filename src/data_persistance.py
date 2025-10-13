import aiosqlite
import json
from typing import Dict, Union

from config import DATABASE_FILE
from notification_handling import set_notifications

# TODO add logging to module

# Create database if does not exist
async def initialise_from_database():
    """Initialize the database and restore notification settings for existing users."""
    async with aiosqlite.connect(DATABASE_FILE) as conn:
        # Create table if it doesn't exist
        await conn.execute('''
                       CREATE TABLE IF NOT EXISTS user_settings (
                       user_id INT PRIMARY KEY,
                       enable BOOLEAN,
                       subnets TEXT,  -- JSON string of subnet list
                       frequency FLOAT  -- Hours
                       )
                       ''')
        await conn.commit()
        
        # Iterate through existing users and recreate jobs
        cursor = await conn.execute('SELECT user_id, enable, subnets, frequency FROM user_settings')
        rows = await cursor.fetchall()
        await cursor.close()
        
        for row in rows:
            user_id, enable, subnets_json, frequency = row
            if enable:  # Only recreate if enabled
                subnets = json.loads(subnets_json) if subnets_json else []
                user_data = {
                    'send_notifications_flag': enable,
                    'notification_subnets': subnets,
                    'notification_frequency': frequency
                }

                await set_notifications(user_id, user_data)



    

async def search_database_for_user(user_id) -> Union[Dict, False]: # Union for Amazon Linux
    """Search database for user_id key, return dict of settings or false if doesn't exist"""

    async with aiosqlite.connect(DATABASE_FILE) as conn:
        cursor = await conn.execute('SELECT enable, subnets, frequency FROM user_settings WHERE user_id = ?', (user_id,))
        result = await cursor.fetchone()
        await cursor.close()
        
        if result:
            enable, subnets_json, frequency = result
            subnets = json.loads(subnets_json) if subnets_json else []
            user_data = {
                'send_notifications_flag': enable,
                'notification_subnets': subnets,
                'notification_frequency': frequency
            }
            await conn.commit()
            return user_data
        await conn.commit()
        return None  # User not found
        


# Update database for user settings
async def update_database_user_settings(user_id, user_data):
    """Write or update user settings in the database."""

    async with aiosqlite.connect(DATABASE_FILE) as conn:
        subnets_json = json.dumps(user_data['notification_subnets']) # Convert list to JSON string
        await conn.execute(
            '''INSERT OR REPLACE INTO user_settings (user_id, enable, subnets, frequency)
            VALUES (?, ?, ?, ?)''',
            (user_id, user_data['send_notifications_flag'],
            subnets_json, user_data['notification_frequency']))
        await conn.commit()



        """
        
        Looks like everything is good now apart from how subnets is being stored, need to check how its
        stored and accessed 
        
        """