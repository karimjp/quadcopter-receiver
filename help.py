import uart1

i = uart1.IMUDevice()
i.openSerialPort()
while True:
	i.ser.readline()
