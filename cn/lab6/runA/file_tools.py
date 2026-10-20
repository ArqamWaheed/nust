# Experiment 7: SHA-256 fingerprint, timing and throughput
import hashlib
import os
import sys
import time


def file_hash(path):
    """Return the SHA-256 fingerprint of a file."""
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            block = f.read(65536)
            if not block:
                break
            sha.update(block)
    return sha.hexdigest()


if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "sensor_log.txt"
    size_bytes = os.path.getsize(name)

    start = time.perf_counter()
    digest = file_hash(name)
    elapsed = time.perf_counter() - start

    print("File       :", name)
    print("Size       :", size_bytes, "bytes")
    print("SHA-256    :", digest)
    print("Hash time  : {:.6f} s".format(elapsed))
    print("Throughput : {:.2f} KB/s".format((size_bytes / 1024) / elapsed))
