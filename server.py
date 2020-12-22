import socket

IP = "95.179.188.56"
PORT = 5001
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((IP, PORT))
server.listen()

while True:
    client, address = server.accept()
    print(address)
    client.send("TEXT".encode("utf-8"))
    m = client.recv(1024).decode("utf-8")
    print(m)
