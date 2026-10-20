# Experiment 1: TCP messaging client
import socket

HOST = "127.0.0.1"
PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print("Connected to TCP server.")
print("Server:", client_socket.recv(1024).decode().strip())   # welcome line

while True:
    try:
        message = input("Enter message: ")
    except EOFError:
        break
    print(message)                     # echo so the transcript shows what was typed
    client_socket.send(message.encode())
    if message.lower() == "exit":
        break
    response = client_socket.recv(1024)
    print("Server:", response.decode())

client_socket.close()
print("Client closed.")
