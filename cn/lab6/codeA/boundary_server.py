# Experiment 4: TCP is a byte stream (server side, port 5004)
import socket
import time

HOST = "127.0.0.1"
PORT = 5004

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print("Boundary demo server waiting...")

conn, addr = server_socket.accept()
print("Connected by:", addr)
conn.sendall(b"AAAA")        # three separate send() calls
conn.sendall(b"BBBB")
conn.sendall(b"CCCC")
print("Sent AAAA, BBBB, CCCC in three sendall() calls")
time.sleep(1)                # keep the connection open for a moment
conn.close()
server_socket.close()
