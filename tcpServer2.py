#Main program:
#reads IMU data from arduino uart
#receives PS3 Controller input
#Mantains Controller input frequency with CST

#!/usr/bin/env python
from map import mapControllerToDeg
from map import constrain
from map import wrap_180
from map import motorOutputLimitHandler
from uart1 import IMUDevice
import socket
from controlStateTable2 import ControlStateTable
from map import arduino_map
from pid import PID
import time
import pdb
def setup(pids):
	# PID Configuration
	
	#pids['PITCH'].set_Kpid(6.5,0.1,1.2)
	#pids['ROLL'].set_Kpid(6.5,0.1,1.2)

	#pids['PITCH'].set_Kpid(6.5,0.1,1.2)
	#pids['ROLL'].set_Kpid(6.5,0.1,1.2)
	#pids['YAW'].set_Kpid(2.7,1,0)

	pids['PITCH'].set_Kpid(6.5,0,0)
	pids['ROLL'].set_Kpid(0,0,0)
	#pids['YAW'].set_Kpid(0,0,0)

def print_IMU_CST_Streams():
	print CST.strTable()
	#print "IMU reading" + IMU.getLine()

def convert_IMU_CST_to_Degrees():
	global C_YPR
	#sets Y,P,R in IMU class

	IMU.getYPR(IMU.getLine())
	#converts the control values for YPR to degrees
	C_YPR = mapControllerToDeg(CST.getTable())	
	#print "IMU DATA:"
	#print IMU.Yaw, IMU.Pitch, IMU.Roll
	print "CONTROL DEG DATA: ", str(C_YPR)
	

def calculatePIDs():
	global pitch_output, roll_output, yaw_output, thr, pids
	#PID CODE
	#print "PID _____ PITCH: "
	pitch_output = constrain(pids['PITCH'].update_pid_std(C_YPR['P'], IMU.Pitch, 10000),-250, 250)
	#print "PID _____ ROLL: "
	roll_output = constrain(pids['ROLL'].update_pid_std(C_YPR['R'], IMU.Roll, 10000),-250, 250)
	#print "PID _____ YAW: "
	yaw_output = constrain(pids['YAW'].update_pid_std(wrap_180(C_YPR['Y']), wrap_180(IMU.Yaw), 10000),-360, 360)
	#get thrust
	#thr = float(CST.getTable()['THRUST'])

def calculateMotorThrust():		
	global pitch_output, roll_output, yaw_output, thr, motor, pidStatusEnable

	#motor['FL'] = thr + roll_output + pitch_output - yaw_output
	#motor['BL'] = thr + roll_output - pitch_output + yaw_output
	#motor['FR'] = thr - roll_output + pitch_output + yaw_output
	#motor['BR'] = thr - roll_output - pitch_output - yaw_output
	motor['FL'] = thr + roll_output - pitch_output + yaw_output
	motor['BL'] = thr + roll_output + pitch_output - yaw_output
	motor['FR'] = thr - roll_output - pitch_output - yaw_output
	motor['BR'] = thr - roll_output + pitch_output + yaw_output

	motorOutputLimitHandler(motor)
	sep= ","
	tuple1 = str(int(motor['BR']))+sep+str(int(motor['BL']))+sep+str(int(motor['FR']))+sep+str(int(motor['FL']))
	

	writeResult = IMU.writeSerialPort(tuple1)

		#except Exception, e:
	#	raise
#	if writeResult == -1:
		#print "Could not write motor value............."
	print "Motor: ", str(motor)
	print "--------"

def sleep():
	global seconds, microseconds_unit
	time.sleep(seconds/microseconds_unit)

def stabilizationCode():
	print_IMU_CST_Streams()
	convert_IMU_CST_to_Degrees()
	calculatePIDs()
	#try:
	calculateMotorThrust()
	#except Exception, e:
	#	raise
	sleep()

seconds = 10000
microseconds_unit = 1000000.0
unblocking = 0 #unblocks socket
#verify client and server ip are = to interface ip
#TCP_IP = '192.168.1.7'
TCP_IP='192.168.1.101'
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response
#To store degrees from PS3 Controller
C_YPR = {}
#PID dictionary
pids = { 'PITCH': PID(), 
	'ROLL': PID(),
	'YAW': PID()  }
 
#motor dictionary
motor = { 'FL':0, 'BL':0,
    	 'FR':0, 'BR':0  }


pitch_output=0
roll_output=0
yaw_output=0
thr = 0

THR_MIN = 1100
THR_MAX = 2000

IMU = IMUDevice()
IMU.openSerialPort()
IMU.openSampleFile()
CST = ControlStateTable()


