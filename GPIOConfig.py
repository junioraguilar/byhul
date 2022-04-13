import RPi.GPIO as gpio
import time

#Constantes dos pinos dos motores
MOTOR_RIGHT_PWM = 19 
MOTOR_RIGHT_INA = 20 
MOTOR_RIGHT_INB = 26 
MOTOR_RIGHT_EN =  0 

MOTOR_LEFT_PWM = 13
MOTOR_LEFT_INA = 5 
MOTOR_LEFT_INB = 6 
MOTOR_LEFT_EN =  0 

MOTOR_CLAW_PWM = 12
MOTOR_CLAW_INA = 1
MOTOR_CLAW_INB = 21
MOTOR_CLAW_EN =  0 

TILT_SENSOR_INPUT = 4

def GPIO_cleanup():
    gpio.cleanup()


