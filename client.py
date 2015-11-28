import zerorpc

c=zerorpc.Client()
c.connect("tcp://127.0.0.1:4242")

if (c.carConfirm("00000001")):
	print "Confirmed"
	c.dataUpload('01','00000001','kesonYang')
	c.dataSelect('01')
else:
	print "not Confirmed"
