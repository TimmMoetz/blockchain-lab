import sys
import os
from Crypto.PublicKey import RSA
from Crypto.Signature import *
from network.node import P2PNode
from network.conversations.transaction_validation import Transaction_Validation
from network.conversations.block_download import Block_download

if __name__ == "__main__":

    # start node
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
        node = P2PNode("127.0.0.1", port, port, max_connections=3)
        node.start_up()



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


        possible_inputs = ['s', 'v']
        user_input = ''
        while user_input not in possible_inputs:
            user_input = input("type 's' to stop the node or 'v' to validate a transaction "
                               "or 'd' to download new blocks from a peer \n")

            if user_input == 's':
                node.stop()

            elif user_input == 'v':
                # validate transaction first... if valid:
                transaction = {'hash':'test'}

                validation = Transaction_Validation(node, transaction)
                node.conversations["transaction_validation"] = validation
                validation.send_prepare_to_validate()

                user_input = ''

            elif user_input == 'd':
                block_download = Block_download(node)
                block_download.get_blocks(node.nodes_outbound[0])

                user_input = ''
    else:
        print("specify the port as argument to start a node")