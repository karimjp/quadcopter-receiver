import uart1
import time
import pdb

i = uart1.IMUDevice()
i.openSerialPort()
time.sleep(2)
func = 'inc'
Tuple=""
ite=1150
while True:
	if ite>=2000:
		ite = 2000
		func='dec'
	elif ite<=1150:
		ite =1150
		func ='inc'
	
	size=i.ser.inWaiting()
	buff = i.ser.read(size)
	print buff
	buff = buff.split('\r\n')
	#print buff
	if len(buff) < 2:
		latestReading =buff[-1]
	else:
		latestReading = buff[-2]
	while len(latestReading.split(',')) != 4:
		latestReading = i.ser.readline()
		print "about to check [0]"
		print latestReading
		if latestReading:
			if latestReading[0] == 'Z': #and len(latestReading.split(','))==4:
				break
			
	print latestReading
	try:
		if func == 'inc':
			ite = ite + 100
			value = ite
			Tuple = str(value)+","+str(value)+","+str(value)+","+str(value)+"\n"
		elif func == 'dec':
			ite = ite -100
			value = ite
			Tuple = str(value)+","+str(value)+","+str(value)+","+str(value)+"\n"
		writing = i.ser.write(Tuple)
		print str(Tuple)
		print "Writing was sucessfull!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
		print i.ser.inWaiting()
		time.sleep(100000/100000)
	
	except Exception, e:
		print e
		print "Waiting to write......... ........ .......... ......... ..... ......"
		continue
		
	
	
	
