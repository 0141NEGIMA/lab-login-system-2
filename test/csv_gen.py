import csv

csv_file = "test/test.csv"

with open(csv_file, "w", encoding="utf-8") as f:
    writer = csv.writer(f)
    header_row = ["week"]
    for hh in range(24):
        for mm in range(0, 60, 10):
            header_row.append(f"{hh:02}:{mm:02}")
    writer.writerow(header_row)
    
    day_order = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    empty_row = [""] + [0 for _ in range(6*24)]

    for i, day in enumerate(day_order):
        current_day_row = [day] + [1 if (i+1)*6 <= slot < (i+2)*6 else 0 for slot in range(6*24)]
        writer.writerow(current_day_row)
        #writer.writerow(empty_row)
    

with open(csv_file, "r") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row[0], len(row))