import sys
from p2pnetwork.node import Node

class P2PNode(Node):

    def __init__(self, host, port, id=None, callback=None, max_connections=0):
        super(P2PNode, self).__init__(host, port, id, callback, max_connections)
        self.fluester_post_requested = False

        print("MyPeer2PeerNode: Started")

    def outbound_node_connected(self, node):
        print("outbound_node_connected (" + self.id + "): " + node.id)
        
    def inbound_node_connected(self, node):
        print("inbound_node_connected: (" + self.id + "): " + node.id)

    def inbound_node_disconnected(self, node):
        print("inbound_node_disconnected: (" + self.id + "): " + node.id)

    def outbound_node_disconnected(self, node):
        print("outbound_node_disconnected: (" + self.id + "): " + node.id)

    def node_message(self, node, data):
        print("node_message (" + self.id + ") from " + node.id + ": " + data['message'] +" with payload: "+ str(data['payload']))

        if data['message'] == 'printConns':
            self.print_conns()
        
        if data['message'] == 'flüsterPost':
            if self.fluester_post_requested:
                print("Flüster-Post received: " + data['payload'])
                self.fluester_post_requested = False 
            else:
                for conn in self.all_nodes:
                    if conn.id != node.id:
                        print("relay Flüster-Post " + data['payload'] + " from Node " + self.id + " to Node " + conn.id)
                        self.send_to_node(conn , data)

        if data['message'] == 'getaddr':
            # sends host, port and id of his peers
            payload = []
            for conn in self.all_nodes:
                payload.append({'host': conn.host, 'port': conn.port,'id': conn.id})
            msg = {'message':'addr','payload':payload}
            self.send_to_node(node, msg)

        if data['message'] == 'addr':
            # connect to new peers...
            pass
        
    def node_disconnect_with_outbound_node(self, node):
        print("node wants to disconnect with oher outbound node: (" + self.id + "): " + node.id)
        
    def node_request_to_stop(self):
        print("node is requested to stop (" + self.id + "): ")

    def print_conns(self):
        for conn in self.nodes_outbound:
            print("out:")
            print(conn)
        for conn in self.nodes_inbound:
            print("in:")
            print(conn)

    def start_up(self):
    
        self.start()
        for port in sys.argv:
            if port != self.port and port != sys.argv[0]:
                self.connect_with_node('127.0.0.1', int(port))

        if len(sys.argv) > 3:
            self.send_to_nodes({'message':'printConns','payload':''})
            self.print_conns()

            payload = "moiiiiiin"
            print("Send Flüster-Post: " + payload + " from Node " + self.id + " to Node " + self.all_nodes[0].id)
            self.send_to_node(self.all_nodes[0], {'message': 'flüsterPost', 'payload': payload})
            self.fluester_post_requested = True

            #node.send_to_nodes({'message':'getaddr','payload':''})


if __name__ == "__main__":
    if len(sys.argv) > 1:
        ownPort = int(sys.argv[1])
        node = P2PNode("127.0.0.1", ownPort, ownPort)
        node.start_up()

        input = input("type 's' to stop the node:   ")
        if input == 's':
            node.stop()