import hashlib
from block import Block, Transaction

dig = hashlib.sha256(b"hello world").hexdigest()
print("Digest=" + str(dig))
print("Digest (binary)=" + bin(int(dig, 16)))

t1 = Transaction("Peter", "Stephan", 100.0)
t2 = Transaction("Stephan", "Peter", 5.0)
b1 = Block(pred=None)
b1.add_transaction(t1)
b1.add_transaction(t2)
b1_hash = b1.hash()
b2 = Block(pred=b1_hash)
b2_hash = b2.hash()

b1.write_to_file("./blocks")
b2.write_to_file("./blocks")
