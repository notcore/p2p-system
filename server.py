import socket


class Server:

    def __init__(self, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("", port))
        self.peers = {}  # Keeps track of connected peers in format {IP:PORT}

    # Returns a string version of the peers dictionary without curly brackets
    def peers_to_str(self):
        return str(self.peers)[1:-1]

    def listen(self):
        while True:
            addr = self.sock.recvfrom(1024)[1]
            print("Connection request from: {0} on port {1}".format(addr[0], addr[1]))
            if addr[0] in self.peers:
                del self.peers[addr[0]]
            self.sock.sendto(b'\xf3\xf3' + bytes(self.peers_to_str(), "UTF-8"), (addr[0], addr[1]))
            self.peers[addr[0]] = addr[1]


s = Server(5005)
s.listen()
