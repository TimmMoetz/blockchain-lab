from blockchain import *
from block import *
import hashlib
import json
from textwrap import dedent
from uuid import uuid4
from flask import Flask
from urllib.parse import urlparse
from Crypto.PublicKey import RSA
from Crypto.Signature import *
from time import time
from datetime import datetime


class Transaction (object):
    def __init__(self, sender, reciever, amount):
        self.sender = sender
        self.reciever = reciever
        self.amount = amount
        self.time = time()
        self.hash = self.calculateHash()

    def calculateHash(self):
        hashString = self.sender + self.reciever + \
            str(self.amount) + str(self.time)
        hashEncoded = json.dumps(hashString, sort_keys=True).encode()
        return hashlib.sha256(hashEncoded).hexdigest()
