StateTable={
'PITCH_UP': 0,
'PITCH_DOWN': 0,
'ROLL_RIGHT':0,
'ROLL_LEFT':0,
'YAW_RIGHT':0,
'YAW_LEFT':0,
'THRUST_INCREASE':0,
'THRUST_DECREASE':0

}

class ControlStateTable:
	def __init__(self):
		self.PS3ControllerState=StateTable
	def decode(self,input):
		input = input.split('|') 
		code=int(input[0])
		value=int(input[1])
		key,value=self.getAction(code,value) #returns tuple 
		return (key,value)
	def getAction(self,code,value):
		#[1,127]
		if (code == 3) and (value in range(0,128)):
			return ("PITCH_UP",value)	
		#[-128,-1]
		elif (code == 3) and (value in range(-128,0)): 			
	 		return ("PITCH_DOWN",value)
		#[1,127]
		elif (code == 2) and (value in range(0,128)):
			return ("ROLL_RIGHT",value)
		#[-128,-1]
		elif (code == 2) and (value in range(-128,0)):
			return ("ROLL_LEFT",value)
		#[1,127]
		elif (code == 0) and (value in range(0,128)):
			return ("YAW_RIGHT",value)
		#[-128,-1]
		elif (code == 0) and (value in range(-128,0)):
			return ("YAW_LEFT",value)
		#[0,255] no need to check range
		elif (code == 15):
			return ("THRUST_INCREASE",value)
		#[0,255] no need to check range
		elif (code == 14):
			return ("THRUST_DECREASE",value)
		else:
			return (-1,-1)
	def updateStateTable(self,key,value):
		self.PS3ControllerState[key] = value
	def printTable(self):
		print self.PS3ControllerState
