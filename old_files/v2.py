import select, socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)
server.bind(('192.168.0.11', 50002))
server.listen(5)

# TCP Keepalive Options
#server.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
#server.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 1)
#server.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 3)
#server.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)

inputs = [server]

print ("Listening on port 50000")

while True:
    readable, writable, exceptional = select.select(inputs, [], inputs)

    for s in readable:
        if s is server:
            connection, client_address = s.accept()
            print ("New client connected: %s" % (client_address,))

            connection.setblocking(0)
            inputs.append(connection)
        else:
            data = s.recv(1024)

            if data:
                print(data)
            else:
                print ("%s disconnected" % (s.getpeername(),))

                inputs.remove(s)
                s.close()

    for s in exceptional:
        print("Client at %s dropped out" % (s.getpeername(),))
        inputs.remove(s)
        s.close()