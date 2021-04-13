"""
This class represents a single client on the network.
Currently transitions to a chat application after successful connection.

Source for NAT Hole Punching Technique: https://bford.info/pub/net/p2pnat/
"""

import socket
import threading
from time import sleep
from ast import literal_eval


class Client:

    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.peers = {}
        self.ip = ip
        self.port = port

    def conn_request(self):
        data = b'\xf3\xf3'
        while data == b'\xf3\xf3':
            print("Sending connection request...")
            self.sock.sendto(b'', (self.ip, self.port))
            data = self.sock.recvfrom(1024)[0]
            sleep(5)
        self.peers = self.peers_to_dict(data)

    @staticmethod
    def peers_to_dict(peers_str):
        new_peers = {}
        peers_str = peers_str[2:-1].decode("UTF-8")
        peers_list = peers_str.split("|")
        for addr in peers_list:
            new_peers.update(literal_eval("{"+addr+"}"))
        return new_peers

    # Stops the connection from closing because of idling
    # Works by sending out a 2 byte-sized packet every 10 seconds
    def idle_packets(self):
        for addr in self.peers.values():
            self.sock.sendto(b'\xf1\xf1', (addr[0], addr[1]))

    def update_peers(self):
        self.sock.sendto(b'', (self.ip, self.port))

    def keep_alive(self):
        while True:
            self.update_peers()
            self.idle_packets()
            sleep(5)

    # Checks if message is functional
    def check_msg(self, msg):
        if msg == b'\xf1\xf1':  # idle message
            return False
        elif b'\xf3\xf3' in msg:  # peer update
            self.peers = self.peers_to_dict(msg)
            return False
        return True

    # Subroutine to catch messages from other clients
    def recv_messages(self):
        while True:
            received_msg, ip = self.sock.recvfrom(1024)
            if self.check_msg(received_msg):
                tag = '<{0}>'.format(ip[0])
                print(tag, received_msg.decode('UTF-8'))

    def start_chat(self):
        print("Connecting to network...")

        recv_thread = threading.Thread(target=self.recv_messages)
        keep_alive_thread = threading.Thread(target=self.keep_alive)
        recv_thread.start()
        keep_alive_thread.start()  # Does hole punching on first pass

        print("Connected to network. You can now chat.")
        while True:
            msg = input('')
            for addr in self.peers.values():
                self.sock.sendto(bytes(msg, 'UTF-8'), (addr[0], addr[1]))


c = Client("178.79.154.241", 5005)
c.conn_request()
c.start_chat()
