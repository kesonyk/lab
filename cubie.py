import time
import serial
import zerorpc

#configure the RPC Client
c=zerorpc.Client()
c.connect("tcp://127.0.0.1:4242")

#configure the serial connections,auto open the serialPort
ser=serial.Serial(
	port='/dev/ttyUSB0',
	baudrate=9600,
	parity=serial.PARITY_ODD,
	stopbits=serial.STOPBITS_TWO,
	bytesize=serial.SEVENBITS,
	timeout=1
)

def dataParse(dataPackage):
	src=dataPackage[4:12]
	data=dataPackage[12:-2]
	return src,data

def readData(serPort,debug=False):
	string=serPort.read(50)
	
	if string:
		ret=string.split('\n')
		logInfo=ret[0]
		dataPackage=ret[1]
		if debug:
			print "logInfo: %s"%logInfo
			print "dataPack: %s"%dataPackage
		#parse the string,get the src address and data
		src,data=dataParse(dataPackage)
		state=True
	else:
		state=False
		src=""
		data=""
	return state,src,data		
	

if (ser.isOpen()==False):
	ser.open()
else:
	print "Open the port successed!"
	while 1:
		state,src,data=readData(ser)
		if state:
			print src,data
			#confirm the car
			if(c.carConfirm(src)):	
				print "Confirmed"
				c.dataUpload('01',src,data)
			else:
				print "Not Confirmed"	
			




