import os
from datetime import datetime

LOG_DIR = "log/"

def write_error_log(content):
    error_log_file = os.path.join(LOG_DIR, "error.log")
    with open(error_log_file, "a", encoding="utf-8") as f:
        f.write(f"ERROR[{datetime.now()}]:\n{content}\n\n")

def write_info_log(content):
    info_log_file = os.path.join(LOG_DIR, "info.log")
    with open(info_log_file, "a", encoding="utf-8") as f:
        f.write(f"INFO[{datetime.now()}]: {content}\n")

def print_info_log(content):
    print(f"INFO[{datetime.now()}]: {content}")