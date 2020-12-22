import socket


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect("95.179.188.56", 5001)


client.send(f'Test connection'.encode("utf-8"))
