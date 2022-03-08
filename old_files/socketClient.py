import socket

HEADERSIZE = 10

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.connect(("192.168.0.78", 27166))


while True:
    msg = input("Digite a msg de envio: ")
    tcp.send(msg.encode()) 