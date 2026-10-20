# Experiment 4: one recv(1024), or three recv(5) calls with --split
import socket
import sys
import time

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 5004))
time.sleep(0.5)              # let all three sends arrive first

if "--split" in sys.argv:
    for i in range(1, 4):
        piece = client_socket.recv(5)          # step 3: small buffer
        print("recv(5) call {} returned: {}  ({} bytes)".format(i, piece, len(piece)))
else:
    data = client_socket.recv(1024)            # step 2: ONE recv() call
    print("recv() returned:", data)
    print("Number of bytes:", len(data))

client_socket.close()
