from datetime import datetime
import hashlib
import json
from abc import ABC, abstractmethod

BLOCKCHAIN_DIR = 'blocks/'


class Serializable(ABC):
    def serialize(self):
        return json.dumps(self.to_dict(),
                          sort_keys=True).encode("utf-8")

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

    def to_dict(self):
        transactions = list()
        for t in self. transactions:
            transactions.append(t.to_dict())

        return {
            "predecessor": self.predecessor,
            "transactions": transactions
        }

    def hash(self):
        print("Erzeuge Hash für:", self.serialize())
        return hashlib.sha256(self.serialize()).hexdigest()

    def write_to_file(self, directory):
        h = self.hash()
        try:
            with open(directory + "/" + str(h), "w") as file:
                file.write(str(self.serialize()))
        except EOFError:
            print("...")


def main():
    b1 = Block(pred=None)
    t1 = Transaction(source='Timme', target='Jan', amount=1000)
    b1.add_transaction(t1)
    b1.write_to_file("./blocks")


if __name__ == '__main__':
    main()
