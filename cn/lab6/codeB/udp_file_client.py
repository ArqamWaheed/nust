"""Experiment 9 + optional challenge: UDP file client that repairs losses.

    python3 udp_file_client.py sensor_log.txt [--host IP] [--no-repair]

Chunks go into a pre-sized list instead of a dictionary, so reassembly is just
b"".join(parts).  After the 2 s silence timeout the client sends one RESEND
message listing every gap and waits again - up to REPAIR_ROUNDS times.
"""
import argparse
import hashlib
import socket
import struct
import sys
import time
from pathlib import Path

PORT = 6001
TIMEOUT = 2.0
MAX_TRIES = 3
REPAIR_ROUNDS = 3
HEADER = struct.Struct("!I")


def collect(sock: socket.socket, parts: list, expected: int) -> tuple[int, int]:
    """Receive datagrams until `expected` chunks are held or the socket goes quiet."""
    duplicates = unexpected = 0
    have = sum(piece is not None for piece in parts)
    try:
        while have < expected:
            packet, _ = sock.recvfrom(HEADER.size + 65535)
            if len(packet) < HEADER.size:
                unexpected += 1
                continue
            (seq,) = HEADER.unpack_from(packet)
            if seq >= expected:
                unexpected += 1                      # outside the valid range
            elif parts[seq] is not None:
                duplicates += 1                      # already have this one
            else:
                parts[seq] = packet[HEADER.size:]
                have += 1
    except socket.timeout:
        pass
    return duplicates, unexpected


def download(filename: str, host: str, repair: bool) -> int:
    save_as = Path("received_udp_" + filename.replace("/", "_").replace("\\", "_"))
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
        client.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 4 * 1024 * 1024)
        client.settimeout(TIMEOUT)
        start = time.perf_counter()

        reply = None
        for attempt in range(1, MAX_TRIES + 1):
            client.sendto(f"GET {filename}".encode(), (host, PORT))
            try:
                reply, _ = client.recvfrom(2048)
                break
            except socket.timeout:
                print(f"No reply (attempt {attempt} of {MAX_TRIES})")
        if reply is None:
            print("Transfer failed: server did not respond")
            return 1

        status, *rest = reply.decode(errors="replace").split()
        if status != "OK":
            print("Server error:", " ".join(rest))
            return 1
        size, total, expected_hash = int(rest[0]), int(rest[1]), rest[2]

        parts: list[bytes | None] = [None] * total
        duplicates, unexpected = collect(client, parts, total)

        rounds = 0
        while repair and rounds < REPAIR_ROUNDS:
            missing = [n for n, piece in enumerate(parts) if piece is None]
            if not missing:
                break
            rounds += 1
            print(f"Missing after round {rounds - 1}: {missing[:20]} - asking the server to resend")
            client.sendto(("RESEND " + ",".join(map(str, missing[:200]))).encode(), (host, PORT))
            more_dup, more_unexpected = collect(client, parts, total)
            duplicates += more_dup
            unexpected += more_unexpected

        elapsed = time.perf_counter() - start

    missing = [n for n, piece in enumerate(parts) if piece is None]
    if missing:
        print("Transfer incomplete. Missing chunks:", missing[:20])
        print(f"Received {total - len(missing)} of {total} chunks")
        return 1

    data = b"".join(parts)
    save_as.write_bytes(data)
    actual = hashlib.sha256(data).hexdigest()

    print(f"Protocol          : UDP")
    print(f"Filename          : {filename}")
    print(f"Saved as          : {save_as}")
    print(f"Bytes received    : {len(data)} of {size}")
    print(f"Chunks            : {total}")
    print(f"Duplicates ignored: {duplicates}")
    print(f"Unexpected packets: {unexpected}")
    print(f"Repair rounds     : {rounds}")
    print(f"Elapsed time      : {elapsed:.4f} s")
    print(f"Throughput        : {(len(data) / 1024) / elapsed:.2f} KB/s")
    print(f"File integrity    : {'MATCH' if actual == expected_hash else 'MISMATCH'}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("filename")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--no-repair", action="store_true", help="do not ask for missing chunks")
    args = ap.parse_args()
    sys.exit(download(args.filename, args.host, repair=not args.no_repair))
