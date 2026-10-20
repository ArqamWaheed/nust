# Experiment 1 + Group A tasks 1, 2, 3: TCP messaging server
# Sends a welcome line, numbers every message and replies with the text reversed.
import socket

HOST = "127.0.0.1"
PORT = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print("TCP Server is waiting for a connection...")

conn, addr = server_socket.accept()
print("Connected by:", addr)
conn.send(b"Welcome to the Computer Networks Lab\n")   # Task 1

count = 0
while True:
    data = conn.recv(1024)
    if not data:
        break
    message = data.decode().strip()
    count += 1                                          # Task 2
    print("Message {}: {}".format(count, message))
    if message.lower() == "exit":
        break
    response = "Server received: " + message[::-1]      # Task 3 (reversed)
    conn.send(response.encode())

conn.close()
server_socket.close()
print("Server closed. Messages handled:", count)
