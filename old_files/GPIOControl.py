import RPi.GPIO as GPIO
import GPIOConfig
import time


def Move_Motors(control_packet):
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


    GPIO.output(GPIOConfig.MOTOR_RIGHT_EN, GPIO.HIGH)
    GPIO.output(GPIOConfig.MOTOR_RIGHT_INA, motor_right_direction)
    GPIO.output(GPIOConfig.MOTOR_RIGHT_INB, not motor_right_direction)

    GPIO.output(GPIOConfig.MOTOR_LEFT_EN, GPIO.HIGH)
    GPIO.output(GPIOConfig.MOTOR_LEFT_INA, motor_left_direction)
    GPIO.output(GPIOConfig.MOTOR_LEFT_INB, not motor_left_direction)

    GPIO.output(GPIOConfig.MOTOR_CLAW_EN, GPIO.HIGH)
    GPIO.output(GPIOConfig.MOTOR_CLAW_INA, claw1_direction)
    GPIO.output(GPIOConfig.MOTOR_CLAW_INB, not claw1_direction)
    


    motor_claw = GPIO.PWM(GPIOConfig.MOTOR_CLAW_PWM, 100)
    motor_right = GPIO.PWM(GPIOConfig.MOTOR_RIGHT_PWM, 100)
    motor_left = GPIO.PWM(GPIOConfig.MOTOR_LEFT_PWM, 100)

    print("Motor left: " + str(motor_left_speed))
    print("Motor Right: " + str(motor_right_speed))
    
    motor_right.start(motor_right_speed)
    motor_left.start(motor_left_speed)
    motor_claw.start(claw1_speed)
    
    motor_right.ChangeDutyCycle(motor_right_speed)
    motor_left.ChangeDutyCycle(motor_left_speed)
    time.sleep(1)
    
    if control_packet == "0000000000000":
        print("cleanup")
        GPIO.cleanup()
       





def Sensor_GetDistance():
    file = open("SensorData.txt", "r")
    sensor_value = file.read()
    file.close()
    return sensor_value

def Clear_Gpio():
    GPIO.cleanup()