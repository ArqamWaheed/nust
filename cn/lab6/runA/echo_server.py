# Group A task 6: UDP echo server (port 5006) - returns exactly the bytes it received
import socket

HOST = "127.0.0.1"
PORT = 5006

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))
print("UDP echo server listening on {}:{}".format(HOST, PORT))

while True:
    data, addr = server_socket.recvfrom(1024)
    print("Echoing {} bytes from {}: {!r}".format(len(data), addr, data))
    if data.decode(errors="replace").strip().lower() == "exit":
        break
    server_socket.sendto(data, addr)          # exactly the same bytes, nothing added

server_socket.close()
print("Echo server closed.")
