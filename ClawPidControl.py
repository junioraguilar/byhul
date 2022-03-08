import time
import mpu
import GPIOConfig
import RPi.GPIO as GPIO

def MoveMotors(motor_claw_speed, motor_claw_direction):
    GPIO.output(GPIOConfig.MOTOR_CLAW_EN, GPIO.LOW)
    GPIO.output(GPIOConfig.MOTOR_CLAW_INA, 1)
    GPIO.output(GPIOConfig.MOTOR_CLAW_INB, 0)

    motor_right.ChangeDutyCycle(motor_right_speed)
    motor_left.ChangeDutyCycle(motor_left_speed)
    motor_claw.ChangeDutyCycle(0)

kp = 2
kd = 0
ki = 0.001


setpoint = 85
i_error = 0
d_error = 0


presentTime = 0
pastTime = 0
lastTime = 0

lastError = 0

mpu = mpu.MPU(250, 2, 0.98)
mpu.setUp()
mpu.calibrateGyro(500)
yaw = 0

lastTime = time.time()


GPIO.setwarnings(False)
#Configurando GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setup(GPIOConfig.MOTOR_CLAW_PWM, GPIO.OUT)
GPIO.setup(GPIOConfig.MOTOR_CLAW_INA, GPIO.OUT)
GPIO.setup(GPIOConfig.MOTOR_CLAW_INB, GPIO.OUT)
GPIO.setup(GPIOConfig.MOTOR_CLAW_EN, GPIO.OUT)

GPIO.output(GPIOConfig.MOTOR_CLAW_EN, GPIO.HIGH)
GPIO.output(GPIOConfig.MOTOR_CLAW_INA, 0)
GPIO.output(GPIOConfig.MOTOR_CLAW_INB, 1)



motor_claw = GPIO.PWM(GPIOConfig.MOTOR_CLAW_PWM, 100)

motor_claw.start(0)


i = 0


presentTime2 = time.time()
while True:
    now = time.time()
    if pastTime > 5:
        break
        print("calibrating")
    pastTime = now - presentTime2

    
while True:
    presentTime = time.time()
    pastTime = presentTime - lastTime        

    ##Leitura do sensor ###
    yaw, pitch = mpu.compFilter(0)


    
    error = setpoint - pitch
    i_error += error * pastTime
    d_error = (error - lastError)/pastTime


    pid_value = kp*error + ki*i_error + kd*d_error
    speed_claw = 10 + pid_value

    if speed_claw > 99:
        speed_claw = 99
    elif speed_claw <= 1:
        speed_claw = 0


    print("\rerror: " + str(error) + "    Pid: " + str(pid_value))

    GPIO.output(GPIOConfig.MOTOR_CLAW_EN, GPIO.HIGH)
    GPIO.output(GPIOConfig.MOTOR_CLAW_INA, 0)
    GPIO.output(GPIOConfig.MOTOR_CLAW_INB, 1)
    motor_claw.ChangeDutyCycle(speed_claw)

    if error < 2 and error > -2:
        i+=1
        if(i > 20):
            motor_claw.stop()
            GPIO.cleanup()
            exit()



    lastError = error
    lastTime = presentTime





