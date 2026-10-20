"""Experiment 2 and Group A tasks 4 and 6 in one file (UDP, port 5001).

    python3 udp_messaging.py server --mode upper     # task 4: reply in UPPERCASE
    python3 udp_messaging.py server --mode echo      # task 6: reply byte-for-byte
    python3 udp_messaging.py client "one" "two" ...

Only the reply rule changes between the two tasks, so one dispatch table covers both.
"""
import argparse
import socket
import sys

ADDRESS = ("127.0.0.1", 5001)

MODES = {
    "upper": lambda data: f"Server received: {data.decode().upper()}".encode(),
    "echo":  lambda data: data,                       # exactly what arrived
}


def serve(mode: str) -> None:
    reply_for = MODES[mode]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.bind(ADDRESS)
        print(f"[server] UDP {mode} server on {ADDRESS[0]}:{ADDRESS[1]}")
        while True:
            data, peer = server.recvfrom(1024)        # one datagram per call
            text = data.decode(errors="replace").rstrip("\n")
            print(f"[server] {len(data):>3} bytes from port {peer[1]}: {text}")
            if text.lower() == "exit":
                break
            server.sendto(reply_for(data), peer)
    print("[server] closed")


def talk(messages: list[str]) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
        client.settimeout(3)
        print("[client] UDP client started (no connect, no handshake)")
        for text in messages + ["exit"]:
            payload = text.encode()
            client.sendto(payload, ADDRESS)
            print("[client] sent    :", text)
            if text.lower() == "exit":
                break
            back, _ = client.recvfrom(1024)
            same = "identical" if back == payload else "changed"
            print(f"[client] reply   : {back.decode()}   ({same})")
    print("[client] closed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("role", choices=["server", "client"])
    ap.add_argument("messages", nargs="*")
    ap.add_argument("--mode", choices=list(MODES), default="upper")
    args = ap.parse_args()
    if args.role == "server":
        serve(args.mode)
    else:
        talk(args.messages or [line.rstrip("\n") for line in sys.stdin])
