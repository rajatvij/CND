import urllib
import re

urllib.urlretrieve("https://collector.torproject.org/recent/exit-lists/", filename="recent-list.txt")

with open("recent-list.txt", "r") as infile:
    for line in infile:
        filenameregex = re.search(r"\d{4}\-\d{2}\-\d{2}\-\d{2}\-\d{2}\-\d{2}.*?", line)
        if filenameregex:
            urllib.urlretrieve("https://collector.torproject.org/recent/exit-lists/"+filenameregex.group(0), filename="tor-list.txt")
            break

with open("tor-list.txt", "r") as infile, open("Output.txt", "w") as outfile:
    for line in infile:
        ip = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",line)
        if ip:
            print >> outfile, ip.group(0)+"\n",

with open("Output.txt", "r") as infile, open("Output2.py", "w") as outfile:
	outfile.write("from stix.common.vocabs import VocabString \nfrom stix.core import STIXPackage \nfrom stix.indicator import Indicator \nfrom stix.ttp import TTP \nfrom stix.ttp.infrastructure import Infrastructure \n")
	outfile.write("from stix.ttp.resource import Resource \nfrom cybox.core import Observables, Observable, Object \nfrom cybox.objects.address_object import Address \ndef main(): \n    stix_package = STIXPackage()\n\n")
	num=1
	for line in infile:
		outfile.write ('    addr'+str(num)+' = Observable(Address(address_value=\"'+line[:-1]+'\", category=Address.CAT_IPV4))\n')
		num+=1
	num=1
	infile.seek(0)
	for line in infile:
		outfile.write ( '    stix_package.add_observable(addr'+str(num)+')\n')
		num+=1
	num=1
	infile.seek(0)
	for line in infile:
		outfile.write ( '    obs_addr'+str(num)+' = Observable()\n')
		num+=1
	infile.seek(0)
	num=1
	for line in infile:
		outfile.write ( '    obs_addr'+str(num)+'.id_ = None\n')
		num+=1
	infile.seek(0)
	num=1
	for line in infile:
		outfile.write ( '    obs_addr'+str(num)+'.idref = addr1.id_\n')
		num+=1
	outfile.write ( '    vocab_string = VocabString(value=\'Malware C2\')\n    infrastructure = Infrastructure()\n    infrastructure.observable_characterization = Observables([')
	infile.seek(0)
	num=1
	lines = len(infile.readlines())
	infile.seek(0)
	for line in infile:
		if num==lines:
		    outfile.write ( 'obs_addr'+str(num))
		else:
		    outfile.write ( 'obs_addr'+str(num)+',')
		num+=1
		
	outfile.write ( '])\n')
	outfile.write ( '    infrastructure.add_type(vocab_string)\n    resource = Resource()\n    resource.infrastructure = infrastructure\n')
	outfile.write ( '    ttp = TTP(title="Malware C2 Channel")\n    ttp.resources = resource\n\n')
	outfile.write ( '    stix_package.add_ttp(ttp)\n')
	outfile.write ( '    print stix_package.to_xml()\n\n')
	outfile.write ( 'if __name__ == \'__main__\':\n    main()')