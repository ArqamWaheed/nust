# Experiment 7: build a realistic sensor log of about TARGET_KB kilobytes
import random
import sys
from datetime import datetime, timedelta

FILE_NAME = sys.argv[2] if len(sys.argv) > 2 else "sensor_log.txt"
TARGET_KB = int(sys.argv[1]) if len(sys.argv) > 1 else 300
LOCATIONS = ["Library", "CS-Block", "Cafeteria", "Hostel-A", "Admin-Block"]

random.seed(553514)                   # same file every run, so hashes are reproducible
reading_time = datetime(2026, 9, 23, 8, 0, 0)
size = 0

with open(FILE_NAME, "w", newline="\n") as f:
    header = "timestamp,location,temperature_C,humidity_pct,air_quality_AQI\n"
    f.write(header)
    size += len(header)

    while size < TARGET_KB * 1024:
        line = "{},{},{:.1f},{:.1f},{}\n".format(
            reading_time.strftime("%Y-%m-%d %H:%M:%S"),
            random.choice(LOCATIONS),
            random.uniform(18.0, 38.0),      # temperature
            random.uniform(25.0, 80.0),      # humidity
            random.randint(30, 180))         # air quality index
        f.write(line)
        size += len(line)
        reading_time += timedelta(seconds=5)

print("Created", FILE_NAME, "with", size, "bytes (", round(size / 1024, 1), "KB )")
