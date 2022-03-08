import select, socket
import GPIOConfig
import time
import RPi.GPIO as GPIO

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)
server.bind(('192.168.0.3', 27166))
server.listen(5)

# TCP Keepalive Options
#server.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
#server.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 1)
#server.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 3)
#server.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)

inputs = [server]

print ("Listening on port")


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

while True:
    readable, writable, exceptional = select.select(inputs, [], inputs)

    for s in readable:
        if s is server:
            connection, client_address = s.accept()
            print ("New client connected: %s" % (client_address,))

            connection.setblocking(0)
            inputs.append(connection)
            #Configurando para ocultar mensagem de aviso
            
            motor_left.ChangeDutyCycle(0)
            motor_right.ChangeDutyCycle(0)
            motor_claw.ChangeDutyCycle(0)
            
            
        else:
            data = s.recv(1024)
            print(len(data))
            if data and len(data) == 15:
                ########################
                data = data[2:]
                control_packet = data
                motor_left_direction = int(control_packet[:1])
                motor_left_speed = int(control_packet[1:3])
                motor_right_direction = int(control_packet[3:4])
                motor_right_speed = int(control_packet[4:6])
                claw1_direction = int(control_packet[6:7])
                claw1_speed = int(control_packet[7:9])
                claw2_direction = int(control_packet[9:10])
                claw2_speed = int(control_packet[10:12])
                reset_driver = int(control_packet[12:13])

                print(motor_left_direction, motor_left_speed, motor_right_direction, motor_right_speed, claw1_direction, claw1_speed,claw2_direction, claw2_speed, reset_driver)
                
                
                GPIO.output(GPIOConfig.MOTOR_RIGHT_EN, GPIO.HIGH)
                GPIO.output(GPIOConfig.MOTOR_RIGHT_INA, motor_right_direction)
                GPIO.output(GPIOConfig.MOTOR_RIGHT_INB, not motor_right_direction)

                GPIO.output(GPIOConfig.MOTOR_LEFT_EN, GPIO.HIGH)
                GPIO.output(GPIOConfig.MOTOR_LEFT_INA, motor_left_direction)
                GPIO.output(GPIOConfig.MOTOR_LEFT_INB, not motor_left_direction)

                GPIO.output(GPIOConfig.MOTOR_CLAW_EN, GPIO.HIGH)
                GPIO.output(GPIOConfig.MOTOR_CLAW_INA, claw1_direction)
                GPIO.output(GPIOConfig.MOTOR_CLAW_INB, not claw1_direction)

                motor_right.ChangeDutyCycle(motor_right_speed)
                motor_left.ChangeDutyCycle(motor_left_speed)
                motor_claw.ChangeDutyCycle(claw1_speed)
                
                                
            else:
                print ("%s disconnected" % (s.getpeername(),))

                inputs.remove(s)
                s.close()
                ini = time.time()
                end = time.time()
                while True:
                    end = time.time()
                    if end - ini > 2:
                        #motor_claw.stop()
                        #motor_right.stop()
                        #motor_left.stop()
                        motor_right.ChangeDutyCycle(0)
                        motor_left.ChangeDutyCycle(0)
                        motor_claw.ChangeDutyCycle(0)
                        GPIO.output(GPIOConfig.MOTOR_CLAW_EN, GPIO.LOW)
                        #GPIO.cleanup()
                        print("Timed out")
                        break
                
                

    for s in exceptional:
        print("Client at %s dropped out" % (s.getpeername(),))
        inputs.remove(s)
        s.close()