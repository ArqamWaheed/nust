# Experiment 5: simple file sharing over TCP (port 5002)
import socket
import sys

HOST = "0.0.0.0" if "--lan" in sys.argv else "127.0.0.1"
PORT = 5002
FILE_NAME = "share_me.txt"

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print("File server waiting for a client on {}:{}".format(HOST, PORT))

conn, addr = server_socket.accept()
print("Connected by:", addr)

sent = 0
with open(FILE_NAME, "rb") as f:
    while True:
        chunk = f.read(1024)
        if not chunk:                 # end of file reached
            break
        conn.sendall(chunk)
        sent += len(chunk)

print("File sent. Bytes sent:", sent)
conn.close()
server_socket.close()
