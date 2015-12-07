import zerorpc
import sqlite3



conn=sqlite3.connect('center.db')
conn.text_factory=str
"""
 RPC Server Operation
"""
class CenterRPC(object):

	def __init__(self):
		#self.conn=sqlite3.connect('center.db')
		conn.execute('''CREATE TABLE DATABASE
					( GATEID TEXT  NOT NULL,
					  CARID  TEXT  NOT NULL,
					  DATA   TEXT  NOT NULL,
					  STATE  INT   NOT NULL)''')
		print "Table created successfully"

		
		conn.execute("INSERT INTO DATABASE (GATEID,CARID,DATA,STATE)\
			VALUES ('01','fffffffe','',0)")


		cursor=conn.execute("SELECT * from DATABASE")
		for row in cursor:
			print type(row)
			print row

	
	def dataSelect(self,gateId):
		sql="SELECT * from DATABASE WHERE GATEID="+"gateId"
		print sql

		cursor=conn.execute(sql)
		ret=[]
		for row in cursor:
			print row
			ret.append(row)
		return ret
	
	
	def carConfirm(self,carId):
		
		cursor=conn.execute("SELECT carId from DATABASE")
		for row in cursor:
			print carId,row
			if carId in row:
				print "confirmed!"
				return True
			else:
				print "not confirmed"
				return False

	def dataUpload(self,gateId,carId,data):
		
		conn.execute("INSERT INTO DATABASE (GATEID,CARID,DATA,STATE)\
			VALUES ('%s','%s','%s',1)"%(gateId,carId,data))
		conn.commit()
		

if(__name__=='__main__'):	
	s=zerorpc.Server(CenterRPC())
	s.bind("tcp://0.0.0.0:4242")
	s.run()






 











