import re
import util.notion as nt
import util.sqlite as sql

# メンバー名とMACアドレスの入力
member_name = input("Enter your name: ")
while True:
    mac_address_format = r'^([0-9a-f]{2}[:-]){5}([0-9a-f]{2})$'
    mac_address = input("Enter the MAC address of your bluetooth device: ")
    if re.match(mac_address_format, mac_address.lower()):
        break
    else:
        print("Bad MAC address. (example: 12:34:56:78:9a:bc)")
slack_id = input("Enter your slack id: ")

print(f"Registering {member_name}...")

# notionに登録
notion_id = nt.create_member(member_name)

# SQLiteに登録
sql.register_member(member_name, mac_address, notion_id, slack_id)

print(f"{member_name} was successfully registered in the DB!")