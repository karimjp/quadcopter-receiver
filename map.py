
#use to map analog controller values to degrees 
# add // sign division for integer result
def arduino_map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) // (in_max - in_min) + (out_min)

#takes as input a control struct with YPR analog input 
#and returns a dict of size 3 with YPR in Degrees
def mapControllerToDeg(controlDict):
	retStruct ={}
	#PS3 Analog Value
	CONTROL_PITCH_MIN = -128
	CONTROL_PITCH_MAX = 127
	CONTROL_ROLL_MIN = -128
	CONTROL_ROLL_MAX = 127
	CONTROL_YAW_MIN = -128
	CONTROL_YAW_MAX = 127
	
	PITCH_DEG_MIN = -45
	PITCH_DEG_MAX = 45
	ROLL_DEG_MIN = -45
	ROLL_DEG_MAX = 45
	YAW_DEG_MIN = -180
	YAW_DEG_MAX = 180

	retStruct['P']=arduino_map(controlDict['PITCH'],
				CONTROL_PITCH_MIN,
				CONTROL_PITCH_MAX,
				PITCH_DEG_MIN,
				PITCH_DEG_MAX)
	
	retStruct['R']=arduino_map(controlDict['ROLL'],
				CONTROL_ROLL_MIN,
				CONTROL_ROLL_MAX,
				ROLL_DEG_MIN,
				ROLL_DEG_MAX)

	retStruct['Y']=arduino_map(controlDict['YAW'],
				CONTROL_YAW_MIN,
				CONTROL_YAW_MAX,
				YAW_DEG_MIN,
				YAW_DEG_MAX)

	return retStruct



def wrap_180(x): 
	if x<-180:
		return x+360
	elif x > 180:
		return x-360
	else:
		return x

def constrain(amt, low, high):
	if amt < low:
		return low
	elif amt > high:
		return high
	else:
		return amt


def motorOutputLimitHandler(motor_dict):
	MIN_THRUST = 1150
	MAX_THRUST = 2000
	for key, value in motor_dict.iteritems():
		motor_dict[key] = constrain(value, MIN_THRUST,
						MAX_THRUST)
