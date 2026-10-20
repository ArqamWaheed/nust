# Experiment 5: simple file download over TCP
import socket
import sys

SERVER_IP = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
PORT = 5002
SAVE_AS = "received_share_me.txt"

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, PORT))
print("Connected to file server at", SERVER_IP)

total = 0
with open(SAVE_AS, "wb") as f:
    while True:
        data = client_socket.recv(1024)
        if not data:                  # server closed the connection
            break
        f.write(data)
        total += len(data)

client_socket.close()
print("File saved as:", SAVE_AS)
print("Bytes received:", total)
