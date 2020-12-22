import socket
from server import IP, PORT


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))
