import socket
import sys

HOST = sys.argv[1] if len(sys.argv) > 1 else "localhost"
PORT = 6000

name = input("Enter name: ")
roll = input("Enter roll number: ")

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    sock.connect((HOST, PORT))
    sock.sendall(f"{name};{roll}".encode())
    print("\nServer says:\n" + sock.recv(1024).decode())
    sock.close()
except OSError as e:
    print(f"Connection to {HOST}:{PORT} failed: {e}")
