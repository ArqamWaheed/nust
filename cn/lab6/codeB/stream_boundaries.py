"""Experiment 4: TCP keeps byte order but not message boundaries (port 5004).

    python3 stream_boundaries.py            # one recv(1024)
    python3 stream_boundaries.py --split    # three recv(5) calls

The sender runs in a background thread, so one command shows the whole effect
instead of needing two terminals.
"""
import argparse
import socket
import threading
import time

ADDRESS = ("127.0.0.1", 5004)
PIECES = [b"AAAA", b"BBBB", b"CCCC"]


def sender(ready: threading.Event) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind(ADDRESS)
        listener.listen(1)
        ready.set()
        conn, _ = listener.accept()
        with conn:
            for piece in PIECES:
                conn.sendall(piece)             # three separate sendall() calls
                print(f"[sender]   sendall({piece!r})")
            time.sleep(1)                        # hold the connection open


def receiver(split: bool) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect(ADDRESS)
        time.sleep(0.5)                          # let all three sends arrive first
        if split:
            for call in range(1, len(PIECES) + 1):
                data = client.recv(5)            # smaller than one message
                print(f"[receiver] recv(5) call {call}: {data!r}  ({len(data)} bytes)")
        else:
            data = client.recv(1024)             # ONE recv() for three sends
            print(f"[receiver] recv(1024) returned: {data!r}")
            print(f"[receiver] number of bytes: {len(data)}")
            print(f"[receiver] sender made {len(PIECES)} send calls, receiver made 1 recv call")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--split", action="store_true", help="read with recv(5) three times")
    args = ap.parse_args()

    ready = threading.Event()
    thread = threading.Thread(target=sender, args=(ready,), daemon=True)
    thread.start()
    ready.wait(2)
    receiver(args.split)
    thread.join(3)
