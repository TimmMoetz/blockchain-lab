import sys
import os
import json
from Crypto.PublicKey import RSA
from Crypto.Signature import *
from network.node import P2PNode
from network.conversations.transaction_validation import Transaction_Validation

if __name__ == "__main__":

    def base58(address_hex):
        alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        b58_string = ''
        # Get the number of leading zeros
        leading_zeros = len(address_hex) - len(address_hex.lstrip('0'))
        # Convert hex to decimal
        address_int = int(address_hex, 16)
        # Append digits to the start of string
        while address_int > 0:
            digit = address_int % 58
            digit_char = alphabet[digit]
            b58_string = digit_char + b58_string
            address_int //= 58
        # Add ‘1’ for each 2 leading zeros
        ones = leading_zeros // 2
        for one in range(ones):
            b58_string = '1' + b58_string
        return b58_string

    # start node
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
        node = P2PNode("127.0.0.1", port, port, max_connections=3)
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

            target = input("please enter the public key of the target you want to send coins: \n")
            amount = input("please enter the amount you want to send: \n")

            with open("db/keys/public_key.pem", "rb") as file:
                source = file.read()
            
            print(amount)
            print(source.hexdigest())
            target = input("please enter the public key of the target you want to send coins: \n")
            print(target)

            # validate transaction first... if valid:
            transaction = {'hash':'test'}

            validation = Transaction_Validation(node, transaction)
            node.conversations["transaction_validation"] = validation
            validation.send_prepare_to_validate()
            
            user_input = ''   
            
