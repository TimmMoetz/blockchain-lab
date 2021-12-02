from block import Block
import os
import json

class Blockchain(): 
    def __init__(self) -> None:
        self.blockchain_dir = os.path.dirname(os.path.realpath(__file__)) + "/blockchain"
        self.latest_block_hash_file = os.path.dirname(os.path.realpath(__file__)) + "/latest_block_hash"
    
    def get_block(self, hash):
        with open(self.blockchain_dir + "/" + hash, "rb") as file:
            block_str = file.read()
            block = json.loads(block_str)
        return block

    def add_block(self, transactions):   
        
        with open(self.latest_block_hash_file) as file:
            pred_hash = file.read()

        block = Block(pred=pred_hash)
        for transaction in transactions:
            block.add_transaction(transaction)

        block.write_to_file(self.blockchain_dir)

        with open(self.latest_block_hash_file, "w") as file:
            file.write(str(block.hash()))


