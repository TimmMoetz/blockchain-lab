from network.node import P2PNode
import sys
from Crypto.PublicKey import RSA
from Crypto.Signature import *

if __name__ == "__main__":
    
    # start node
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
        node = P2PNode("127.0.0.1", port, port, max_connections=3)
        node.start_up(port)


    # generate keys
    key = RSA.generate(2048)
    private_key = key.export_key()
    with open("private_key.pem", "wb") as file:
        file.write(private_key)

    public_key = key.publickey().export_key()
    with open("public_key.pem", "wb") as file:
        file.write(public_key)
    
    decoded_public_key = public_key.decode('ASCII')
    print(decoded_public_key)


    possible_inputs = ['s', 't']
    user_input = ''
    while user_input not in possible_inputs:
        user_input = input("type 's' to stop the node or 't' to make a transaction \n")    
                         
        if user_input == 's':
            node.stop()
        elif user_input == 't':
            # validate transaction first... if valid:
            transaction = {'hash':'test'}
            msg = {'message':'prepare-to-validate','payload': transaction}
            node.send_to_nodes(msg)
            user_input = ''   
