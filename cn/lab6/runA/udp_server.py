# Experiment 2 + Group A task 4: UDP messaging server, replies in UPPERCASE
import socket

HOST = "127.0.0.1"
PORT = 5001

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))
print("UDP Server is waiting for messages...")

while True:
    data, addr = server_socket.recvfrom(1024)
    message = data.decode().strip()
    print("Client {}: {}".format(addr[1], message))
    if message.lower() == "exit":
        break
    response = "Server received: " + message.upper()     # Task 4
    server_socket.sendto(response.encode(), addr)

server_socket.close()
print("UDP Server closed.")
