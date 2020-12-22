import threading
import socket
import select

host = "0.0.0.0"
port = 5001

HEADER_LENGTH = 10


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((host, port))
server.listen()

clients = []


print(server.recv(1024))


# def broadcast(message):
#     for client in clients:
#         client.send(message)


# def handle(client):
#     while True:
#         try:
#             clients.remove(client)
#             client.close()
#             broadcast(f'Node left the Network!'.encode("ascii"))
#         except:
#             print("ERROR in Handle")
#             break


# def receive():
#     while True:
#         client, address = server.accept()
#         print(f'Connected with {str(address)}')
#         client.send('Welcome to the Network'.encode("ascii"))
#         clients.append(client)

#         broadcast(f'Node joined Network!'.encode("ascii"))

#         thread = threading.Thread(target=handle, args=(client, ))
#         thread.start()


# print("Server is listening...")
# receive()
