import serial
import time 
ser = serial.Serial('/dev/ttyUSB0',38400,timeout=1)
while True:
    ser.write("bed")
    print(ser.readline())
    time.sleep(0.5)
