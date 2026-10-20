"""Experiment 9 + optional challenge: file transfer over UDP (port 6001).

    python3 udp_file_server.py [--lan] [--dup] [--drop 7]

Datagrams:
    client -> GET <filename>              request
    server -> OK <size> <chunks> <sha>    or  ERROR <reason>
    server -> 4-byte seq + up to 1024 B   data
    client -> RESEND 7,19,204             ask for the chunks that never arrived
    server -> the same data datagrams again

The RESEND message is the optional challenge from the manual: the server keeps
the file it last served to each client, so it can repair losses on request.
"""
import argparse
import hashlib
import socket
import struct
import time
from pathlib import Path

PORT = 6001
FILES_FOLDER = Path("server_files")
CHUNK_SIZE = 1024
PACE_EVERY = 50                     # 1 ms pause after this many datagrams
HEADER = struct.Struct("!I")        # one unsigned 32-bit sequence number


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load(name: str) -> bytes | str:
    """Return the file contents, or an ERROR string explaining the refusal."""
    if not name or name != Path(name).name or ".." in name:
        return "ERROR Invalid filename"
    path = FILES_FOLDER / name
    if not path.is_file():
        return "ERROR File not found"
    return path.read_bytes()


def send_chunks(sock: socket.socket, peer, data: bytes, order: list[int]) -> int:
    for count, seq in enumerate(order, start=1):
        payload = data[seq * CHUNK_SIZE:(seq + 1) * CHUNK_SIZE]
        sock.sendto(HEADER.pack(seq) + payload, peer)
        if count % PACE_EVERY == 0:
            time.sleep(0.001)       # let the receiver's buffer drain
    return len(order)


def main(host: str, duplicate: bool, drop: int | None) -> None:
    served: dict[tuple, bytes] = {}         # last file sent to each client
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.bind((host, PORT))
        print(f"[server] UDP file server on {host}:{PORT}, sharing {FILES_FOLDER}/")

        while True:
            request, peer = server.recvfrom(2048)
            text = request.decode(errors="replace").strip()
            verb, _, argument = text.partition(" ")

            if verb == "RESEND":
                data = served.get(peer)
                if data is None:
                    server.sendto(b"ERROR Nothing to resend", peer)
                    continue
                wanted = [int(n) for n in argument.split(",") if n.strip().isdigit()]
                total = -(-len(data) // CHUNK_SIZE)
                wanted = [n for n in wanted if n < total]
                print(f"[server] {peer[1]} asked again for chunk(s) {wanted}")
                send_chunks(server, peer, data, wanted)
                continue

            if verb != "GET" or not argument:
                server.sendto(b"ERROR Bad request", peer)
                continue

            print(f"[server] {peer[0]}:{peer[1]} asked for {argument!r}")
            data = load(argument)
            if isinstance(data, str):
                server.sendto(data.encode(), peer)
                print(f"[server] rejected: {data[6:]}")
                continue

            total = -(-len(data) // CHUNK_SIZE)        # ceiling division
            served[peer] = data
            server.sendto(f"OK {len(data)} {total} {digest(data)}".encode(), peer)

            order = list(range(total))
            if duplicate and total > 12:
                order[10], order[11] = order[11], order[10]      # out of order
                order.insert(4, 3)                               # chunk 3 twice
            if drop is not None and drop in order:
                order.remove(drop)                               # simulated loss
                print(f"[server] chunk {drop} deliberately not sent")

            sent = send_chunks(server, peer, data, order)
            print(f"[server] sent {sent} datagram(s) for {total} chunk(s)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--lan", action="store_true")
    ap.add_argument("--dup", action="store_true", help="duplicate and reorder some chunks")
    ap.add_argument("--drop", type=int, default=None, metavar="SEQ", help="never send this chunk")
    args = ap.parse_args()
    try:
        main("0.0.0.0" if args.lan else "127.0.0.1", args.dup, args.drop)
    except KeyboardInterrupt:
        print("\n[server] stopped by Ctrl+C")
