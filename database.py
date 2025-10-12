import sqlite3




conn = sqlite3.connect('user_data.db')
c = conn.cursor()

c.execute("SELECT * FROM user_settings")

id, enable, subnets_json, fr = c.fetchone()

print(f"id is type {type(id)} and value: {id}")
print(f"id is type {type(enable)} and value: {enable}")
print(f"id is type {type(subnets_json)} and value: {subnets_json}")
print(f"id is type {type(fr)} and value: {fr}")
