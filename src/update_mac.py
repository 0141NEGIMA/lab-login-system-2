import re
import util.sqlite as sq

while True:
    member_name = input("Enter the member_name to update: ")

    if sq.exists_member(member_name):
        mac_addr_format = r'^([0-9a-f]{2}[:-]){5}([0-9a-f]{2})$'
        while True:
            new_mac_addr = input(f"Enter the new_mac_addr of '{member_name}': ")
            if re.match(mac_addr_format, new_mac_addr.lower()):
                break
            else:
                print("Bad MAC address. (example: 12:34:56:78:9a:bc)")
        sq.update_mac(member_name, new_mac_addr)
        exit()
    else:
        print(f"'{member_name}' is not in DB. Try again.")