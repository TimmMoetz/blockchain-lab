import time
import json
import socket
from p2pnetwork.node import Node
from .bo.messages.prepare_to_validate import Prepare_to_validate
from .conversations.transaction_validation import Transaction_Validation
from .conversations.initial_peer_discovery import Initial_Peer_Discovery

class P2PNode(Node):

    def __init__(self, host, port, id=None, callback=None, max_connections=0):
        super(P2PNode, self).__init__(host, port, id, callback, max_connections)
        self.genesis_host = "192.168.0.89"
        self.genesis_port = 80
        self.potential_peers = [self.genesis_host + str(self.genesis_port)]
        self.conversations = {}
        self.debug = False

        print("MyPeer2PeerNode: Started")

    def outbound_node_connected(self, node):
        print("outbound_node_connected (" + self.id + "): " + node.id)

    def inbound_node_connected(self, node):
        print("inbound_node_connected: (" + self.id + "): " + node.id)

        # When the maximum connections is reached, it sends host and port of his peers and disconnects the connection 
        if len(self.nodes_inbound) > self.max_connections:
            peer_discovery = Initial_Peer_Discovery(self)           
            peer_discovery.send_addr(node)

    def inbound_node_disconnected(self, node):
        print("inbound_node_disconnected: (" + self.id + "): " + node.id)
        self.print_conns()

    def outbound_node_disconnected(self, node):
        print("outbound_node_disconnected: (" + self.id + "): " + node.id)
        self.print_conns()

    def node_message(self, sender_node_conn, message):
        print("node_message (" + self.id + ") from " + sender_node_conn.id + ": " + message['name'] +" with payload: "+ str(message))

        if message['name'] == 'addr':
            # addr is received from nodes that want to disconnect, the payload contains addresses from potential peers
            peer_discovery = Initial_Peer_Discovery(self)           
            peer_discovery.addr_recieved(sender_node_conn, message) 

        if message["name"] == 'prepare-to-validate':   
            msg_in = Prepare_to_validate.from_dict(message)

            validation = Transaction_Validation(self, msg_in.get_transaction())
            self.conversations["transaction_validation"] = validation
            validation.prepare_to_validate_recieved(sender_node_conn)
        
        if message['name'] == 'vote':
            validation = self.conversations["transaction_validation"]
            validation.vote_recieved(sender_node_conn, message)

        if message['name'] == 'global-decision': 
            validation = self.conversations["transaction_validation"]
            validation.global_decision_recieved(message)


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
        print("---")

    def connect_with_node(self, host, port, reconnect=False):
        """ Make a connection with another node that is running on host with port. When the connection is made, 
            an event is triggered outbound_node_connected. When the connection is made with the node, it exchanges
            the id's of the node. First we send our id and then we receive the id of the node we are connected to.
            When the connection is made the method outbound_node_connected is invoked. If reconnect is True, the
            node will try to reconnect to the code whenever the node connection was closed."""

        if host == self.host and port == self.port:
            print("connect_with_node: Cannot connect with yourself!!")
            return False

        # Check if node is already connected with this node!
        for node in self.nodes_outbound:
            if node.host == host and node.port == port:
                print("connect_with_node: Already connected with this node (" + node.id + ").")
                return True

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.debug_print("connecting to %s port %s" % (host, port))
            sock.connect((host, port))

            # Basic information exchange (not secure) of the nodes!
            data = {'id': self.id, 'port': self.port}
            msg = json.dumps(data)
            sock.send(msg.encode('utf-8'))  # Send my id and port to the connected node
            connected_node_id = sock.recv(4096).decode('utf-8') # When a node is connected, it sends it id!

            # Fix bug: Cannot connect with nodes that are already connected with us!
            for node in self.nodes_inbound:
                if node.host == host and node.id == connected_node_id:
                    print("connect_with_node: This node (" + node.id + ") is already connected with us.")
                    return True

            thread_client = self.create_new_connection(sock, connected_node_id, host, port)
            thread_client.start()

            self.nodes_outbound.append(thread_client)
            self.outbound_node_connected(thread_client)

            # If reconnection to this host is required, it will be added to the list!
            if reconnect:
                self.debug_print("connect_with_node: Reconnection check is enabled on node " + host + ":" + str(port))
                self.reconnect_to_nodes.append({
                    "host": host, "port": port, "tries": 0
                })

        except Exception as e:
            self.debug_print("TcpServer.connect_with_node: Could not connect with node. (" + str(e) + ")")

    def run(self):
        """The main loop of the thread that deals with connections from other nodes on the network. When a
           node is connected it will exchange the node id's. First we receive the id of the connected node
           and secondly we will send our node id to the connected node. When connected the method
           inbound_node_connected is invoked."""
        while not self.terminate_flag.is_set():  # Check whether the thread needs to be closed
            try:
                self.debug_print("Node: Wait for incoming connection")
                connection, client_address = self.sock.accept()

                self.debug_print("Total inbound connections:" + str(len(self.nodes_inbound)))
                
                # Basic information exchange (not secure) of the id's of the nodes!
                data = connection.recv(4096).decode('utf-8')
                connected_node = json.loads(data)  # When a node is connected, it sends its id and port
                connection.send(self.id.encode('utf-8'))  # Send my id to the connected node!

                thread_client = self.create_new_connection(connection, connected_node["id"], client_address[0], connected_node["port"])
                thread_client.start()

                self.nodes_inbound.append(thread_client)
                self.inbound_node_connected(thread_client)
            
            except socket.timeout:
                self.debug_print('Node: Connection timeout!')

            except Exception as e:
                raise e

            self.reconnect_nodes()

            time.sleep(0.01)

        print("Node stopping...")
        for t in self.nodes_inbound:
            t.stop()

        for t in self.nodes_outbound:
            t.stop()

        time.sleep(1)

        for t in self.nodes_inbound:
            t.join()

        for t in self.nodes_outbound:
            t.join()

        self.sock.settimeout(None)   
        self.sock.close()
        print("Node stopped")


    def start_up(self):
    
        self.start()
        if self.host != self.genesis_host:
            self.connect_with_node(self.genesis_host, self.genesis_port)
