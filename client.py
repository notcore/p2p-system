import socket
import threading
# import atexit
from time import sleep


# Checks if message is functional
def check_msg(message):
    if message == b'\xf1\xf1':  # idle message
        return False
    elif message == b'\xf2\xf2':  # disconnect message
        print('User has disconnected')
        return False
    return True


# Subroutine to catch messages from other clients
def recv_messages(sc):
    while True:
        received_msg, ip = sc.recvfrom(1024)
        if check_msg(received_msg):
            tag = '<{0}>'.format(ip[0])
            print(tag, received_msg.decode('UTF-8'))


# Stops the connection from closing because of idling
# Works by sending out a 2 byte-sized packet every 10 seconds
def idle_packets(sc, cinfo):
    while True:
        sc.sendto(b'\xf1\xf1', (cinfo[0], cinfo[1]))
        sleep(10)


# Sends a notification stating the user has disconnected
def disconnect_send(sc, cinfo):
    print('Exiting')
    sc.sendto(b'\xf2\xf2', (cinfo[0], cinfo[1]))


# Send request to public server
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(b'', ('139.162.210.80', 5005))

# Decode peer info
data = sock.recvfrom(1024)[0]
data = data.decode('UTF-8').split(',')
conn_info = (data[0], int(data[1]))

# Send hole punching packet
print('Connecting to: {0} on port {1}'.format(conn_info[0], conn_info[1]))
sock.sendto(b'', (conn_info[0], conn_info[1]))
data = sock.recvfrom(1024)[0]

# atexit.register(disconnect_send, sock, conn_info)

recv_thread = threading.Thread(target=recv_messages, args=[sock])
idle_thread = threading.Thread(target=idle_packets, args=[sock, conn_info])
recv_thread.start()
idle_thread.start()

print('Talking with {0}'.format(conn_info[0]))
while True:
    msg = input('')
    sock.sendto(bytes(msg, 'UTF-8'), (conn_info[0], conn_info[1]))
