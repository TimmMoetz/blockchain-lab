from block import *
from transaction import *
from textwrap import dedent
from uuid import uuid4
from flask import Flask
from urllib.parse import urlparse
from Crypto.PublicKey import RSA
from Crypto.Signature import *
from time import time
from datetime import datetime


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

    def chainJSONencode(self):

        blockArrJSON = []
        for block in self.chain:
            blockJSON = {}
            blockJSON['hash'] = block.hash
            blockJSON['prev'] = block.prev

            blockArrJSON.append(blockJSON)

        return blockArrJSON
