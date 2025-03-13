import re
import mysql.connector
import util.notion as notion

# ユーザ名とMACアドレスの入力
user_name = input("Enter your name: ")
while True:
    mac_address_format = r'^([0-9a-f]{2}[:-]){5}([0-9a-f]{2})$'
    mac_address = input("Enter the MAC address of your bluetooth device: ")
    if re.match(mac_address_format, mac_address.lower()):
        break
    else:
        print("Bad MAC address. (example: 12:34:56:78:9a:bc)")

print(f"Registering {user_name}...")

# notionに登録
new_id = notion.create_member(user_name)

# MySQLに接続
conn = mysql.connector.connect(
    host="localhost",
    user="sqladmin",
    password="sqladmin",
    database="lab_login_system_2"
)
cursor = conn.cursor()

# データの挿入
insert_query = f"INSERT INTO member (name, macaddr, notionid) VALUES ('{user_name}', '{mac_address}', '{new_id}')"
cursor.execute(insert_query)
conn.commit()

# MySQLとの接続を閉じる
cursor.close()
conn.close()

print(f"{user_name} was successfully registered in the DB!")