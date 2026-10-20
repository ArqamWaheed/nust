# Experiment 8: request-response file server over TCP (port 6000)
import hashlib
import os
import socket
import sys
import time

HOST = "0.0.0.0" if "--lan" in sys.argv else "127.0.0.1"
PORT = 6000
FILES_FOLDER = "server_files"
CHUNK_SIZE = 1024
SLOW_DEMO = "--slow" in sys.argv       # True = pause after each chunk (for the premature-closure test)


def recv_line(conn, limit=255):
    """Read bytes one at a time until a newline is found."""
    line = b""
    while not line.endswith(b"\n"):
        ch = conn.recv(1)
        if not ch:
            raise ConnectionError("Client closed the connection early")
        line += ch
        if len(line) > limit:
            raise ValueError("Request line too long")
    return line.decode().strip()


def is_valid_name(name):
    """Accept plain file names only (no folders, no '..')."""
    return name != "" and name == os.path.basename(name) and ".." not in name


def sha256_of(path):
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            sha.update(block)
    return sha.hexdigest()


def handle_client(conn, addr):
    filename = recv_line(conn)
    print("Request from", addr, "for:", repr(filename))

    if not is_valid_name(filename):
        conn.sendall(b"ERROR Invalid filename\n")
        print("Rejected: invalid filename")
        return

    path = os.path.join(FILES_FOLDER, filename)
    if not os.path.isfile(path):
        conn.sendall(b"ERROR File not found\n")
        print("Rejected: file not found")
        return

    size = os.path.getsize(path)
    header = "OK {} {}\n".format(size, sha256_of(path))
    conn.sendall(header.encode())

    start = time.perf_counter()
    sent = 0
    with open(path, "rb") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            conn.sendall(chunk)
            sent += len(chunk)
            if SLOW_DEMO:
                time.sleep(0.05)
    elapsed = time.perf_counter() - start
    print("Sent {} bytes in {:.4f} s".format(sent, elapsed))


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print("TCP file server listening on {}:{}".format(HOST, PORT))

while True:
    conn, addr = server_socket.accept()
    try:
        handle_client(conn, addr)
    except Exception as error:
        print("Transfer failed:", error)
    finally:
        conn.close()
