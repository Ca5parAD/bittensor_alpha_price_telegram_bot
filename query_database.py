import sqlite3

from src.config import DATABASE_FILE

conn = sqlite3.connect(DATABASE_FILE)
c = conn.cursor()

c.execute("SELECT * FROM user_settings")
users = c.fetchall()

for user in users:
    print(f"User: {user[0]}")
    print(f"Notifications enabled: {"yes" if user[1] else "no"}")
    print(f"Subnets: {user[2]}")
    print(f"Notification intervals: {user[3]}hrs\n")