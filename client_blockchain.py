from collections import OrderedDict

import binascii

import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

import requests
from flask import Flask, jsonify, request, render_template


class Transaction:

    def __init__(self, sender_adress, sender_private_key, recipient_address, value):
        self.sender_adress = sender_adress.strip()
        self.sender_private_key = sender_private_key.strip()
        self.recipient_address = recipient_address.strip()
        self.value = value.strip()

    def __getattr__(self, attr):
        return self.data[attr]

    def to_dict(self):
        return OrderedDict({"sender_adress": self.sender_adress,
                            "recipient_address": self.recipient_address,
                            "value": self.value})

    def sign_transaction(self):
        """
        Sign tx with private key
        """
        private_key = RSA.importKey(
            binascii.unhexlify(self.sender_private_key))
        signer = PKCS1_v1_5.new(private_key)
        h = SHA.new(str(self.to_dict()).encode("utf-8"))
        return binascii.hexlify(signer.sign(h)).decode("ascii")


app = Flask(__name__)


@app.route("/wallet/new", methods=["GET"])
def new_wallet():
    random_gen = Crypto.Random.new().read
    private_key = RSA.generate(1024, random_gen)
    public_key = private_key.publickey()
    response = {
        "-----WARNING-----": "YOU MUST NEVER SHARE THE PRIVATE KEY. IF YOU LOSE THE PRIVATE KEY YOUR DATA ON IT IS LOST... as your life is",
        'private_key': binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'),
        'public_key': binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii')
    }
    return jsonify(response), 200


@app.route("/create/transactions")
def get_transaction_details():
    return render_template("tx_keys.html")


@ app.route("/create/transactions", methods=["POST"])
def create_transactions():
    sender_adress = request.form["sender"].strip()
    sender_private_key = request.form["private"].strip()
    receiver_address = request.form["receiver"].strip()
    value = request.form["value"].strip()

    print(type(sender_adress))
    print("-"*80)
    data = {
        "sender_adress": sender_adress,
        "sender_private_key": sender_private_key,
        "receiver_address": receiver_address,
        "Amount": value,
    }

    transaction = Transaction(
        sender_adress, sender_private_key, receiver_address, value)

    sender_adress.strip()
    print("-"*50)
    response = {"transaction": transaction.to_dict(
    ), "signature": transaction.sign_transaction()}

    print("HHHEEE")
    # print(response)
    return jsonify(response), 200


# # sending post request and saving response as response object
# r = requests.post(url=API_ENDPOINT, data=data)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=8080,
                        type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)
