from dnslib import DNSRecord,DNSHeader,DNSQuestion,RR,A

c=list()
for i in range(0,100):
    d = DNSRecord(DNSHeader(qr=1,aa=1,ra=1,auth=1,bitmap=0  ),q=DNSQuestion(qname='z.tiwaz.net',qtype=1,qclass=1),a=RR(rname="www.google"+str(i)+".com",rdata=A("127.0.0.1"),rtype=2))
    c.append(d)

print c
f = open("dns_response.txt", "w")
f.write(str(c))
f.close()