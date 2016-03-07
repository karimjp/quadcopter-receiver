
from scapy.all import *


class ControlFrame(Packet):
        name="Control Frame"
        fields_desc=[ ShortField("code", 0),
                      ShortField("value",0)]
def make_test(x, y,srcIP,dstIP,dstPort):
        pkt = IP(src=srcIP, dst=dstIP)/TCP(dport=dstPort)/ControlFrame(code=x,value=y)
        pkt.show()
        sendp(pkt, iface="wlan0")

