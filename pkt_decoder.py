from scapy.all import *

interface = "wlan0"

class ControlFrame(Packet):
        name="Control Frame"
        fields_desc=[ ShortField("code", 0),
                      ShortField("value",0)]

def test(x):
	if x.haslayer(ControlFrame):	
		print "True"
	else:
		print "False"
sniff(iface=interface,prn=lambda x:test(x))
