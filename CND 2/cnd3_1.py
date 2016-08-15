import sys
import argparse

def argmethod(argstr):
    number_of_arguments = len(argstr)
    return str(sys.stdout.write("The number of arguments are - %d" %number_of_arguments))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--argstr", type=str, nargs='+', help="give string arguments")
    args = parser.parse_args()
    argmethod(args.argstr)
