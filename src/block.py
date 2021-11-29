from datetime import datetime
import hashlib
import json
from abc import ABC, abstractmethod
import os

class Serializable(ABC):
    def serialize(self, hash = None):
        return json.dumps(self.to_dict(hash),
                          sort_keys=True)

    @abstractmethod
    def to_dict(self):
        pass


class Transaction(Serializable):
    def __init__(self, source=None, target=None, amount=0):
        self.__source = source
        self.__target = target
        self.__amount = amount
        self.__timestamp = datetime.now()

    def to_dict(self):
        return {
            "source": self.__source,
            "target": self.__target,
            "amount": self.__amount,
            "timestamp": self.__timestamp.strftime("%m/%d/%Y, %H:%M:%S")
        }


class Block(Serializable):
    def __init__(self, pred=None):
        self.predecessor = pred
        self.transactions = list()

    def add_transaction(self, t):
        self.transactions.append(t)

    def to_dict(self, hash = None):
        transactions = list()
        for t in self.transactions:
            transactions.append(t.to_dict())

        if hash:
            return {
                "hash": hash,
                "block": {
                    "predecessor": self.predecessor,
                    "transactions": transactions
                }
            }
        else:
            return {
                "block": {
                    "predecessor": self.predecessor,
                    "transactions": transactions
                }
            }

    def hash(self):
        print("Erzeuge Hash für:", self.serialize())
        return hashlib.sha256(self.serialize().encode("utf-8")).hexdigest()

    def write_to_file(self, directory):
        blocks_count = len(os.listdir(directory))
        current_block_index = "blk" + str(blocks_count + 1)

        hash = self.hash()
        try:
            with open(directory + "/" + current_block_index, "w") as file:
                file.write(str(self.serialize(hash)))
        except EOFError:
            print("...")