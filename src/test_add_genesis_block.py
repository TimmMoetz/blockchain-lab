from block import Block
import os

b1 = Block(pred=None)
b1.write_to_file(os.path.dirname(os.path.realpath(__file__)) + "/blockchain")