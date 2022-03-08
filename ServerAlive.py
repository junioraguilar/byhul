from distutils.fancy_getopt import wrap_text
import os
import select
import socket
import time
import GPIOConfig
import RPi.GPIO as GPIO



def move_motors(packet_control):

    # eneable_motors = False

    #motor_right_direction = 0
    #motor_left_direction = 0
    #motor_claw_direction = 0
    
    #motor_right_speed = 0
    #motor_left_speed = 0
    #motor_claw_speed = 0
    
    #Comando para subir o robo
    if packet_control == 'u':
        
        eneable_motors = True

        motor_right_direction = 0
        motor_left_direction = 0
        motor_claw_direction = 0
        
        motor_right_speed = 80
        motor_left_speed = 80
        motor_claw_speed = 0
    
    #Comando para descer o robo
    elif packet_control == 'd':

        eneable_motors = True
        
        motor_right_direction = 1
        motor_left_direction = 1
        motor_claw_direction = 0
        
        motor_right_speed = 20
        motor_left_speed = 20
        motor_claw_speed = 0

    #comando para subir a esquerda   
    elif packet_control == 'l':
        
        eneable_motors = True
        
        motor_right_direction = 0
        motor_left_direction = 0
        motor_claw_direction = 0
        
        motor_right_speed = 20
        motor_left_speed = 99
        motor_claw_speed = 0
    
    #Comando para subir a direita
    elif packet_control == 'r':

        eneable_motors = True
        
        motor_right_direction = 0
        motor_left_direction = 1
        motor_claw_direction = 0
        
        motor_right_speed = 80
        motor_left_speed = 40
        motor_claw_speed = 0
        
    #comando para descer a lanca
    elif packet_control == 'b':
        eneable_motors = True
        
        motor_right_direction = 0
        motor_left_direction = 0
        motor_claw_direction = 0
        
        motor_right_speed = 0
        motor_left_speed = 0
        motor_claw_speed = 20
    
    #comando para subir a lanca    
    elif packet_control == 'c':
        
        eneable_motors = True

        motor_right_direction = 0
        motor_left_direction = 0
        motor_claw_direction = 1
        
        motor_right_speed = 0
        motor_left_speed = 0
        motor_claw_speed = 5
    
    else:
        
        
        eneable_motors = True
        
        motor_right_direction = 0
        motor_left_direction = 0
        motor_claw_direction = 0
        
        motor_right_speed = 0
        motor_left_speed = 0
        motor_claw_speed = 0       
        
    GPIO.output(GPIOConfig.MOTOR_CLAW_EN, eneable_motors)
    GPIO.output(GPIOConfig.MOTOR_RIGHT_EN, GPIO.HIGH)
    GPIO.output(GPIOConfig.MOTOR_RIGHT_INA, motor_right_direction)
    GPIO.output(GPIOConfig.MOTOR_RIGHT_INB, not motor_right_direction)

    GPIO.output(GPIOConfig.MOTOR_LEFT_EN, GPIO.HIGH)
    GPIO.output(GPIOConfig.MOTOR_LEFT_INA, motor_left_direction)
    GPIO.output(GPIOConfig.MOTOR_LEFT_INB, not motor_left_direction)

    GPIO.output(GPIOConfig.MOTOR_CLAW_EN, GPIO.HIGH)
    GPIO.output(GPIOConfig.MOTOR_CLAW_INA, motor_claw_direction)
    GPIO.output(GPIOConfig.MOTOR_CLAW_INB, not motor_claw_direction)

    motor_right.ChangeDutyCycle(motor_right_speed)
    motor_left.ChangeDutyCycle(motor_left_speed)
    motor_claw.ChangeDutyCycle(motor_claw_speed)
    

#os.system("/home/pi/RPi_Cam_Web_Interface/start.sh")

host = 'raspberrypi.local'
port = 1237

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

GPIO.setup(GPIOConfig.MOTOR_RIGHT_PWM, GPIO.OUT)
GPIO.setup(GPIOConfig.MOTOR_RIGHT_INA, GPIO.OUT)
GPIO.setup(GPIOConfig.MOTOR_RIGHT_INB, GPIO.OUT)
GPIO.setup(GPIOConfig.MOTOR_RIGHT_EN, GPIO.OUT)


GPIO.setup(GPIOConfig.MOTOR_LEFT_PWM, GPIO.OUT)
GPIO.setup(GPIOConfig.MOTOR_LEFT_INA, GPIO.OUT)
GPIO.setup(GPIOConfig.MOTOR_LEFT_INB, GPIO.OUT)
GPIO.setup(GPIOConfig.MOTOR_LEFT_EN, GPIO.OUT)

GPIO.setup(GPIOConfig.MOTOR_CLAW_PWM, GPIO.OUT)
GPIO.setup(GPIOConfig.MOTOR_CLAW_INA, GPIO.OUT)
GPIO.setup(GPIOConfig.MOTOR_CLAW_INB, GPIO.OUT)
GPIO.setup(GPIOConfig.MOTOR_CLAW_EN, GPIO.OUT)

GPIO.setup(GPIOConfig.TILT_SENSOR_INPUT, GPIO.IN)


GPIO.output(GPIOConfig.MOTOR_RIGHT_EN, GPIO.HIGH)
GPIO.output(GPIOConfig.MOTOR_RIGHT_INA, 0)
GPIO.output(GPIOConfig.MOTOR_RIGHT_INB, 0)

GPIO.output(GPIOConfig.MOTOR_LEFT_EN, GPIO.HIGH)
GPIO.output(GPIOConfig.MOTOR_LEFT_INA, 0)
GPIO.output(GPIOConfig.MOTOR_LEFT_INB, 0)

GPIO.output(GPIOConfig.MOTOR_CLAW_EN, GPIO.HIGH)
GPIO.output(GPIOConfig.MOTOR_CLAW_INA, 0)
GPIO.output(GPIOConfig.MOTOR_CLAW_INB, 0)



motor_claw = GPIO.PWM(GPIOConfig.MOTOR_CLAW_PWM, 100)
motor_right = GPIO.PWM(GPIOConfig.MOTOR_RIGHT_PWM, 100)
motor_left = GPIO.PWM(GPIOConfig.MOTOR_LEFT_PWM, 100)

motor_claw.start(0)
motor_right.start(0)
motor_left.start(0)

def read_status_server():
    file = open("/home/pi/Desktop/byhull/status.txt", "r")
    flag = file.readline()
    file.close()
    return flag


while True:
    readable, writable, exceptional = select.select(inputs, [], inputs, 5)
    if read_status_server() == '0' or  read_status_server() == '':
        move_motors("p")  
    for s in readable:
        if s is server:
            client, address = server.accept()
            print ("New client connected: %s" % (address,))
            client.settimeout(1)
            inputs.append(client)
            motor_left.ChangeDutyCycle(0)
            motor_right.ChangeDutyCycle(0)
            motor_claw.ChangeDutyCycle(0)
        else:
            try: data = s.recv(1024)
            except ConnectionResetError:
                data = 0
            if data:
                if len(data) > 2:
                    data = data[2:]
                    data = data.decode()
                    if data[0] == '#' and data[-1] == '!':
                        print(data[1:-1])
                        move_motors(data[1:-1])
            else:
                print ("Disconnected")
                inputs.remove(s)
                s.close()
                move_motors("p")