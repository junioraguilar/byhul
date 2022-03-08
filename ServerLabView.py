from distutils.fancy_getopt import wrap_text
import os
import select
import socket
import time
import GPIOConfig
import RPi.GPIO as GPIO


host = '192.168.4.4'
port = 27161

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(5)
server.settimeout(5)

inputs = [server]
lastread = {}
print ("Listening on port ", port)


while True:
    readable, writable, exceptional = select.select(inputs, [], inputs, 0.1)
    now = time.time()
    for s in readable:
        if s is server:
            client, address = server.accept()
            print ("New client connected: %s" % (address,))
            client.settimeout(1)
            inputs.append(client)
        else:       
            try: data = s.recv(1024)
            except ConnectionResetError:
                data = 0
            if data:
                lastread[s] = now
                if len(data) > 2:
                    data = data[2:]
                    data = data.decode()
                    print(data)
                    post = "**001212851473180000"
                    post2 = "**000310123"
                    s.send(post.encode())
                    s.send(post2.encode())
                    
            else:
                print ("disconnected")
                inputs.remove(s)
                closed.append(s)
                s.close()
                del lastread[s]
            
    closed = []
    for s in lastread:
        if s not in readable and now - lastread[s] > 2:
            print("timeout socket: " + str(now - lastread[s]))
            s.close()
            closed.append(s)
            inputs.remove(s)
            
    for s in closed:
        del lastread[s]

