import sys
import os

exe = "cat /dev/ttyACM0 >> /dev/null &"
if sys.argv[1]=='start':
	
	os.system(exe)
	import tcpServer2
