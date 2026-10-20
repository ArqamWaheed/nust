import socket
from datetime import datetime

PORT = 6000

srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind(("", PORT))
srv.listen(5)
print(f"Server running on port {PORT}")

requests = 0
while True:
    conn, addr = srv.accept()
    try:
        name, roll = conn.recv(1024).decode().split(";", 1)
        requests += 1
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = (f"Hello {name} ({roll})\n"
               f"Your address: {addr[0]}:{addr[1]}\n"
               f"Request number: {requests}\n"
               f"Server date/time: {stamp}")
        conn.sendall(msg.encode())
        print(f"[{stamp}] Request {requests}: {name} ({roll}) from {addr[0]}:{addr[1]}")
    except (ValueError, OSError) as e:
        print(f"Invalid request from {addr[0]}:{addr[1]}: {e}")
    finally:
        conn.close()
