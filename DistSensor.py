import serial
import time


lendo = True
def Stop_Read():
    lendo = False

def Distance_data():
    ser = serial.Serial("/dev/ttyS0", 9600)
    received_data_acum = 0
    for a in range(0,15):
        received_data = ser.read(5)
        received_data = received_data.decode()
        received_data = int(received_data[1:4])
        received_data_acum += received_data
    try:
        media_distance_data = int(int(received_data_acum)/15)
        print(media_distance_data)
        file = open("/home/pi/Desktop/byhull/SensorData.txt", "w")
        file.write(str(media_distance_data))
        file.close()
        ser.close()
        return media_distance_data
    except:
        ser.close()
        pass
    

while lendo:
    Distance_data()