# Simulates a friend's machine by sending from that machine's IP and port
import runpy
import socket
import sys

ip, port = sys.argv.pop(1), int(sys.argv.pop(1))
_connect = socket.socket.connect

def connect(self, addr):
    self.bind((ip, port))
    return _connect(self, addr)

socket.socket.connect = connect
runpy.run_path("client.py", run_name="__main__")
