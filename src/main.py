from network.node import P2PNode
import sys
import os
from Crypto.PublicKey import RSA
from Crypto.Signature import *
from network.bo.messages.prepare_to_validate import Prepare_to_validate

if __name__ == "__main__":
    
    # start node
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
        node = P2PNode("127.0.0.1", port, port, max_connections=3)
        node.start_up()
    else:
        print("specify the port as argument to start a node")


    if not os.path.exists('./keys/private_key.pem') or not os.path.exists('./keys/public_key.pem'):
        # generate keys
        key = RSA.generate(2048)
        private_key = key.export_key()
        with open("keys/private_key.pem", "wb") as file:
            file.write(private_key)

        public_key = key.publickey().export_key()
        with open("keys/public_key.pem", "wb") as file:
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
            msg = Prepare_to_validate(transaction)
            node.send_to_nodes(msg.to_dict()) 
            user_input = ''   
