"""Experiment 7: write a sensor log of a given size with the csv module.

    python3 make_log.py            # ~300 KB sensor_log.txt
    python3 make_log.py 100 small_log.txt
"""
import csv
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

FIELDS = ["timestamp", "location", "temperature_C", "humidity_pct", "air_quality_AQI"]
LOCATIONS = ("Library", "CS-Block", "Cafeteria", "Hostel-A", "Admin-Block")


def build(path: Path, target_kb: int, seed: int = 553514) -> int:
    rng = random.Random(seed)                     # fixed seed = reproducible hash
    clock = datetime(2026, 9, 23, 8, 0, 0)
    limit = target_kb * 1024

    with path.open("w", newline="\n") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(FIELDS)
        while handle.tell() < limit:
            writer.writerow([clock.strftime("%Y-%m-%d %H:%M:%S"),
                             rng.choice(LOCATIONS),
                             f"{rng.uniform(18.0, 38.0):.1f}",
                             f"{rng.uniform(25.0, 80.0):.1f}",
                             rng.randint(30, 180)])
            clock += timedelta(seconds=5)
    return path.stat().st_size


if __name__ == "__main__":
    kb = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    out = Path(sys.argv[2] if len(sys.argv) > 2 else "sensor_log.txt")
    size = build(out, kb)
    print(f"Created {out} with {size} bytes ({size / 1024:.1f} KB, {size // 1024 + 1} chunks of 1024 B)")
