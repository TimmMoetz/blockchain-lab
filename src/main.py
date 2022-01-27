import sys
import os
from Crypto.PublicKey import RSA
from Crypto.Signature import *
from network.node import P2PNode
from network.conversations.transaction_validation import Transaction_Validation

if __name__ == "__main__":
    
    # start node
    if len(sys.argv) > 2:
        host = sys.argv[1]
        port = int(sys.argv[2])
        node = P2PNode(host, port, port, max_connections=3)
        node.start_up()
    else:
        print("specify the port as argument to start a node")


    if not os.path.exists('db/keys/private_key.pem') or not os.path.exists('db/keys/public_key.pem'):
        # generate keys
        key = RSA.generate(2048)
        private_key = key.export_key()
        with open("db/keys/private_key.pem", "wb") as file:
            file.write(private_key)

        public_key = key.publickey().export_key()
        with open("db/keys/public_key.pem", "wb") as file:
            file.write(public_key)
        
        print(public_key.decode('ASCII'))


    possible_inputs = ['s', 't']
    user_input = ''
    while user_input not in possible_inputs:
        user_input = input("type 's' to stop the node or 't' to make a transaction \n")    
                         
        if user_input == 's':
            node.stop()
        elif user_input == 't':
            # validate transaction first... if valid:
            transaction = {'hash':'test'}

            validation = Transaction_Validation(node, transaction)
            node.conversations["transaction_validation"] = validation
            validation.send_prepare_to_validate()
            
            user_input = ''   
