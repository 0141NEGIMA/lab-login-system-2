import bluetooth

def check_bluetooth_device(address):
    try:
        services = bluetooth.find_service(address=address)
        if services:
            print(f"{address} has been found.")
            return 1
        else:
            print(f"{address} has not been found.")
            return 0
    except Exception as e:
        print(f"Error: {e}")
        return -1

address = "98:50:2e:b9:80:ec"
print(check_bluetooth_device(address))