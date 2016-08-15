import subprocess
import sys
import socket

######################################################################################################
#
#  print_hostname.py
#    Copyright 2016 - Matthew Norris
#
#  Simple Python boilerplate to wrap the get_hostname() function in a calling program.
#    Please modify as need be, but describe all changes in your writeup.
#
#  Last Modified: 20160126 - Divya Nayak
#
######################################################################################################


def main():
    print "\nThe hostname is:\n" + socket.gethostname() + "\n"

if __name__ == "__main__":
	main()
