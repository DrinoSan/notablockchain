import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4


########
import threading
import socket
import select

import requests


class Blockchain:

    difficulty = 5

    def __init__(self, IP):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()
        self.ip = (IP + ":5002")

        self.new_block(previous_hash="TEST", proof=420)

    def new_block(self, proof, previous_hash):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": time(),
            "transactions": self.current_transactions,
            "proof": proof,
            "previous_hash": previous_hash or self.hash(self.chain[-1]),
        }

        self.current_transactions = []
        self.chain.append(block)

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_block):
        last_proof = last_block["proof"]
        last_hash = self.hash(last_block)

        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:Blockchain.difficulty] == (Blockchain.difficulty * "0")

    @property
    def last_block(self):
        return self.chain[-1]

    def mine(self):
        while True:
            print("Inside Mine")
            last_block = self.last_block
            new_proof = self.proof_of_work(last_block)

            self.new_transaction(
                sender="0",
                recipient=node_identifier,
                amount=1
            )

            previous_hash = self.hash(last_block)
            self.new_block(new_proof, previous_hash)

            print("New block has been forged with the index: {}".format
                  (self.chain[-1]["index"]))
            print(15 * "-")
            print("Content of forged Block: ")
            print(json.dumps(self.chain[-1], indent=4))
            print("LEAVING MINE")

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1


if __name__ == "__main__":

    node_identifier = str(uuid4()).replace('-', '')
    IP = "95.179.188.56"
    PORT = 5002
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((IP, PORT))
    server.listen()

    # while True:
    client, address = server.accept()
    print(address)
    client.send("TEXT".encode("utf-8"))
    m = client.recv(1024).decode("utf-8")
    print(m)
    blockchain = Blockchain(IP)
    t = threading.Thread(target=blockchain.mine)
    t.start()
