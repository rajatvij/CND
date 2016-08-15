from scapy.all import *

for i in range(0,100):
    packet = (IP(src="192.168.106.128",dst="127.0.0.1")/UDP(sport=53)/DNS(id=i*10,rd=1,qd=DNSQR(qname='z.tiwaz.net',qtype="A",qclass="IN")))
    res = sr(packet)
