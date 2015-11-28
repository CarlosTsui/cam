import serial
import time
ser = serial.Serial('COM9', 9600)
#ser.open()

while 1:
	ser.write("saaaaaaaaaaaaaaaaaa")
	time.sleep(1)
	ser.write("sdddddddddddddddddd")

#ser.close()
