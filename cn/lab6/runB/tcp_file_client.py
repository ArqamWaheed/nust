"""Experiment 8: TCP file client with an exact-length receive loop.

    python3 tcp_file_client.py sensor_log.txt [--host IP]

recv_into() fills one pre-allocated buffer, so the whole file is received without
joining many small byte objects, and never one byte past the announced size.
"""
import argparse
import hashlib
import socket
import sys
import time
from pathlib import Path

PORT = 6000
BUFFER_SIZE = 4096


def read_line(sock: socket.socket, limit: int = 255) -> str:
    """The reply header is one short line, so read it a byte at a time."""
    line = bytearray()
    while not line.endswith(b"\n"):
        piece = sock.recv(1)
        if not piece:
            raise ConnectionError("Server closed before replying")
        line += piece
        if len(line) > limit:
            raise ValueError("Reply line too long")
    return line.decode().strip()


def download(filename: str, host: str) -> int:
    save_as = Path("received_tcp_" + filename.replace("/", "_").replace("\\", "_"))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.settimeout(10)
        client.connect((host, PORT))
        start = time.perf_counter()
        client.sendall(f"{filename}\n".encode())

        status, *rest = read_line(client).split()
        if status != "OK":
            print("Server error:", " ".join(rest))
            return 1
        size, expected = int(rest[0]), rest[1]

        buffer = bytearray(size)                 # exact room for the file
        view = memoryview(buffer)
        received = 0
        while received < size:
            got = client.recv_into(view[received:received + min(BUFFER_SIZE, size - received)])
            if not got:
                print(f"Transfer failed: Connection closed early: got {received} of {size} bytes")
                return 1
            received += got
        elapsed = time.perf_counter() - start

    save_as.write_bytes(buffer)
    actual = hashlib.sha256(buffer).hexdigest()
    print(f"Protocol       : TCP")
    print(f"Filename       : {filename}")
    print(f"Saved as       : {save_as}")
    print(f"Bytes received : {received} of {size}")
    print(f"Elapsed time   : {elapsed:.4f} s")
    print(f"Throughput     : {(received / 1024) / elapsed:.2f} KB/s")
    print(f"Expected hash  : {expected[:32]}...")
    print(f"File integrity : {'MATCH' if actual == expected else 'MISMATCH'}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("filename")
    ap.add_argument("--host", default="127.0.0.1")
    args = ap.parse_args()
    try:
        sys.exit(download(args.filename, args.host))
    except (ConnectionError, socket.timeout, OSError, ValueError) as error:
        print("Transfer failed:", error)
        sys.exit(1)
