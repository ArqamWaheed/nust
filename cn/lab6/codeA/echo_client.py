# Group A task 6: UDP echo client - proves the reply is byte-for-byte identical
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.settimeout(3)
print("UDP echo client started.")

while True:
    try:
        text = input("Enter message: ")
    except EOFError:
        break
    print(text)
    sent = text.encode()
    client.sendto(sent, ("127.0.0.1", 5006))
    if text.lower() == "exit":
        break
    back, _ = client.recvfrom(1024)
    print("Echo: {!r}  identical: {}".format(back.decode(), back == sent))

client.close()
print("Client closed.")
