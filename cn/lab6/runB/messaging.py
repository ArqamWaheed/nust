"""Experiment 1 and Group A tasks 1-3 in one file (TCP, port 5000).

    python3 messaging.py server
    python3 messaging.py client  "Hello Server" "Computer Networks" ...

Server behaviour: greets the client, numbers every message and answers with the
text reversed.  Both roles live here so the protocol is defined in one place.
"""
import argparse
import socket
import sys

ADDRESS = ("127.0.0.1", 5000)
WELCOME = "Welcome to the Computer Networks Lab"


def transform(number: int, text: str) -> str:
    """The server's reply for message `number`."""
    return f"[{number}] {text[::-1]}"


def serve() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind(ADDRESS)
        listener.listen(1)
        print(f"[server] listening on {ADDRESS[0]}:{ADDRESS[1]}")

        conn, peer = listener.accept()
        with conn, conn.makefile("rwb", buffering=0) as stream:
            print(f"[server] connected by {peer[0]}:{peer[1]}")
            stream.write((WELCOME + "\n").encode())

            counter = 0
            for raw in stream:                       # one iteration per line
                text = raw.decode().rstrip("\n")
                counter += 1
                print(f"[server] message {counter}: {text}")
                if text.lower() == "exit":
                    break
                stream.write((transform(counter, text) + "\n").encode())

        print(f"[server] closed after {counter} message(s)")


def talk(messages: list[str]) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect(ADDRESS)
        with client.makefile("rwb", buffering=0) as stream:
            print(f"[client] connected, local port {client.getsockname()[1]}")
            print("[client] greeting:", stream.readline().decode().strip())

            for text in messages + ["exit"]:
                print("[client] sending :", text)
                stream.write((text + "\n").encode())
                if text.lower() == "exit":
                    break
                print("[client] reply   :", stream.readline().decode().strip())
    print("[client] closed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("role", choices=["server", "client"])
    ap.add_argument("messages", nargs="*", help="client only: messages to send")
    args = ap.parse_args()
    if args.role == "server":
        serve()
    else:
        talk(args.messages or [line.rstrip("\n") for line in sys.stdin])
