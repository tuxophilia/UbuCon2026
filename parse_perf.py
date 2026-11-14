import os
import re
import csv
import sys

RAW_FILE = "perf_raw.txt"
OUTPUT_FILE = "hpc_data_store.txt"

SPECIAL_COLUMNS = [
    "Elapsed_Time",
    "Time_Diff",
    "Timestamp_Normalized"
]

existing_rows = []
existing_hpcs = []

if os.path.exists(OUTPUT_FILE) and os.path.getsize(OUTPUT_FILE) > 0:
    with open(OUTPUT_FILE, "r") as f:
        reader = csv.reader(f, delimiter="\t")
        try:
            header = next(reader)
        except StopIteration:
            header = []

        if header:
            existing_hpcs = [
                col for col in header
                if col not in (["Timestamp"] + SPECIAL_COLUMNS)
            ]
            for row in reader:
                if row:
                    existing_rows.append(row)

measurements = {}

with open(RAW_FILE, "r", errors="replace") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        match = re.match(
            r"^\s*([0-9]+\.[0-9]+)\s+([0-9,]+|<[^>]+>|not\s+counted|not\s+supported)\s+(\S+)",
            line
        )

        if not match:
            continue

        timestamp = float(match.group(1))
        value_string = match.group(2).strip()
        event_string = match.group(3).strip()

        event_string = event_string.strip("/")
        if "/" in event_string:
            parts = event_string.split("/")
            event = parts[-1]
        else:
            event = event_string

        invalid_values = ["<not supported>", "<not counted>", "not counted", "not supported"]
        if any(x in value_string.lower() for x in invalid_values):
            value = "N/A"
        else:
            value_string = value_string.replace(",", "")
            try:
                value = float(value_string)
            except ValueError:
                value = "N/A"

        if timestamp not in measurements:
            measurements[timestamp] = {}

        if event not in measurements[timestamp]:
            measurements[timestamp][event] = value
        else:
            old_value = measurements[timestamp][event]
            if isinstance(old_value, (int, float)) and isinstance(value, (int, float)):
                measurements[timestamp][event] = old_value + value
            elif value != "N/A":
                measurements[timestamp][event] = value

if not measurements:
    print("ERROR: No perf measurements found.")
    print("\nFirst few lines of raw perf file:")
    if os.path.exists(RAW_FILE):
        with open(RAW_FILE, "r", errors="replace") as f:
            for i, line in enumerate(f):
                print(line.rstrip())
                if i >= 10:
                    break
    sys.exit(1)

current_hpcs = []
for timestamp in sorted(measurements):
    for event in measurements[timestamp]:
        if event not in current_hpcs:
            current_hpcs.append(event)

for hpc in current_hpcs:
    if hpc not in existing_hpcs:
        existing_hpcs.append(hpc)

timestamps = sorted(measurements.keys())
first_timestamp = timestamps[0]

previous_timestamp = None
if existing_rows:
    try:
        previous_timestamp = float(existing_rows[-1][0])
    except Exception:
        previous_timestamp = None

new_rows = []
for timestamp in timestamps:
    data = measurements[timestamp]
    elapsed_time = timestamp - first_timestamp
    time_diff = 0.0 if previous_timestamp is None else timestamp - previous_timestamp
    timestamp_normalized = timestamp - first_timestamp

    row = [timestamp]
    for hpc in existing_hpcs:
        row.append(data.get(hpc, "----"))

    row.extend([elapsed_time, time_diff, timestamp_normalized])
    new_rows.append(row)
    previous_timestamp = timestamp

header = ["Timestamp"] + existing_hpcs + SPECIAL_COLUMNS

with open(OUTPUT_FILE, "w") as f:
    writer = csv.writer(f, delimiter="\t", lineterminator="\n")
    writer.writerow(header)

    for old_row in existing_rows:
        if len(old_row) < len(header):
            diff = len(header) - len(old_row)
            old_row = old_row[:-len(SPECIAL_COLUMNS)] + ["----"] * diff + old_row[-len(SPECIAL_COLUMNS):]
        writer.writerow(old_row)

    for row in new_rows:
        writer.writerow(row)

print("\n========================================")
print("HPC recording processed successfully")
print("========================================")
print("Output file :", OUTPUT_FILE)
print("Measurements :", len(new_rows))
print("\nHPCs found in this run:")
for hpc in current_hpcs:
    print("  ", hpc)
print("\nTotal HPC columns:", len(existing_hpcs))
