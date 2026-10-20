# Group A task 5: TCP calculator client
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 5005))
print("Connected to calculator server.")

while True:
    try:
        text = input("Expression: ")
    except EOFError:
        break
    print(text)
    client.send(text.encode())
    if text.lower() == "exit":
        break
    print("Server:", client.recv(1024).decode())

client.close()
print("Client closed.")
