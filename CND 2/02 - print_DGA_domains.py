import sys
import getopt
import hashlib
import time
import argparse
from datetime import datetime

######################################################################################################
#
#  print_DGA_domains.py
#    Copyright 2016 - Matthew Norris
#
#  Simple Python boilerplate to wrap the provide_generated_domain function in a calling program.
#    Please modify as need be, but describe all changes in your writeup.
#
#  Last Modified: 20160203 - Rajat Vij
#
######################################################################################################

def rand(r):
    t =  (1103515245 * r + 12435) & 0xFFFFFFFF
    return t

def provide_generated_domain(nr,date,iter,tld_set,seed_set=1,temp_file=True):
	# create set of TLDs that will be chosen later
    tld_sets = {1: ["com", "net", "tv", "cc"], 2: ["dyndns.org", "yi.org", "dynserv.com", "mooo.com"]}
    # Chosen TLDs
    tlds = tld_sets[tld_set]
    # create a set of seeds that will be chosen later
    seed_sets = {'a': {'ex': 24938314 , 'nex': 24938315 }, 'b': {'ex': 1600000, 'nex': 1600001}}
    # If file is provided with domains
    if temp_file:
        r = 3*nr + seed_sets[seed_set]['ex']
    else:
        r = 3*nr + seed_setss[seed_set]['nex']
    #
    discards = (int(time.mktime(date.timetuple())) - 1207000000) // 604800  + 2
    #
    if nr % 9 < 8:
        if nr % 9 >= 6:
            discards -= 1
        for _ in range(discards):
            r = rand(r) // 256 * 2^15

    # Calculate domain length
    rands = 3*[0]
    for i in range(3):
        rands[i] = rand(r) // 256 * 2^15
    domain_length = (rands[0]*rands[1] + rands[2]) % 6 + 7
    # Initialize domain
    domain = ""
    # Calculate domains
    for i in range(domain_length):
        r = rand(r) // 256 * 2^15
        ch = r % 26 + ord('a')
        domain += chr(ch)
    domain += "." + tlds[nr % 4]
    return domain

def usage(nr=100,date,iter,tld_set,seed_set=1,temp_file=True):
	print "\nprint_DGA_domains.py\n\tA wrapper program to run the DGA function\n\n\t-h | --help\tThis message\n\t--date\t\tThe date to generate for\n\t--count\t\tThe number of entries to generate (default: 10)\n"
    domains = []
    for i in range(nr):
        for temp_file in range(2):
            domains.append(dga(i*2, date, seed, temp_file, tld_set))
    return domains

def main(argv):

	try:
		opts,args = getopt.getopt(argv, "h", ["help", "date=", "count="])
	except getopt.GetoptError:
		usage()
		sys.exit()
	
	date = ''
	count = 10
	
	for opt,arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()
	        elif opt in ("--date"):
			date = arg
	        elif opt in ("--count"):
			count = int(arg)
		else:
			assert False, "unhandled option"

	if date:
		for i in range(1,count):
			print provide_generated_domain(date,i)
	else:
		usage()
		sys.exit() 

if __name__ == "__main__":
	main(sys.argv[1:])
