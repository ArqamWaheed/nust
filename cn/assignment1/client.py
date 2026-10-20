import socket
import sys

SERVER = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
PORT = 5000

name = input("Enter name: ")
roll = input("Enter roll number: ")

try:
    with socket.create_connection((SERVER, PORT), timeout=10) as s:
        s.sendall(f"{name}|{roll}".encode())
        reply = s.recv(1024).decode()
    print("\nServer says:\n" + reply)
except OSError as e:
    print(f"Could not reach server {SERVER}:{PORT}: {e}")
