
import pcap, dpkt, ctypes, sys
from ctypes.util import find_library


if sys.platform == "darwin":
    _pcap = ctypes.cdll.LoadLibrary(find_library("libpcap"))

errbuf = ctypes.create_string_buffer(256) 

###### Beginning of Set up promiscous mode for interface en0 ########

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

###### End of Set up promiscous mode for interface en0 ########

#########capture packet###########
pc = pcap.pcap('en0')
pc.setfilter('tcp')
for ptime, pdata in pc:
    try: 
        eth = dpkt.ethernet.Ethernet(pdata)
        ip = eth.data
        if type(ip.data) == TCP:        
            tcp = ip.data
            if (tcp.flags == 1):
                srcIP = '%d.%d.%d.%d'%tuple(map(ord,list(ip.src))) 
                dstIP = '%d.%d.%d.%d'%tuple(map(ord,list(ip.dst))) 
                srcport = tcp.sport
                dstport = tcp.dport
                new_packet = IP(src=srcIP, dst=dstIP)/TCP(sport=srcport, dport=dstport)/Raw("\x00\x00\x00\x00")
                send(new_packet)
          
            break


    except KeyboardInterrupt:
        print "[*] Shutting down..."
        exit(0)


















