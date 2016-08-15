##
## A very low level AR.Drone2.0 Python controller
## by Micah Sherr
## (use at your own risk)
##




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

#send command
def sendCommand( cmd ):
    global address
    global seqno   #sequence number
    global s
    print "DEBUG: Sending:  '%s'" % cmd.strip()
    s.sendto(cmd,address)
    #seqno += 1


def reset():
    global seqno
    seqno = 1   #needs to send before other commands
    sendCommand("AT*FTRIM=%d\r" % seqno ) #sets the reference for the horizontal plane

        
def takeoff():
    global seqno
    sendCommand("AT*FTRIM=%d\r" % seqno )
    takeoff_cmd = setBits([9])
    for i in xrange(1,25):                  #send repeatly to make it take off
        sendCommand("AT*REF=%d,%d\r" % (seqno,takeoff_cmd)) #AT*REF is used for takeoff, landing, reset and emergency stop

        
def land():
    global seqno
    land_cmd = setBits([])
    for i in xrange(1,25):                 #send repeatly to make it land
        sendCommand("AT*REF=%d,%d\r" % (seqno,land_cmd)) 


def toggleEmergencyMode():
    global seqno
    shutdown_cmd = setBits([8]) #if in emergency mode, it will change to normal. If in normal mode, change to emergency
    sendCommand("AT*REF=%d,%d\r" % (seqno,shutdown_cmd))

#control drone movement during flight

def disable_Yaw():
    global seqno
    comYaw_cmd = setBits([1])

def roll(direct):
    global seqno
    #progressive()
    if direct == 'a':
        roll_cmd = -1082130432
    if direct == 'd':
        roll_cmd = 1065353216
    sendCommand("AT*PCMD=%d,1,%d,0,0,0\r" % (seqno,roll_cmd))

def pitch(direct):
    global seqno
    if direct == 'w':
        pitch_cmd = -1082130432
    if direct == 's':
        pitch_cmd = 1065353216
    sendCommand("AT*PCMD=%d,1,0,%d,0,0\r" % (seqno,pitch_cmd))

def gaz(direct):
    global seqno
    if direct == 'u':
        gaz_cmd = 1065353216
    if direct == 'j':
        gaz_cmd = -1082130432
    sendCommand("AT*PCMD=%d,1,0,0,%d,0\r" % (seqno,gaz_cmd))

def yaw(direct):
    global seqno
    if direct == 'h':
        yaw_cmd = -1082130432
    if direct == 'k':
        yaw_cmd = 1065353216
    sendCommand("AT*PCMD=%d,1,0,0,0,%d\r" % (seqno,yaw_cmd))

#user instruction
def printUsage():
    print "\n\n"
    print "Keyboard commands:"
    print "\tq       - quit"
    print "\tt       - takeoff"
    print "\tl       - land"
    print "\t(space) - emergency shutoff"
    print "\ta       - Left"
    print "\td       _ Right"
    print "\tw       _ front"
    print "\ts       _ back"
    print "\tu       _ up"
    print "\tj       _ down"
    print "\th       _ spin left"
    print "\tk       _ spin right"



print """
NOTE:  This program assumes you are already connected to the
       drone's WiFi network.
"""
    
address = ('192.168.1.1',5556)
seqno = 1
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", 5554))


while True:
    printUsage()
    ch = getChar()
    if ch == 'q':
        exit(0)
    elif ch == 't':
        takeoff()
    elif ch == 'l':
        land()
    elif ch == ' ':
        reset()
        toggleEmergencyMode()
    elif ch == 'a' or ch == 'd':
        roll(ch)
    elif ch == 'w' or ch == 's':
        pitch(ch)
    elif ch == 'u' or ch == 'j':
        gaz(ch)
    elif ch == 'h' or ch == 'k':
        yaw(ch)
    else:
        print "Invalid command!"