import time
import serial

#configure the serial connections auto open the serialPort
ser=serial.Serial(
	port='/dev/ttyUSB0',
	baudrate=9600,
	parity=serial.PARITY_ODD,
	stopbits=serial.STOPBITS_TWO,
	bytesize=serial.SEVENBITS,
	timeout=5
)


ser.write("V DEBUG ========\nM01200000001KESONfg\n")
