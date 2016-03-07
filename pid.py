#Reference: https://github.com/antodoms/beagle-copter/blob/master.pid.h
#http://robotics.stackexchange.com/questions/2964/quadcopter-pid-output

class PID:

	def __init__(self,Kp=0,Ki=0,Kd=0):
		'''PID Initialization'''
		#PID Constants
		self.m_Kp=Kp;
		self.m_Ki=Ki;
		self.m_Kd=Kd;

		#PID constants
		self.m_err=0;
		self.m_sum_err=0;
		self.m_ddt_err=0;
		self.m_lastInput=0;
		if Kp == 0:
			self.m_outmax=200;
			self.m_outmin=-200;
		else:
			self.m_outmax=400;
			self.m_outmin=-400;
		self.m_output=0;
		#self.setpoint=0;

	def update_pid_std(self, setpoint, Input, dt):
		#computes error
		self.m_err = setpoint - Input
		
		#Integrating errors
		self.m_sum_err += self.m_err * self.m_Ki * dt
		
		#calculating error derivative
		#Input derivative is used to avoid derivative kick
		self.m_ddt_err = -1*(self.m_Kd) / dt * (Input - self.m_lastInput)
		
		#Calculation of the output
		#winds up boundaries
		self.m_output = self.m_Kp * self.m_err + self.m_sum_err + self.m_ddt_err
		if self.m_output > self.m_outmax:
			#winds up boundaries 
			self.m_sum_err = 0.0
			self.m_output = self.m_outmax
		elif self.m_output < self.m_outmin:
			#winds up boundaries
			self.m_sum_err = 0.0
			self.m_output = self.m_outmin
		
		self.m_lastInput = Input
		
		"""print "kp " + str(self.m_Kp)
		print "kd " + str(self.m_Kd)
		print "ki " + str(self.m_Ki)
		print "setpoint " + str(setpoint)
		print "input " + str(Input)
		print "output " + str(self.m_output)
		print "err " + str(self.m_err)
		print "ddt_err " + str(self.m_ddt_err)
		print "sum_err " + str(self.m_sum_err)"""	
		
		return self.m_output
		
	def set_Kpid(self, Kp, Ki, Kd):
		self.m_Kp = Kp
		self.m_Ki = Ki
		self.m_Kd = Kd
	
	def set_windup_bounds(self, Min, Max):
		self.m_outmax = Max
		self.m_outmin = Min
		
	def reset():
		self.m_sum_err = 0
		self.m_ddt_err = 0
		self.m_lastInput = 0
	

	

