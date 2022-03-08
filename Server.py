from distutils.fancy_getopt import wrap_text
import os
import select
import socket
import time
import GPIOConfig
import RPi.GPIO as GPIO

os.system("/home/pi/RPi_Cam_Web_Interface/start.sh")

host = 'raspberrypi.local'
port = 1235

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(5)
server.settimeout(5)

inputs = [server]
lastread = {}
print ("Listening on port ", port)

GPIO.setwarnings(False)
#Configurando GPIO
GPIO.setmode(GPIO.BCM)

def server_status_offline():
    flag = 0
    file = open("/home/pi/Desktop/byhull/status.txt", "w")
    file.write(str(flag))
    file.close()

def server_status_online():
    flag = 1
    file = open("/home/pi/Desktop/byhull/status.txt", "w")
    file.write(str(flag))
    file.close()


while True:
    readable, writable, exceptional = select.select(inputs, [], inputs, 0.1)
    now = time.time()
    for s in readable:
        if s is server:
            client, address = server.accept()
            print ("New client connected: %s" % (address,))
            client.settimeout(1)
            inputs.append(client)
            server_status_online()
        else:       
            try: data = s.recv(1024)
            except ConnectionResetError:
                data = 0
            if data:
                server_status_online()
                file = open("/home/pi/Desktop/byhull/SensorData.txt", "r")
                distValue = file.readline()
                distValue = '#'+ distValue + '!'
                s.send(distValue.encode())
                print('Send: ' + str(distValue.encode()))
                file.close()
                lastread[s] = now
                if len(data) > 2:
                    data = data[2:]
                    data = data.decode()
                    print('Received: ' + data)
            else:
                print ("disconnected")
                server_status_offline()
                inputs.remove(s)
                closed.append(s)
                s.close()
                del lastread[s]
    closed = []
    for s in lastread:
        if s not in readable and now - lastread[s] > 2:
            print("timeout socket: ")
            server_status_offline()
            s.close()
            closed.append(s)
            inputs.remove(s)
            
    for s in closed:
        try:
            del lastread[s]
        except:
            pass