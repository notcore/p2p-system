"""
This class represents an access server on the network. It's purpose
is to provide information about the network so that incoming clients know
who to connect to.

"""

import socket
import hashlib


class Server:

    def __init__(self, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("", port))
        self.peers = {}  # Keeps track of connected peers in format {ADDR_HASH:(ADDR_DATA)}
        self.port = port

    # Returns a string version of the peers dictionary without curly brackets
    def peers_to_str(self):
        peer_string = ""
        for k, v in self.peers.items():
            peer_string += "'" + k + "'" + ":" + str(v) + "|"
        return peer_string

    def add_peer(self, ip, port):
        addr_string = bytes(ip + str(port), "UTF-8")
        addr_hash = hashlib.md5(addr_string).hexdigest()
        self.peers.update({addr_hash: (ip, port)})

    def listen(self):
        print("Listening on port {0}".format(self.port))
        while True:
            addr = self.sock.recvfrom(1024)[1]
            print("Connection request from: {0} on port {1}".format(addr[0], addr[1]))
            self.sock.sendto(b'\xf3\xf3' + bytes(self.peers_to_str(), "UTF-8"), (addr[0], addr[1]))
            self.add_peer(addr[0], addr[1])


s = Server(5005)
s.listen()
