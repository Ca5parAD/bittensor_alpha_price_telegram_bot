import sqlite3

from src.config import DATABASE_FILE

path_to_database = DATABASE_FILE
conn = sqlite3.connect(path_to_database)
c = conn.cursor()

c.execute("SELECT * FROM user_settings")

users = c.fetchall()

for user in users:
    print(user)
