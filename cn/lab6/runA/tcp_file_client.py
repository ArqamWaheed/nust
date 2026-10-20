# Experiment 8: TCP file client - size header, exact-length receive, hash check
import hashlib
import socket
import sys
import time

SERVER_IP = sys.argv[2] if len(sys.argv) > 2 else "127.0.0.1"
PORT = 6000
BUFFER_SIZE = 4096


def recv_line(sock, limit=255):
    line = b""
    while not line.endswith(b"\n"):
        ch = sock.recv(1)
        if not ch:
            raise ConnectionError("Server closed before replying")
        line += ch
        if len(line) > limit:
            raise ValueError("Reply line too long")
    return line.decode().strip()


filename = sys.argv[1] if len(sys.argv) > 1 else input("File to request: ")
save_as = "received_tcp_" + filename.replace("/", "_").replace("\\", "_")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.settimeout(10)

try:
    client.connect((SERVER_IP, PORT))
    start = time.perf_counter()
    client.sendall((filename + "\n").encode())

    reply = recv_line(client).split()
    if reply[0] != "OK":
        print("Server error:", " ".join(reply[1:]))
        sys.exit(1)

    size, expected_hash = int(reply[1]), reply[2]
    received = 0
    sha = hashlib.sha256()

    with open(save_as, "wb") as f:
        while received < size:
            data = client.recv(min(BUFFER_SIZE, size - received))
            if not data:
                raise ConnectionError("Connection closed early: got {} of {} bytes"
                                      .format(received, size))
            f.write(data)
            sha.update(data)
            received += len(data)

    elapsed = time.perf_counter() - start
    throughput = (received / 1024) / elapsed
    ok = sha.hexdigest() == expected_hash

    print("Protocol       : TCP")
    print("Filename       :", filename)
    print("Bytes received :", received)
    print("Elapsed time   : {:.4f} s".format(elapsed))
    print("Throughput     : {:.2f} KB/s".format(throughput))
    print("File integrity :", "MATCH" if ok else "MISMATCH")

except (ConnectionError, socket.timeout, OSError) as error:
    print("Transfer failed:", error)
finally:
    client.close()
