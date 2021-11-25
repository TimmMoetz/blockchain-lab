from block import *
from block_test import write_block
from transaction import *
from textwrap import dedent
from uuid import uuid4
from flask import Flask
from urllib.parse import urlparse
from Crypto.PublicKey import RSA
from Crypto.Signature import *
from time import time
from datetime import datetime
import os
import json
import hashlib

BLOCKCHAIN_DIR = 'blockchain/'


class Blockchain (object):
    def __init__(self):
        self.chain = []

    def getLastBlock(self):
        return self.chain[-1]

    def addBlock(self, block):
        if(len(self.chain) > 0):
            block.prev = self.getLastBlock().hash
        else:
            block.prev = "none"
        self.chain.append(block)
        # write_block(block)

    def get_hash(self, prev_block):
        with open(BLOCKCHAIN_DIR + prev_block, 'rb') as f:
            content = f.read()
        return hashlib.sha256(content).hexdigest()

    def write_block(self, borrower, lender, amount):

        blocks_count = len(os.listdir(BLOCKCHAIN_DIR))
        prev_block = str(blocks_count)

        data = {
            "borrower": borrower,
            "lender": lender,
            "amount": amount,
            "prev_block": {
                "hash": self.get_hash(prev_block),
                "filename": prev_block
            }
        }

        current_block = BLOCKCHAIN_DIR + str(blocks_count + 1)

        with open(current_block, 'w') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.write('\n')

    def chainJSONencode(self):

        blockArrJSON = []
        for block in self.chain:
            blockJSON = {}
            blockJSON['hash'] = block.hash
            blockJSON['prev'] = block.prev

            blockArrJSON.append(blockJSON)

        return blockArrJSON
