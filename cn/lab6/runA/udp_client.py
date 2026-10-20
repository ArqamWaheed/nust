# Experiment 2: UDP messaging client
import socket

HOST = "127.0.0.1"
PORT = 5001

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("UDP Client started.")

while True:
    try:
        message = input("Enter message: ")
    except EOFError:
        break
    print(message)
    client_socket.sendto(message.encode(), (HOST, PORT))
    if message.lower() == "exit":
        break
    data, server_address = client_socket.recvfrom(1024)
    print("Server:", data.decode())

client_socket.close()
print("Client closed.")
