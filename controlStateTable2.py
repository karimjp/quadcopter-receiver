StateTable={
'PITCH': 0,
'ROLL':0,
'YAW':0,
'THRUST':1000
}

class ControlStateTable:
	def __init__(self):
		self.PS3ControllerState=StateTable
	def decode(self,Input):
		Input = Input.split('|') 
		code=int(Input[0])
		value=int(Input[1])
		key,value=self.getAction(code,value) #returns tuple 
		return (key,value)
	def getAction(self,code,value):
		#PITCH CODE [-128,127]
		if (code == 3):
			return ("PITCH",value)	
		#ROLL CODE [-128,127]
		elif (code == 2):
			return ("ROLL",value)
		#YAW CODE [-128,127]
		elif (code == 0):
			return ("YAW",value)
		#THRUST CODE INCREASE [0,255] #change code 
		elif (code == 15):
			value = self.PS3ControllerState['THRUST'] + 5
			if value > 2000:  #highest threshold
				value = 2000
			return ("THRUST",value)
		#THRUST CODE DECREASE [0,255] #change code
		elif (code == 14):
			value = self.PS3ControllerState['THRUST'] - 5
			if value < 1000: #lowest threshold
				value = 1000
			return ("THRUST",value)
		elif (code == 28): #button X
			return ("EXIT", 500)
		else:
			return (-1,-1)
		
	def updateStateTable(self,key,value):
		self.PS3ControllerState[key] = value
	def strTable(self):
		return str(self.PS3ControllerState)	
	def getTable(self):
		return self.PS3ControllerState


