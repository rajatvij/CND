# Import libraries for retreiving information from url and regular expression
import urllib
import re

# retrieve list of tor list links data from url and write it to a text file.
urllib.urlretrieve("https://collector.torproject.org/recent/exit-lists/", filename="recent-list.txt")

# Open and parse text file containing list of tor list.
with open("recent-list.txt", "r") as infile:
    for line in infile:
	# Find most recent tor list using regular expression.
        filenameregex = re.search(r"\d{4}\-\d{2}\-\d{2}\-\d{2}\-\d{2}\-\d{2}.*?", line)
        if filenameregex:
	    # Once their is a match, retrieve most recent tor list from its url to a text file.
            urllib.urlretrieve("https://collector.torproject.org/recent/exit-lists/"+filenameregex.group(0), filename="tor-list.txt")
            break

# Open and parse the most recent tor list line by line
with open("tor-list.txt", "r") as infile, open("ip-list.txt", "w") as outfile:
    for line in infile:
	# search for ip address in each line.
        ip = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",line)
        if ip:
	    # If ip address is found then print it to the outfile.
            print >> outfile, ip.group(0)+"\n",

# Open and parse the list of ip address from Output.txt line by line.
with open("ip-list.txt", "r") as infile, open("dynamically-generated.py", "w") as outfile:

	# Write following python code to an output python file.
	outfile.write("from stix.common.vocabs import VocabString \nfrom stix.core import STIXPackage \nfrom stix.indicator import Indicator \nfrom stix.ttp import TTP \nfrom stix.ttp.infrastructure import Infrastructure \n")
	outfile.write("from stix.ttp.resource import Resource \nfrom cybox.core import Observables, Observable, Object \nfrom cybox.objects.address_object import Address \ndef main(): \n    stix_package = STIXPackage()\n\n")
	num=1

	for line in infile:
	    # Insert ip address that is parsed line by line to the python code
	    outfile.write ('    addr'+str(num)+' = Observable(Address(address_value=\"'+line[:-1]+'\", category=Address.CAT_IPV4))\n')
	    num+=1

	num=1
	infile.seek(0)

	for line in infile:
	    # Insert the line number to the python code line by line.
	    outfile.write ( '    stix_package.add_observable(addr'+str(num)+')\n')
	    num+=1

	num=1
	infile.seek(0)

	for line in infile:
	    # Insert the line number to the python code line by line.
	    outfile.write ( '    obs_addr'+str(num)+' = Observable()\n')
	    num+=1

	infile.seek(0)
	num=1

	for line in infile:
	    # Insert the line number to the python code line by line.
	    outfile.write ( '    obs_addr'+str(num)+'.id_ = None\n')
	    num+=1

	infile.seek(0)
	num=1

	for line in infile:
	    # Insert the line number to the python code line by line.
	    outfile.write ( '    obs_addr'+str(num)+'.idref = addr1.id_\n')
	    num+=1

	outfile.write ( '    vocab_string = VocabString(value=\'Malware C2\')\n    infrastructure = Infrastructure()\n    infrastructure.observable_characterization = Observables([')
	infile.seek(0)
	num=1
	lines = len(infile.readlines())
	#infile.seek(0)

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
