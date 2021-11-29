from block import Block
import os
import json

class Blockchain(): 
    def __init__(self) -> None:
        self.blockchain_dir = "./blockchain"

    def get_best_block(self):
        block_file_names = os.listdir(self.blockchain_dir)
        best_block_file_name = block_file_names[len(block_file_names) -1]
        with open(self.blockchain_dir + "/" + best_block_file_name) as file:
            best_block_str = file.read()
        best_block = json.loads(best_block_str)
        return best_block

    def add_block(self, transactions):                             
        best_block = self.get_best_block()
        pred_hash = best_block['hash']

        block = Block(pred=pred_hash)
        for transaction in transactions:
            block.add_transaction(transaction)

        block.write_to_file(self.blockchain_dir)



