#Receives IMU data and control data
import sys

IMU_struct = sys.argv[1]
control_struct = sys.argv[2] 

def dataRX(IMU_struct, control_struct):
	print IMU_struct
	print control_struct



