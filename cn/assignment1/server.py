import socket
from datetime import datetime

HOST, PORT = "0.0.0.0", 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()
print(f"Server listening on port {PORT}")

count = 0
while True:
    conn, (ip, port) = server.accept()
    with conn:
        try:
            data = conn.recv(1024).decode()
            name, roll = data.split("|", 1)
            count += 1
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            reply = (f"Hello {name} ({roll})\n"
                     f"Your address: {ip}:{port}\n"
                     f"Request number: {count}\n"
                     f"Server date/time: {now}")
            conn.sendall(reply.encode())
            print(f"Request {count} from {ip}:{port} - {name} ({roll}) at {now}")
        except (ValueError, OSError) as e:
            print(f"Bad request from {ip}:{port}: {e}")
