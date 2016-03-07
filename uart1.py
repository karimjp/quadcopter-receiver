import serial
#import io
import time
import pdb

class IMUDevice:
	def __init__(self):
		self.sampleFileHandle = None
		self.Yaw=0
		self.Pitch=0
		self.Roll=0
		self.ser=None

	def openSerialPort(self):
		self.ser = serial.Serial('/dev/ttyACM0',writeTimeout=1,timeout=0)
		self.ser.setBaudrate(115200)		
		
	
	def writeSerialPort(self, Tuple):
		#self.ser.flushInput()
		#self.ser.flushOutput()
		#self.ser.flush()
		#sio = io.TextIOWrapper(io.BufferedRWPair(self.ser,self.ser))
		#sio = io.TextIOWrapper(io.BufferedWriter(self.ser))
		releasebuff = self.ser.read(self.ser.inWaiting())
		try:
			value = Tuple + '\n'
			#value = value.encode('utf-8')
			#bytesWritten=sio.write(unicode(Tuple))
			#it is buffering. Required to get the data out
			#sio.flush()
			print "Writing: " + value 
			writing = self.ser.write(unicode(value))
			#pdb.set_trace()	
			#writing = self.ser.writeLine(value)
			#time.sleep(0.5)
			#self.ser.writeV2(value) 
		except Exception, e:
			print e
			exit()
			
	#return in main loop one line at a time 
	def openSampleFile(self):
		self.sampleFileHandle = open('IMU_Data','rb')
		#ignore/read header
		self.sampleFileHandle.readline()
		#return sampleFile
	def getLine(self):
		#line = self.sampleFileHandle.readline()
		#self.ser.flushInput()
		#self.ser.flushOutput()
		#self.ser.flush()
		#line = self.ser.readline()
		bytesToRead=self.ser.inWaiting()
		#print type(bytesToRead)
		#print bytesToRead
		buff = self.ser.read(bytesToRead)
		lines = buff.split('\r\n')
		print lines
		line = lines[-2]
		line = self.is4TupleHelper(line)
		if line:
			#Motor sent values can be seen in the serial port.
			#Data split is > or < than 4 due to delay.
			#while line[0]!='Z' or len(line.split(',')) != 4:
			#	print line
			#	line = self.ser.readline()#get a new line
			return line
		else:
			print "No more data in sampleFile"
			exit()

	def is4TupleHelper(self,line):
		loop = True
		newLine=""
		#returns same passed line, OK
		if len(line.split(',')) == 4:
			return line
		else:
			while loop:
			#no check for len=4 because readline waits
			#for EOL to return. 
				newline = self.ser.readline()
				if newline[0]=='Z':
					return newline #This is a new line
		
			

	def parseLine(self, line):
		print "line to parse:"
		print line
		line = line.strip('\r\n')
		parsedLine = line.split(',')
		print parsedLine
		marker,Y,P,R = parsedLine
		return (marker,Y,P,R)

	def getYPR(self, line):
		Marker,Y,P,R = self.parseLine(line)
		#convert strings to decimal with precision
		self.Yaw, self.Pitch, self.Roll =(float(Y), float(P), float(R))
	
