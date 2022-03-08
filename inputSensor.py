import GPIOConfig
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(4, GPIO.IN)

while True:
    if(GPIO.input(4) == 0):
        print("0")
    else:
        print("1")
       