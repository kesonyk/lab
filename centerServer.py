import zerorpc
import sqlite3



conn=sqlite3.connect('center.db')
conn.text_factory=str
carMap={}
distMap={'01':'300'}


def isTabExist(tabName):
	cursor=conn.execute("SELECT tbl_name FROM sqlite_master WHERE type='table'")
	for row in cursor:
		if tabName in row:
			return True
	return False

"""
 RPC Server Operation
"""
class CenterRPC(object):

	def __init__(self):
		if not isTabExist('PERMISSION'):
		#create the Permission Tab
			conn.execute('''CREATE TABLE PERMISSION
					( GATEID TEXT  NOT NULL,
					  CARID  TEXT  NOT NULL,
					  CARSRC   TEXT  NOT NULL)''')
			print "Permission Table created successfully"
			conn.execute("INSERT INTO PERMISSION (GATEID,CARID,CARSRC)\
			VALUES ('01','001','fffffffffffffff1')")


		if not isTabExist('DATABASE'):
			conn.execute('''CREATE TABLE DATABASE
						( GATEID TEXT  NOT NULL,
					  	CARID  TEXT  NOT NULL,
					  	DATA   TEXT  NOT NULL,
					  	STATE  TEXT  NOT NULL)''')
			print "Database Table created successfully"
			conn.execute("INSERT INTO DATABASE (GATEID,CARID,DATA,STATE)\
			VALUES ('01','fffffffffffffff1','',0)")
	
	
		if not isTabExist('DISTTAB'):
			conn.execute('''CREATE TABLE DISTTAB
						( GATEID TEXT NOT NULL,
						  DIST	 TEXT NOT NULL)''')
			print "Distance Table created successfully"
			conn.execute("INSERT INTO DISTTAB (GATEID,DIST)\
			VALUES ('01','300')")
			conn.execute("INSERT INTO DISTTAB (GATEID,DIST)\
			VALUES ('02','300')")
			conn.execute("INSERT INTO DISTTAB (GATEID,DIST)\
			VALUES ('03','300')")
			conn.execute("INSERT INTO DISTTAB (GATEID,DIST)\
			VALUES ('04','300')")



		print "CarPermission Show:"
		print "Gate   Car"
		cursor=conn.execute("SELECT * from PERMISSION")
		for row in cursor:
			carMap[row[2]]=row[1]
			print row

		cursor=conn.execute("SELECT * from DATABASE")
		for row in cursor:
			print type(row)
			print row
		
		cursor=conn.execute("SELECT GATEID,DIST from DISTTAB")
		for row in cursor:
			print type(row)
			print row
		conn.commit()

		conn.close()

		

	def dataSelect(self,gateId):
			
		conn=sqlite3.connect('center.db')
		sql="SELECT * from DATABASE WHERE GATEID="+"gateId"
		print sql

		cursor=conn.execute(sql)
		ret=[]
		for row in cursor:
			print row
			ret.append(row)
		conn.close()
		return ret


	def carConfirm(self,gateId,carSrc):
		
		conn=sqlite3.connect('center.db')
		cursor=conn.execute("SELECT GATEID,CARSRC from PERMISSION")
	
		for row in cursor:
			print carId,row
			if gateId==row[0] and carSrc==row[1]:
				print "confirmed!"
				conn.close()
				return True
			else:
				print "not confirmed"
				conn.close()
				return False

	def dataUpload(self,gateId,carId,data):
		
		conn=sqlite3.connect('center.db')
		conn.execute("""INSERT INTO DATABASE (GATEID,CARID,DATA,STATE)\
			VALUES (?,?,?,1);""",(gateId,carMap[carId],data))
		conn.commit()
		conn.close()

	def distInfo(self):
		conn=sqlite3.connect('center.db')
		cursor=conn.execute("SELECT GATEID,DIST from DISTTAB")
		for row in cursor:
			distMap[row[0]]=row[1]
		conn.close()
		print distMap
		return distMap;


if(__name__=='__main__'):
	s=zerorpc.Server(CenterRPC())
	s.bind("tcp://0.0.0.0:4242")
	s.run()







