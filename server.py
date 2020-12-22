import socket

IP = "127.0.0.1"
PORT = 5432
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen()

while True:
    client, address = server.accept()
    print(address)
