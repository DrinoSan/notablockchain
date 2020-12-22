import socket

IP = "95.179.188.56"
PORT = 5001
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen()

while True:
    client, address = server.accept()
    print(address)
    client.send("TEXT")
