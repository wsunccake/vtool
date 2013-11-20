#!/usr/bin/env python
#
### modified date: 2013/11/21
#

from atm import *

__author__ = ""
__date__ = "2013/11/21"

__version__ = "$Revision: 0.1$"


class GJF:
    """ create/read Gaussian input file """
    def __init__(self, filename = None, comment = None):
        """ 
        """
        self._specs_ = []
#        self._option_ = ''
        self.setOption()
        self.setComment()
        self.setCharge()
        self.setSpin()
        self._atoms_ = []
        self._elements_ = []
        self._element_lists_ = []
        self._numbers_ = []
#        self._lattices_ =  []
        if not(filename is None):
            self.readGJF(filename)

    def addAtom(self, atom):
        self._atoms_.append(atom)

    def getAtoms(self):
        return self._atoms_

    def getLattice(self):
        return self._lattice_

    def setLattice(self, vectors, latticeConstant = 1.0):
        v1 = vectors[0]
        v2 = vectors[1]
        v3 = vectors[2]
        self._lattice_ = Lattice(v1, v2, v3, latticeConstant)

    def sortAtoms(self):
#        self._atoms_ = sorted(self._atoms_, key=lambda atom: atom._element_)
        self._atoms_ = sorted(self._atoms_, key=lambda atom: (atom._element_, atom._zCoordinate_) )

    def getOption(self):
        return self._option_

    def setOption(self, opt = '# opt freq hf/3-21g'):
        self._option_ = opt

    def setComment(self, comment = "This line is comment"):
        self._comment_ = comment

    def getComment(self):
        return self._comment_

    def getCharge(self):
        return self._charge_

    def setCharge(self, charge = 0):
        self._charge_ = charge

    def getSpin(self):
        return self._spin_

    def setSpin(self, spin = 1):
        self._spin_ = spin

    def readGJF(self, filename):
        """ read Gaussian input file """
        f = open(filename, "r")
        i = 0
        for l in f.readlines():
            if l[0] == "%":
                self._specs_.append(l.rstrip() )
                continue
            elif l[0] == "#":
#                self._option_ = l.rstrip()
                self.setOption(l.rstrip() )
                continue 
            elif l.strip() == "":
                continue
            elif len(l.split()) == 4:
                 atom = Atom(l.split()[0], float(l.split()[1]), float(l.split()[2]), float(l.split()[3]) )
                 self.addAtom(atom)
        self._checkLattice_()
        self.sortAtoms()

    def writeGJF(self, filename = None):
        """ write Gaussian input file """
        output = ''
        for l in self._specs_:
            output += l + "\n"
        output += self._option_ + "\n\n"
        output += self._comment_ + "\n\n"
        output += '%i %i\n' %(self._charge_, self._spin_)
        for a in self._atoms_:
            output += "%-2s" % a.getElement() + "       %13.8f    %13.8f    %13.8f\n" % a.getCoordinate()

        # setup output
        if filename == None:
            print output
        else:
            f = open(filename, "wb")
            f.write(output)
            f.close()

    def _checkLattice_(self):
        i = 0
        lattice_indexes = []
        vectors = []
        for atom in self._atoms_:
            if atom.getElement() == "Tv":
#                (x, y, z) = atom.getCoordinate()
#                vectors.append([x, y, z])
                vectors.append(atom.getCoordinate() )
                lattice_indexes.append(i)
            i += 1
        lattice_indexes.reverse()
        for l in lattice_indexes:
            self._atoms_.pop(l)
#        self._lattice_ = Lattice(vectors[0], vectors[1], vectors[2])
        self.setLattice(vectors)

if __name__ == "__main__":
    import sys
    import os

    pass