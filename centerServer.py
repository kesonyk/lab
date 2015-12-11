import zerorpc
import sqlite3



conn=sqlite3.connect('center.db')
conn.text_factory=str
carMap={}
distMap={}


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

		if not isTabExist('DATABASE'):
			conn.execute('''CREATE TABLE DATABASE
						( GATEID TEXT  NOT NULL,
					  	CARID  TEXT  NOT NULL,
					  	DATA   TEXT  NOT NULL,
					  	STATE  TEXT  NOT NULL)''')
			print "Table created successfully"

		if not isTabExist('DISTTAB'):

			conn.execute('''CREATE TABLE DISTTAB
						( GATEID TEXT NOT NULL,
						  DIST	 TEXT NOT NULL)''')

			print "Table created successfully"


		conn.execute("INSERT INTO PERMISSION (GATEID,CARID,CARSRC)\
			VALUES ('01','001','fffffffffffffff1')")


		conn.execute("INSERT INTO DATABASE (GATEID,CARID,DATA,STATE)\
			VALUES ('01','fffffffffffffff1','',0)")

		conn.execute("INSERT INTO DISTTAB (GATEID,DIST)\
			VALUES ('01','200')")


		cursor=conn.execute("SELECT * from PERMISSION")
		for row in cursor:
			carMap[row[2]]=row[1]
			print type(row)
			print row

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


	def carConfirm(self,gateId,carId):

		cursor=conn.execute("SELECT GATEID,CARSRC from PERMISSION")
		for row in cursor:
			print carId,row
			if gateId==row[0] and carId==row[1]:
				print "confirmed!"
				return True
			else:
				print "not confirmed"
				return False

	def dataUpload(self,gateId,carId,data):

		conn.execute("""INSERT INTO DATABASE (GATEID,CARID,DATA,STATE)\
			VALUES (?,?,?,1);""",(gateId,carMap[carId],data))
		conn.commit()


	def distInfo(self):
		distMap={}
		cursor=conn.execute("SELECT GATEID,DIST from DISTTAB")
		for row in cursor:
			print row
			distMap[row[0]]=row[1]
		return distMap;


if(__name__=='__main__'):
	s=zerorpc.Server(CenterRPC())
	s.bind("tcp://0.0.0.0:4242")
	s.run()


















