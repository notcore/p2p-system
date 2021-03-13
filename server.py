import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", 5005))

connections = []
while True:
    while len(connections) < 2:
        data, addr = sock.recvfrom(1024)
        print('Connection request from: {0} on port {1}'.format(addr[0], addr[1]))
        connections.append((addr[0], str(addr[1])))

    a = connections.pop()
    b = connections.pop()
    print('Joining {0} and {1}'.format(a[0], b[0]))
    sock.sendto(bytes(",".join(b), "UTF-8"), (a[0], int(a[1])))
    sock.sendto(bytes(",".join(a), "UTF-8"), (b[0], int(b[1])))
