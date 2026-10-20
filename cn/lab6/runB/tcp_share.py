"""Experiment 5 (and 6): share one file over TCP, port 5002.

    python3 tcp_share.py server [--lan]          # --lan binds 0.0.0.0
    python3 tcp_share.py client [--host IP]

The transfer ends when the server closes the connection, which is exactly the
weakness Experiment 8 fixes with a size header.
"""
import argparse
import socket
from pathlib import Path

PORT = 5002
SOURCE = Path("share_me.txt")
TARGET = Path("received_share_me.txt")
CHUNK = 1024


def serve(host: str) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((host, PORT))
        listener.listen(1)
        print(f"[server] sharing {SOURCE} ({SOURCE.stat().st_size} bytes) on {host}:{PORT}")
        conn, peer = listener.accept()
        with conn, SOURCE.open("rb") as f:
            print(f"[server] connected by {peer[0]}:{peer[1]}")
            sent = 0
            while chunk := f.read(CHUNK):            # walrus: stops on b""
                conn.sendall(chunk)
                sent += len(chunk)
        print(f"[server] file sent, {sent} bytes in {-(-sent // CHUNK)} chunks")


def fetch(host: str) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((host, PORT))
        print(f"[client] connected to {host}:{PORT}")
        received = 0
        calls = 0
        with TARGET.open("wb") as f:
            while data := client.recv(CHUNK):        # b"" = server closed
                f.write(data)
                received += len(data)
                calls += 1
    print(f"[client] saved {TARGET} - {received} bytes from {calls} recv() calls")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("role", choices=["server", "client"])
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--lan", action="store_true", help="server: listen on every interface")
    args = ap.parse_args()
    if args.role == "server":
        serve("0.0.0.0" if args.lan else args.host)
    else:
        fetch(args.host)