############################## open wireless constants set port ##################
TCP_IP2='192.168.1.101'
TCP_PORT2 = 5008
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.setblocking(unblocking)
server_address2 = (TCP_IP2, TCP_PORT2)
s2.bind(server_address2)
s2.listen(1)

conn2, addr2 = s2.accept()

print 'Connection address:', addr2
################################  open ps3 socket port #####################
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.setblocking(unblocking)
server_address = (TCP_IP, TCP_PORT)
s.bind(server_address)
s.listen(1)


conn, addr = s.accept()
print 'Connection address:', addr

conn.setblocking(unblocking) #does not wait for packets
conn2.setblocking(unblocking)
#configure PID
setup(pids)
def setPidConstantsWireless(data):
	#pdb.set_trace()
	global conn2
	global pids
	keyf = data[0]
	keyPidC=data[1]
	value = data[2:]
	value = float(value)
	p=pids['PITCH']
	r=pids['ROLL']
	y=pids['YAW']

	if keyf == 'p':
		pKp = p.m_Kp
		pKd = p.m_Kd
		pKi = p.m_Ki	
		if keyPidC == 'p':
			pKp = value	
		elif keyPidC == 'i':
			pKi = value
		elif keyPidC == 'd':
			pKd = value
		pids['PITCH'].set_Kpid(pKp, pKi, pKd)

	if keyf == 'r':
		rKp = r.m_Kp
		rKd = r.m_Kd
		rKi = r.m_Ki	
		if keyPidC == 'p':
			rKp = value	
		elif keyPidC == 'i':
			rKi = value
		elif keyPidC == 'd':
			rKd = value
		pids['ROLL'].set_Kpid(rKp, rKi, rKd)

	if keyf == 'y':
		yKp = y.m_Kp
		yKd = y.m_Kd
		yKi = y.m_Ki	
		if keyPidC == 'p':
			yKp = value	
		elif keyPidC == 'i':
			yKi = value
		elif keyPidC == 'd':
			yKd = value
		pids['YAW'].set_Kpid(yKp, yKi, yKd)

	ptitle="| Pitch: kp, kd, ki= "
	pData =str(p.m_Kp)+","+ str(p.m_Kd)+","+ str(p.m_Ki)
	rtitle="| Roll: kp, kd, ki= "
	rData=str(r.m_Kp)+","+ str(r.m_Kd)+","+ str(r.m_Ki)
	ytitle="| Yaw: kp, kd, ki= "
	yData=str(y.m_Kp)+","+ str(y.m_Kd)+","+ str(y.m_Ki)
	conn2.send(ptitle+pData+rtitle+rData+ytitle+yData)
	#print "DATA RX:"
	#print data
	#print ptitle + pData
	#exit()

################################## Main loop ######################################
while 1:
	#pdb.set_trace()
	try:	
		data2 = conn2.recv(BUFFER_SIZE)
		#pdb.set_trace()
		if data2 not in ['', None]: #no data
			setPidConstantsWireless(data2)		
	#if no data is rx continue		
	except:	
		#if no data is received from ps3 controller then continue
		try:
			data = conn.recv(BUFFER_SIZE)
		except:  
			#controller is connected but no data has been received
			#send data from CST and IMU when no PS3 input received
			if thr >= 1150: #only run pid if thrust is over 1100
				#try:
				stabilizationCode()
				#except Exception, e:
				#	continue
			#else:
				#due to anomalies in the data stream at the beginning of reading
				#the serial buffer we need to start releasing it before our thrust
				#is good for flight
				#buffRelease=IMU.getLine()
			continue
		"""if data in ['',None]:  #enable for testing 
			#controller is not connected
			#send data from CST and IMU when no PS3 input received
			stabilizationCode()
			continue"""
		#PS3 data received 
		#print "received data:"+ data
		key,value=CST.decode(data)
		
		#print key, value
		if key == 'EXIT': #shutdown pid
			tuple1 = "1000,1000,1000,1000"
			writeResult = IMU.writeSerialPort(tuple1)
			conn.close()
			conn2.close()
			exit()

		CST.updateStateTable(key,value)
		
		thr = float(CST.getTable()['THRUST'])
		if thr  >= 1150: #only run pid if thrust is over 1100
			#try:
			stabilizationCode()
			#except Exception, e:
				#continue
		#else:
			#due to anomalies in the data stream at the beginning of reading
			#the serial buffer we need to start releasing it before our thrust
			#is good for flight
			#buffRelease=IMU.getLine()

		conn.send(data) #echo
	#conn.close()
