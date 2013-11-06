#!/usr/bin/env python
#
### modified date: 2013/07/26
#
import sys, os, getopt
from atm import *

def main():
    def usage():
         print "Usage: v2g -i POSCAR -o xxx.gjf"
         print " -h : help"
         print " -i : input file, ie POSCAR"
         print " -o : output file, ie xxx.gjf, xxx.com"

    try:
        opt_list, args = getopt.getopt(sys.argv[1:], "hi:o:")

    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)
 
    infile = None
    outfile = None
    for o, a in opt_list:
        if o in ('-h'):
            usage()
            sys.exit()
        elif o in ('-i'):
            infile = a
        elif o in ('-o'):
            outfile = a
 
    if infile is None:
        print "No intput file"
        usage()
        sys.exit(2)

    p = POSCAR(infile)
    g = GJF()
    len(sys.argv)
    poscar2gjf(p, g)
#    g.writeGJF()
#       print p.getLattice().getVectors()
    if outfile is None:
        g.writeGJF()
    else:
        g.writeGJF(outfile)

if __name__ == "__main__":
    main()
