from block import Block
from Mapper import Mapper
import os
import json


class Blockchain():
    def add_block(self, transactions):

        pred_hash = Mapper().read_latest_block_hash()

        block = Block(pred=pred_hash)
        for transaction in transactions:
            block.add_transaction(transaction)

        block.write_to_file()

        hash = block.hash()
        Mapper().write_latest_block_hash(hash)
