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

# PRNG Alogorithm
def rand(r):
    t =  (1103515245 * r + 12435) & 0xFFFFFFFF
    return t

# Returns list of domains
def get_domains(nr, date, seed, tld_set):
    # nr - number of domains - user input
    # date - user input date, default date is current date if no date is provided
    # seed - user input of seed a or b, default is a
    # tld_set - user input of tld_set as 1 or 2, default is 1
    
    # Initialize a list of domains
    domains = []
    for i in range(nr):
        for temp_file in range(2):
            # Append the results of dga algo(individual domain) to domains list
            domains.append(provide_generated_domain(i*2, date, seed, temp_file, tld_set))
    return domains

# DGA Algorithm that returns generated domain
def provide_generated_domain(nr, date, seed_set, temp_file=True, tld_set=1):
    # create set of TLDs that will be chosen later
    tld_sets = {1: ["com", "net", "tv", "cc"], 2: ["dyndns.org", "yi.org", "dynserv.com", "mooo.com"]}
    # Chosen TLDs
    tlds = tld_sets[tld_set]
    # Letters to make domains more spellable
    letters = ["aeiouy", "bcdfghklmnpqrstvwxz"]
    # create a set of seeds that will be chosen later
    seed_sets = {'a': {'ex': 24938314 , 'nex': 24938315 }, 'b': {'ex': 1600000, 'nex': 1600001}}
    # Number to domains to be generated
    nr = int(nr/2)
    # If file is provided with domains
    if temp_file:
        r = 3*nr + seed_sets[seed_set]['ex']
    else:
        r = 3*nr + seed_sets[seed_set]['nex']
    # This takes timestamp to determine how many PRNG cycles to be discarded to
    # make algo time independent.
    discards = (int(time.mktime(date.timetuple())) - 1207000000) // 604800  + 2
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
    # Calculate domain
    for i in range(domain_length):
        if not i % 2:
            offset_1 = 0 if rand(r) & 0x100 == 0 else 1
        offset = (offset_1 + i) % 2
        symbols = letters[offset]
        r = rand(r) // 256 * 2^15
        ch = symbols[r % (len(symbols) - 1)]
        domain += ch
    domain += "." + tlds[nr % 4]
    return domain

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date",help="date for which to generate domains")
    parser.add_argument("-t", "--tld", choices=[1,2], type=int,help="tld set", default=1)
    parser.add_argument('-s', '--seed', choices=['a','b'], default='a')
    args = parser.parse_args()
    if args.date:
        d = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        d = datetime.now()
    for domain in get_domains(1000, d, args.seed, args.tld):
        print(domain)
