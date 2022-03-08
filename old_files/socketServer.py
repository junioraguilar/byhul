import socket
import time

#from GPIOControl import Move_Motors
#import GPIOControl



HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("10.160.23.190", 27166))
s.listen(5)

while True:
    # now our endpoint knows about the OTHER endpoint.
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")
    
    while True:
        received_pkt = clientsocket.recv(1024)
        received_pkt = received_pkt.decode()

        print("Payload Size: " + str(len(received_pkt)) + "  Payload: " + received_pkt)
        
        if not received_pkt:
            s.close()
            s.listen(5)
        
        
print("finalizando socket")
s.close()

    

    
