import GPIOConfig
import RPi.GPIO as GPIO

received_pkt = "0000000000000"

motor_left_direction = int(received_pkt[:1])
motor_left_speed = int(received_pkt[1:3])
motor_right_direction = int(received_pkt[3:4])
motor_right_speed = int(received_pkt[4:6])
claw1_direction = int(received_pkt[6:7])
claw1_speed = int(received_pkt[7:9])
claw2_direction = int(received_pkt[9:10])
claw2_speed = int(received_pkt[10:12])
reset_driver = int(received_pkt[12:13])

motor_left_direction = 1
motor_right_direction = 0

motor_left_speed = 10
motor_right_speed = 10

#Configurando para ocultar mensagem de aviso
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


GPIO.output(GPIOConfig.MOTOR_RIGHT_EN, 1)
GPIO.output(GPIOConfig.MOTOR_RIGHT_INA, motor_right_direction)
GPIO.output(GPIOConfig.MOTOR_RIGHT_INB, not motor_right_direction)

GPIO.output(GPIOConfig.MOTOR_LEFT_EN, 1)
GPIO.output(GPIOConfig.MOTOR_LEFT_INA, motor_left_direction)
GPIO.output(GPIOConfig.MOTOR_LEFT_INB, not motor_left_direction)


print("motor_left_direction: "+ str(not motor_left_direction))

GPIO.output(GPIOConfig.MOTOR_CLAW_EN, GPIO.HIGH)
GPIO.output(GPIOConfig.MOTOR_CLAW_INA, claw1_direction)
GPIO.output(GPIOConfig.MOTOR_CLAW_INB, not claw1_direction)



motor_claw = GPIO.PWM(GPIOConfig.MOTOR_CLAW_PWM, 100)
motor_right = GPIO.PWM(GPIOConfig.MOTOR_RIGHT_PWM, 100)
motor_left = GPIO.PWM(GPIOConfig.MOTOR_LEFT_PWM, 100)

motor_right.start(motor_right_speed)
motor_left.start(motor_left_speed)
motor_claw.start(claw1_speed)
print(motor_right_speed)
print(motor_left_speed)

#GPIO.cleanup()

while True:
    direction = input("Command:")
    
    if direction == 'A':
        GPIO.output(GPIOConfig.MOTOR_LEFT_INA, 0)
        GPIO.output(GPIOConfig.MOTOR_LEFT_INB, 1)
        
        GPIO.output(GPIOConfig.MOTOR_RIGHT_INA, 0)
        GPIO.output(GPIOConfig.MOTOR_RIGHT_INB, 1)

        motor_right.start(50)
        motor_left.start(50)
    elif direction == 'B':
        GPIO.output(GPIOConfig.MOTOR_LEFT_INA, 1)
        GPIO.output(GPIOConfig.MOTOR_LEFT_INB, 0)
        
        GPIO.output(GPIOConfig.MOTOR_RIGHT_INA, 1)
        GPIO.output(GPIOConfig.MOTOR_RIGHT_INB, 0)

        motor_right.start(20)
        motor_left.start(20)
    elif direction == 'Q':
        GPIO.cleanup()
        
        
        


