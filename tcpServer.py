#!/usr/bin/env python
import uart1
import socket
#from controlStateTable import ControlStateTable
from controlStateTable2 import ControlStateTable

CST = ControlStateTable()


TCP_IP = '192.168.1.6'
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

 
conn, addr = s.accept()
print 'Connection address:', addr

while 1:
	data = conn.recv(BUFFER_SIZE)
	print "received data:"+ data
	key,value=CST.decode(data)
		
	CST.updateStateTable(key,value)
	#if not data: break
	#CST.printTable()
	conn.send(data)  # echo
	
#conn.close()
