import sys
import argparse
import subprocess

def execute_program(filepath, argstr):
    return programstdout(filepath, argstr)

def programstdout(filepath, argstr):
    subprocess.call("python %s -s %s" %(filepath, argstr), shell=True)
    #return sys.stdout.write("This string is from current program - %s" %argstr)

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filepath",help="give absolute path of python file")
    parser.add_argument("-s", "--argstr", type=str, nargs='+', help="give string arguments")
    args = parser.parse_args()
    execute_program(args.filepath, args.argstr)
