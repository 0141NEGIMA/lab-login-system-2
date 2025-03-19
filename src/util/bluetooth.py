import bluetooth
import util.log as log

def check_bluetooth_device(address):
    try:
        services = bluetooth.find_service(address=address)
        if services:
            #print(f"{address} has been found.")
            return 1
        else:
            #print(f"{address} has not been found.")
            return 0
    except Exception as e:
        log.write_error_log(e)
        return -1