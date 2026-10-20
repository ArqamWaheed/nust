"""Experiment 7: SHA-256 fingerprint, elapsed time and throughput.

    python3 integrity.py sensor_log.txt [more files...]
"""
import hashlib
import sys
import time
from pathlib import Path


def digest(path: Path, block: int = 65536) -> str:
    sha = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(block), b""):
            sha.update(chunk)
    return sha.hexdigest()


def throughput(size_bytes: int, seconds: float) -> float:
    """Application-level throughput in KB/s."""
    return (size_bytes / 1024) / seconds


def report(path: Path) -> None:
    size = path.stat().st_size
    start = time.perf_counter()
    fingerprint = digest(path)
    elapsed = time.perf_counter() - start
    print(f"File       : {path}")
    print(f"Size       : {size} bytes ({size / 1024:.1f} KB)")
    print(f"SHA-256    : {fingerprint}")
    print(f"Hash time  : {elapsed:.6f} s")
    print(f"Throughput : {throughput(size, elapsed):.2f} KB/s")


if __name__ == "__main__":
    for name in sys.argv[1:] or ["sensor_log.txt"]:
        report(Path(name))
        print()
