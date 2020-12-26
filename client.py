import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4


import threading
import socket
import select

import requests


if __name__ == "__main__":

    IP = "95.179.188.56"
    PORT = 5002

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((IP, PORT))

    m = client.recv(1024).decode()
    print(m)
    test_msg = "TEST this is coming from the client"
    # s = input("PLEASE ENTER TEYXT").encode()
    client.send(test_msg.encode())
