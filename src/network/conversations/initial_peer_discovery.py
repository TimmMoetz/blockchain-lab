from ..bo.peer import Peer
from ..bo.messages.addr import Addr

class Initial_Peer_Discovery():
    def __init__(self, node) -> None:
        self.node = node

    # node that refuses connection
    def send_addr(self, node_connection):
        peers = []
        for conn in self.node.nodes_inbound:
            if conn.port != node_connection.port:
                peer = Peer(conn.host, conn.port)
                peers.append(peer)
        
        msg = Addr(peers)
        self.node.send_to_node(node_connection, msg.to_dict())
        
        node_connection.stop()   # stop connection

    # node that searches peer
    def addr_recieved(self, sender_node_conn, message):
        msg_in = Addr.from_dict(message)

        self.node.disconnect_with_node(sender_node_conn)
        
        peer_to_remove = None
        for peer in self.node.potential_peers:
            if peer.get_host() == sender_node_conn.host:
                peer_to_remove = peer
                print(peer_to_remove)
        self.node.potential_peers.remove(peer_to_remove)

        peer: Peer
        for peer in msg_in.get_peers():
            self.node.potential_peers.append(peer)

        self.node.connect_with_node(self.node.potential_peers[0].get_host(), self.node.potential_peers[0].get_port())
        print(self.node.potential_peers)
