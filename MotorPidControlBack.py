import time
import mpu
import GPIOConfig
import RPi.GPIO as GPIO

def MoveMotors(motor_right_speed, motor_left_speed):
    GPIO.output(GPIOConfig.MOTOR_RIGHT_EN, GPIO.HIGH)
    GPIO.output(GPIOConfig.MOTOR_RIGHT_INA, 0)
    GPIO.output(GPIOConfig.MOTOR_RIGHT_INB, 1)

    GPIO.output(GPIOConfig.MOTOR_LEFT_EN, GPIO.HIGH)
    GPIO.output(GPIOConfig.MOTOR_LEFT_INA, 0)
    GPIO.output(GPIOConfig.MOTOR_LEFT_INB, 1)

    GPIO.output(GPIOConfig.MOTOR_CLAW_EN, GPIO.LOW)
    GPIO.output(GPIOConfig.MOTOR_CLAW_INA, 0)
    GPIO.output(GPIOConfig.MOTOR_CLAW_INB, 0)

    motor_right.ChangeDutyCycle(motor_right_speed)
    motor_left.ChangeDutyCycle(motor_left_speed)
    motor_claw.ChangeDutyCycle(0)

kp = 2
kd = 0
ki = 0.001


setpoint = 100
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



presentTime2 = time.time()
while True:
    now = time.time()
    yaw, pitch, row = mpu.compFilter(0)
    if pastTime > 5:
        print("calibrated")
        break

    pastTime = now - presentTime2


while True:
    presentTime = time.time()
    pastTime = presentTime - lastTime

    ##Leitura do sensor ###
    yaw, pitch, row = mpu.compFilter(0)


    
    error = setpoint - pitch
    i_error += error * pastTime
    d_error = (error - lastError)/pastTime


    pid_value = kp*error + ki*i_error + kd*d_error
    speed_left = 80 + pid_value
    speed_right = 80 - pid_value
    if speed_left > 99:
        speed_left = 99
    elif speed_left <= 1:
        speed_left = 0
    if speed_right > 99:
        speed_right = 99
    elif speed_right <= 1:
        speed_right = 0


    
    print("\rerror: " + str(error) + "    Pid: " + str(pid_value))
    GPIO.output(GPIOConfig.MOTOR_RIGHT_EN, GPIO.HIGH)
    GPIO.output(GPIOConfig.MOTOR_RIGHT_INA, 0)
    GPIO.output(GPIOConfig.MOTOR_RIGHT_INB, 1)

    GPIO.output(GPIOConfig.MOTOR_LEFT_EN, GPIO.HIGH)
    GPIO.output(GPIOConfig.MOTOR_LEFT_INA, 0)
    GPIO.output(GPIOConfig.MOTOR_LEFT_INB, 1)

    GPIO.output(GPIOConfig.MOTOR_CLAW_EN, GPIO.HIGH)
    GPIO.output(GPIOConfig.MOTOR_CLAW_INA, 0)
    GPIO.output(GPIOConfig.MOTOR_CLAW_INB, 0)

    motor_right.ChangeDutyCycle(speed_right)
    motor_left.ChangeDutyCycle(speed_left)



    lastError = error
    lastTime = presentTime
