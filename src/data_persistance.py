import sqlite3
import json
from typing import Union, Dict
import asyncio

from config import DATABASE_FILE
from notification_handling import set_notifications

# TODO add logging to module

def initialise_from_database():
    """Initialise database and restore notification settings for existing users"""
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS user_settings (
                       user_id INT PRIMARY KEY,
                       enable BOOLEAN,
                       subnets TEXT,  -- JSON string of subnet list
                       frequency FLOAT  -- Hours
                       )
                       ''')
        
        # Iterate through existing users and recreate jobs
        cursor.execute('SELECT user_id, enable, subnets, frequency FROM user_settings')
        for row in cursor.fetchall():
            user_id, enable, subnets_json, frequency = row
            subnets = json.loads(subnets_json) if subnets_json else []
            user_data = {
                'send_notifications': enable,
                'notification_subnets': subnets,
                'notification_frequency': frequency
            }

            set_notifications(user_id, user_data)
        conn.commit()


def search_database_for_user(user_id) -> Union[Dict,bool]:
    """Search database for user_id key, if exists returns dict of settings, else returns false"""
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT enable, subnets, frequency FROM user_settings WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        if result:
            enable, subnets_json, frequency = result
            subnets = json.loads(subnets_json) if subnets_json else []
            user_data = {
                'send_notifications': enable,
                'notification_subnets': subnets,
                'notification_frequency': frequency
            }
            conn.commit()
            return user_data
        conn.commit()
        return None  # User not found


def update_database_user_settings(user_id, user_data):
    """Update user settings in database"""
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        subnets_json = json.dumps(user_data['notification_subnets']) # Convert list to JSON string
        cursor.execute(
            '''INSERT OR REPLACE INTO user_settings (user_id, enable, subnets, frequency)
            VALUES (?, ?, ?, ?)''',
            (user_id, user_data['send_notifications'],
            subnets_json, user_data['notification_frequency']))
        conn.commit()