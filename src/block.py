from time import time
import json
import hashlib


class Block (object):
    def __init__(self, time, index, transactions):
        self.time = time  # Time block created
        self.index = index  # Block number
        self.transactions = transactions  # Transaction data
        self.hash = self.calculateHash()  # Hash of a block
        self.prev = ''  # Hash of previous block

    def calculateHash(self):
        hashTransactions = ""
        for transaction in self.transactions:
            hashTransactions += transaction.hash

        hashString = str(self.time) + hashTransactions + \
            self.prev + str(self.index)
        hashEncoded = json.dumps(hashString, sort_keys=True).encode()
        return hashlib.sha256(hashEncoded).hexdigest()
