from block import Transaction
from blockchain import Blockchain

transactions = [Transaction("moiiin", "Stephan", 100.0),
                Transaction("Stephan", "dsfdf", 5.0)]
blockchain = Blockchain()
blockchain.add_block(transactions)
