from src.blockchain.block import Block
from src.db.mapper import Mapper
import hashlib


class Blockchain():
    def add_block(self, transactions):

        pred_hash = Mapper().read_latest_block_hash()

        block = Block(pred=pred_hash)
        for transaction in transactions:
            block.add_transaction(transaction)
        block.write_to_file()

        hash = block.hash()
        Mapper().write_latest_block_hash(hash)

    def create_genesis_block(self):
        block = Block()
        block = block.serialize()
        hash = hashlib.sha256(block).hexdigest()

        Mapper().write_block(hash, block)

        Mapper().write_latest_block_hash(hash)