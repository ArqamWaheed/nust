# Experiment 9: UDP file client - sequence numbers, duplicate detection, reassembly
import hashlib
import socket
import struct
import sys
import time

SERVER_IP = sys.argv[2] if len(sys.argv) > 2 else "127.0.0.1"
PORT = 6001
TIMEOUT = 2.0               # seconds to wait for the next datagram
MAX_TRIES = 3               # request attempts
HEADER = struct.calcsize("!I")

filename = sys.argv[1] if len(sys.argv) > 1 else input("File to request: ")
save_as = "received_udp_" + filename.replace("/", "_").replace("\\", "_")

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 4 * 1024 * 1024)
client.settimeout(TIMEOUT)

# ---- Step 1: send the request and wait for the OK / ERROR reply ----
start = time.perf_counter()
reply = None
for attempt in range(1, MAX_TRIES + 1):
    client.sendto(("GET " + filename).encode(), (SERVER_IP, PORT))
    try:
        reply, _ = client.recvfrom(2048)
        break
    except socket.timeout:
        print("No reply (attempt {} of {})".format(attempt, MAX_TRIES))

if reply is None:
    print("Transfer failed: server did not respond")
    sys.exit(1)

fields = reply.decode(errors="replace").split()
if fields[0] != "OK":
    print("Server error:", " ".join(fields[1:]))
    sys.exit(1)

size, total_chunks, expected_hash = int(fields[1]), int(fields[2]), fields[3]

# ---- Step 2: receive chunks until all have arrived ----
chunks = {}
duplicates = 0
unexpected = 0

try:
    while len(chunks) < total_chunks:
        packet, _ = client.recvfrom(HEADER + 65535)
        if len(packet) < HEADER:
            unexpected += 1
            continue
        seq = struct.unpack("!I", packet[:HEADER])[0]
        if seq >= total_chunks:
            unexpected += 1               # sequence number outside the valid range
        elif seq in chunks:
            duplicates += 1               # already received
        else:
            chunks[seq] = packet[HEADER:]
except socket.timeout:
    pass

elapsed = time.perf_counter() - start
client.close()

# ---- Step 3: check and reassemble ----
missing = [n for n in range(total_chunks) if n not in chunks]
if missing:
    print("Transfer incomplete. Missing chunks:", missing[:20])
    print("Received {} of {} chunks".format(len(chunks), total_chunks))
    sys.exit(1)

data = b"".join(chunks[n] for n in range(total_chunks))
with open(save_as, "wb") as f:
    f.write(data)

throughput = (len(data) / 1024) / elapsed
ok = hashlib.sha256(data).hexdigest() == expected_hash

print("Protocol          : UDP")
print("Filename          :", filename)
print("Bytes received    :", len(data), "of", size)
print("Chunks            :", total_chunks)
print("Duplicates ignored:", duplicates)
print("Unexpected packets:", unexpected)
print("Elapsed time      : {:.4f} s".format(elapsed))
print("Throughput        : {:.2f} KB/s".format(throughput))
print("File integrity    :", "MATCH" if ok else "MISMATCH")
