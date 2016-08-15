import getopt, sys
import pcap
from dpkt.ethernet import Ethernet
import dpkt
import ctypes
from ctypes.util import find_library
from scapy.all import *
import tty, termios

if sys.platform == "darwin":
    _pcap = ctypes.cdll.LoadLibrary(find_library("libpcap"))
elif sys.platform == "linux2":
    _pcap = ctypes.cdll.LoadLibrary("libpcap.so")

errbuf = ctypes.create_string_buffer(256)   #error message if lookupdev() fails

dstIP = '192.168.1.1' # spoofed source IP address
srcIP = '0.0.0.0'
dstPort = 5556 
srcPort = 5554 
seqno = 1 


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
    global seqno  
    print "DEBUG: Sending:  '%s'" % cmd.strip()
    for i in xrange(1,25): 
        spoofed_packet = IP(src=source_ip, dst=dstIP) / UDP(sport=srcPort, dport=dstPort) / cmd
        send(spoofed_packet)
        seqno += 1 

def printUsage():
    print "\tl       - land"

####### air drone command ########
def takeoff():
    global seqno
    global srcIP
    seqno = int(seqno) + 100
    takeoff_cmd = setBits([9])
    sendCommand("AT*REF=%d,%d\r" % (seqno,takeoff_cmd),srcIP)

def pitch():
    global seqno
    seqno = int(seqno) + 100
    pitch_cmd = -1082130432
    sendCommand("AT*PCMD=%d,1,0,%d,0,0\r" % (seqno,pitch_cmd),srcIP)

def reset():
    global seqno
    seqno = int(seqno) + 100
    sendCommand("AT*FTRIM=%d\r" % seqno,srcIP)

def land():
    global seqno
    global srcIP
    seqno = int(seqno) + 100
    land_cmd = setBits([])
    sendCommand("AT*REF=%d,%d\r" % (seqno,land_cmd),srcIP)

####### defence function #########
def mac_addr(mac_string):
    """Print out MAC address given a string

    Args:
        mac_string: the string representation of a MAC address
    Returns:
        printable MAC address
    """
    return ':'.join('%02x' % ord(b) for b in mac_string)

def macAdd_check(attackerMAC):  
    if attackerMAC == "90:03:b7:cc:47:9a":        # whether the sender is airdrone?
        return True
    elif attackerMAC == "80:be:05:01:e4:41":     # whether the sender is sharon's iphone?
        return True
    elif attackerMAC == "a4:5e:60:cc:fa:c3":      # whether the sender is sharon's mac?
        return True
    elif attackerMAC == "f8:95:c7:f1:98:e3":      # whether the sender is yingying's phone?
        return True
    elif attackerMAC == "b8:e8:56:35:3f:48":      # whether the sender is yingying's mac?
        return True
    else:
        return False
    #return True

def getSeqno(inputStr):
    global seqno
    sStr1 = inputStr
    ATStr = 'AT*'
    equalStr = '='
    orderTyp = ''

    try:
        nPos = sStr1.index(ATStr)
        sStr1 = sStr1[nPos + len(ATStr) :]
        
    except Exception, e:
        return False

    try:
        nPos = sStr1.index(equalStr)
        orderTyp = sStr1[0:nPos]
        sStr1 = sStr1[nPos + len(equalStr) :]
        sStr1 = sStr1[0: sStr1.index(',')]
        seqno = sStr1
        orderTypeList = {'REF':takeoff, 'PCMD':pitch, 'FTRIM':reset}
        orderTypeList.get(orderTyp)()
    except Exception, e:
        return False
    return True
                                


########## set up to monitor mode #############
pcap_lookupdev = _pcap.pcap_lookupdev
pcap_lookupdev.restype = ctypes.c_char_p
dev = pcap_lookupdev(errbuf)      
print dev

pcap_create = _pcap.pcap_create
pcap_create.restype = ctypes.c_void_p
handle = pcap_create(dev, errbuf)
print handle
if not handle:
    print "failed creating handler:",errbuf
    exit()

pcap_can_set_rfmon = _pcap.pcap_can_set_rfmon
pcap_can_set_rfmon.argtypes = [ctypes.c_void_p]
print "can rfmon:",pcap_can_set_rfmon(handle)

pcap_set_rfmon = _pcap.pcap_set_rfmon
pcap_set_rfmon.argtypes = [ctypes.c_void_p]
print "set rfmon:",pcap_set_rfmon(handle, 1)

pcap_activate = _pcap.pcap_activate
pcap_activate.argtypes = [ctypes.c_void_p]
pcap_activate(handle)
 

def usage():
    print >>sys.stderr, 'usage: %s [-i device] [pattern]' % sys.argv[0]
    sys.exit(1)
 
def main():

    opts, args = getopt.getopt(sys.argv[1:], 'i:h')
    name = None
    for o, a in opts:
        if o == '-i': name = a
        else: usage()
       
    pc = pcap.pcap('en0')
    pc.setfilter(' '.join(args))
    decode = { pcap.DLT_LOOP:dpkt.loopback.Loopback,
               pcap.DLT_NULL:dpkt.loopback.Loopback,
               pcap.DLT_EN10MB:dpkt.ethernet.Ethernet }[pc.datalink()] 
                  
    for ptime, pdata in pc:
        time = ptime
        p = dpkt.ethernet.Ethernet(pdata)
        try:
            if p.data.p == dpkt.ip.IP_PROTO_UDP:       #filter UDP packet
                if p.data.__class__.__name__ == 'IP': 
                    if '%d.%d.%d.%d'%tuple(map(ord,list(p.data.dst))) == "192.168.1.1":              
                        ip='%d.%d.%d.%d'%tuple(map(ord,list(p.data.src)))
                        global srcIP
                        srcIP = ip
                        attacker_macAdd = mac_addr(p.src)
                        
                        if macAdd_check(attacker_macAdd) == True:
                            #print "[+] No attacker detected."
                            pass
                        elif macAdd_check(attacker_macAdd) == False:
                            print "[+] Attacker dectected! MAC address: ", mac_addr(p.src)
                            dataStr = `decode(pdata)`
                            getSeqno(dataStr)
                            
        except:
            continue                           
 
if __name__ == '__main__':
     main()