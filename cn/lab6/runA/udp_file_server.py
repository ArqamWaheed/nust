# Experiment 9: file transfer over UDP (port 6001)
import hashlib
import os
import socket
import struct
import sys
import time

HOST = "0.0.0.0" if "--lan" in sys.argv else "127.0.0.1"
PORT = 6001                 # different from the TCP file server (6000)
FILES_FOLDER = "server_files"
CHUNK_SIZE = 1024           # payload bytes per datagram
PACE_EVERY = 50             # short pause after this many packets

TEST_DUP_REORDER = "--dup" in sys.argv       # duplicate one chunk, swap two chunks
TEST_DROP_CHUNK = 7 if "--drop" in sys.argv else None   # never send chunk 7 (simulates loss)


def is_valid_name(name):
    return name != "" and name == os.path.basename(name) and ".." not in name


def sha256_of(path):
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            sha.update(block)
    return sha.hexdigest()


server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))
print("UDP file server listening on {}:{}".format(HOST, PORT))

while True:
    request, addr = server.recvfrom(1024)
    text = request.decode(errors="replace").strip()
    parts = text.split(" ", 1)
    if len(parts) != 2 or parts[0] != "GET":
        server.sendto(b"ERROR Bad request", addr)
        continue

    filename = parts[1]
    print("Request from", addr, "for:", repr(filename))

    if not is_valid_name(filename):
        server.sendto(b"ERROR Invalid filename", addr)
        continue
    path = os.path.join(FILES_FOLDER, filename)
    if not os.path.isfile(path):
        server.sendto(b"ERROR File not found", addr)
        continue

    size = os.path.getsize(path)
    total_chunks = (size + CHUNK_SIZE - 1) // CHUNK_SIZE
    info = "OK {} {} {}".format(size, total_chunks, sha256_of(path))
    server.sendto(info.encode(), addr)

    with open(path, "rb") as f:
        data = f.read()

    order = list(range(total_chunks))
    if TEST_DUP_REORDER and total_chunks > 12:
        order[10], order[11] = order[11], order[10]   # out-of-order
        order.insert(4, 3)                            # chunk 3 sent twice
    if TEST_DROP_CHUNK is not None and TEST_DROP_CHUNK in order:
        order.remove(TEST_DROP_CHUNK)                 # lost chunk

    sent = 0
    for count, seq in enumerate(order, start=1):
        payload = data[seq * CHUNK_SIZE:(seq + 1) * CHUNK_SIZE]
        server.sendto(struct.pack("!I", seq) + payload, addr)
        sent += 1
        if count % PACE_EVERY == 0:
            time.sleep(0.001)
    print("Sent {} datagrams ({} chunks in the file)".format(sent, total_chunks))
