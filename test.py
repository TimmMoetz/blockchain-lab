from blockchain import *
from block import *
from transaction import *
from time import time
import pprint

pp = pprint.PrettyPrinter(indent=4)

blockchain = Blockchain()
transactions = [
    """    {'hash': 1, 
     "borrower": "Timm",
     "lender": "Jan",
     "amount": 100
    }
    """
]


block = Block(transactions, time(), 0)
blockchain.addBlock(block)

block = Block(transactions, time(), 1)
blockchain.addBlock(block)

block = Block(transactions, time(), 2)
blockchain.addBlock(block)

pp.pprint(blockchain.chainJSONencode())
print("Länge: ", len(blockchain.chain))
