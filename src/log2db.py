import re
from datetime import datetime
from util import sqlite as sq

log_path = "log/info.log"

def parser(line):
    pattern = r"INFO\[(.*?)\]: (\w+) has (left|entered) the room."
    match = re.search(pattern, line)
    if match:
        timestamp, name, entered_left = match.groups()
        timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f").strftime("%Y/%m/%d %H:%M:%S")
        enter_leave = "enter" if entered_left == "entered" else "leave"
        return name, enter_leave, timestamp

sq.init()
sq.reset_table("record")
with open(log_path, "r") as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        line = line.strip()
        name, enter_leave, timestamp = parser(line)
        #print(f"name={name} enter_leave={enter_leave} timestamp={timestamp}")
        sq.insert_into_record(name, enter_leave, timestamp)