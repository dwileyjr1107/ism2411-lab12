# ISM2411 Lab 12 
# Name: Tony Wiley

# Reflection 1:
# Doing this in Excel would mean opening the file, adding a total column,
# filtering, and saving a copy by hand every time. Python can repeat the whole
# job in one second on any number of files, and it never forgets a step.
# Excel is still easier when I just want to look at the data or make a quick chart.

# Reflection 2:
# A store could keep a daily sales log where each night a script adds that
# day's total revenue to the end of a file. Append mode is right because it
# adds a new line without erasing the old ones, so you build up a full history
# you can look back on.

import csv
from datetime import datetime

SALES_FILE = "data/sales.csv"
CLEANED_FILE = "data/cleaned.csv"
LOG_FILE = "data/run_log.txt"


# Exercise 1: 
print("=== Exercise 1: Check the file ===")
with open(SALES_FILE, "r") as f:
    print(f"Opened {SALES_FILE} with no errors.")


#  Exercise 2: 
print("\n=== Exercise 2: Raw rows ===")
with open(SALES_FILE, "r") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)  # every value is a string


#  Exercise 3: Skip the header
print("\n=== Exercise 3: Skip the header ===")
with open(SALES_FILE, "r") as f:
    reader = csv.reader(f)
    header = next(reader)
    print("Header:", header)
    for row in reader:
        print(row)


# Exercise 4: 
print("\n=== Exercise 4: Totals ===")
total_revenue = 0
with open(SALES_FILE, "r") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        product = row[0]
        price = float(row[1])
        qty = int(row[2])
        line_total = price * qty
        total_revenue += line_total
        print(f"{product}: {qty} units × ${price:.2f} = ${line_total:.2f}")
print(f"Total revenue: ${total_revenue:.2f}")


#  Exercise 5: 
print("\n=== Exercise 5: Filter and write ===")
original_count = 0
written_count = 0
with open(SALES_FILE, "r") as infile, open(CLEANED_FILE, "w", newline="") as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    next(reader)
    writer.writerow(["Product", "Price", "Qty", "Total"])
    for row in reader:
        original_count += 1
        price = float(row[1])
        qty = int(row[2])
        line_total = price * qty
        if line_total > 100:
            writer.writerow([row[0], f"{price:.2f}", qty, f"{line_total:.2f}"])
            written_count += 1
print(f"Wrote {written_count} of {original_count} rows to {CLEANED_FILE}")


# Exercise 6: 
print("\n=== Exercise 6: DictReader ===")
# csv.reader is fine for small files when you know the column order.
# DictReader is better when columns might move or there are many, since you use names not numbers.
dict_total = 0
with open(SALES_FILE, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        price = float(row["price"])
        qty = int(row["quantity"])
        line_total = price * qty
        dict_total += line_total
        print(f"{row['product']}: {qty} units × ${price:.2f} = ${line_total:.2f}")
print(f"Total revenue: ${dict_total:.2f}")
print("Matches Exercise 4:", round(dict_total, 2) == round(total_revenue, 2))


# Exercise 7
print("\n=== Exercise 7: Summary by product ===")
summary = {}
with open(SALES_FILE, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row["product"]
        line_total = float(row["price"]) * int(row["quantity"])
        summary[name] = summary.get(name, 0) + line_total
for name in sorted(summary):
    print(f"{name}: ${summary[name]:.2f}")


#  Exercise 8: 
print("\n=== Exercise 8: Append to log ===")
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open(LOG_FILE, "a") as log:
    log.write(f"{now} - Total revenue: ${total_revenue:.2f}\n")
print(f"Added a line to {LOG_FILE}")