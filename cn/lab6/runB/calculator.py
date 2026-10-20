"""Group A task 5: TCP calculator (port 5005), server and client in one file.

    python3 calculator.py server
    python3 calculator.py client "12 + 8" "7 * 6" "10 / 0"

The operators come from the standard `operator` module, so adding one is a single
dictionary entry instead of another elif branch.
"""
import argparse
import operator
import socket

ADDRESS = ("127.0.0.1", 5005)
OPS = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}


def evaluate(line: str) -> str:
    fields = line.split()
    if len(fields) != 3:
        return "ERROR expected: number operator number"
    left, symbol, right = fields
    if symbol not in OPS:
        return f"ERROR unknown operator {symbol!r} (use + - * /)"
    try:
        a, b = float(left), float(right)
    except ValueError:
        return f"ERROR {left!r} or {right!r} is not a number"
    try:
        return f"Result: {OPS[symbol](a, b):g}"
    except ZeroDivisionError:
        return "ERROR division by zero"


def serve() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind(ADDRESS)
        listener.listen(1)
        print(f"[server] calculator ready on {ADDRESS[0]}:{ADDRESS[1]}")
        conn, peer = listener.accept()
        with conn, conn.makefile("rwb", buffering=0) as stream:
            print(f"[server] connected by {peer[0]}:{peer[1]}")
            for raw in stream:
                line = raw.decode().strip()
                if line.lower() == "exit":
                    break
                answer = evaluate(line)
                print(f"[server] {line:<12} -> {answer}")
                stream.write((answer + "\n").encode())
    print("[server] closed")


def ask(expressions: list[str]) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect(ADDRESS)
        with client.makefile("rwb", buffering=0) as stream:
            for line in expressions:
                stream.write((line + "\n").encode())
                print(f"[client] {line:<12} -> {stream.readline().decode().strip()}")
            stream.write(b"exit\n")
    print("[client] closed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("role", choices=["server", "client"])
    ap.add_argument("expressions", nargs="*")
    args = ap.parse_args()
    serve() if args.role == "server" else ask(
        args.expressions or ["12 + 8", "7 * 6", "45 / 4", "10 / 0", "5 ^ 2"])
