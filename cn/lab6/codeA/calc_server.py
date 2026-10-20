# Group A task 5: TCP calculator server (port 5005)
# Protocol: the client sends "<num1> <op> <num2>" on one line, the server replies with the result.
import socket

HOST = "127.0.0.1"
PORT = 5005

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print("Calculator server listening on {}:{}".format(HOST, PORT))

conn, addr = server_socket.accept()
print("Connected by:", addr)

while True:
    data = conn.recv(1024)
    if not data:
        break
    text = data.decode().strip()
    if text.lower() == "exit":
        break
    print("Expression:", text)
    parts = text.split()
    if len(parts) != 3:
        answer = "ERROR send: number operator number"
    else:
        try:
            a, op, b = float(parts[0]), parts[1], float(parts[2])
            if op == "+":
                answer = "Result: {:g}".format(a + b)
            elif op == "-":
                answer = "Result: {:g}".format(a - b)
            elif op == "*":
                answer = "Result: {:g}".format(a * b)
            elif op == "/":
                answer = "ERROR division by zero" if b == 0 else "Result: {:g}".format(a / b)
            else:
                answer = "ERROR unknown operator " + op
        except ValueError:
            answer = "ERROR those are not numbers"
    print("  ->", answer)
    conn.send(answer.encode())

conn.close()
server_socket.close()
print("Calculator server closed.")
