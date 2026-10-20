"""Experiment 10: run both clients three times each and print the table.

    python3 benchmark.py sensor_log.txt [--runs 3]

Both servers must already be running with every test switch turned off.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

PATTERN = re.compile(r"Elapsed time\s*:\s*([0-9.]+)")


def one_run(command: list[str]) -> float | None:
    script = str(Path(__file__).with_name(command[0]))        # the clients live next to this file
    out = subprocess.run([sys.executable, script, *command[1:]], capture_output=True, text=True).stdout
    found = PATTERN.search(out)
    if not found:
        print("  run failed:", out.strip().splitlines()[-1] if out.strip() else "no output")
        return None
    return float(found.group(1))


def main(filename: str, runs: int) -> None:
    size = Path("server_files", filename).stat().st_size
    rows = []
    for label, client in (("TCP", "tcp_file_client.py"), ("UDP", "udp_file_client.py")):
        times = [t for _ in range(runs) if (t := one_run([client, filename])) is not None]
        average = sum(times) / len(times)
        rows.append((label, times, average, (size / 1024) / average))
        print(f"{label}: " + ", ".join(f"{t:.4f} s" for t in times))

    width = 11
    print(f"\nFile: {filename}  ({size} bytes, {size / 1024:.1f} KB)\n")
    header = ["Protocol"] + [f"Run {i}" for i in range(1, runs + 1)] + ["Average", "Throughput"]
    print("".join(h.ljust(width) for h in header))
    print("-" * (width * len(header)))
    for label, times, average, rate in rows:
        cells = [label] + [f"{t:.4f}" for t in times] + [f"{average:.4f}", f"{rate:.0f} KB/s"]
        print("".join(c.ljust(width) for c in cells))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("filename", nargs="?", default="sensor_log.txt")
    ap.add_argument("--runs", type=int, default=3)
    main(*vars(ap.parse_args()).values())
