#!/usr/bin/env python
#
### modified date: 2013/10/23
#

from atm import *
import copy
import math
import os, getopt
import sys

class Vector:
    def __init__(self, x, y, z):
        self.setBasis(x, y, z)

    def setBasis(self, x, y, z):
        self._x_ = x
        self._y_ = y
        self._z_ = z

    def getBasis(self):
        return (self._x_, self._y_, self._z_)

    def normalized(self):
        length = self.getLength()
        if length == 0.0:
            print "Don't normalized"
            return Vector(self._x_, self._y_, self._z_)
        else:
            return Vector(self._x_ / length, self._y_ / length, self._z_ / length)

    def getLength(self):
        self._length_ = self._x_ * self._x_ + self._y_ * self._y_ + self._z_ * self._z_
        self._length_ = math.sqrt(self._length_)
        return self._length_

    def getAngle(self, vector):
        angle = math.acos(self.dot(vector) / self.getLength() / vector.getLength() )
        return math.degrees(angle)

    def dot(self, vector):
        return self._x_ * vector._x_ + self._y_ * vector._y_ + self._z_ * vector._z_

    def cross(self, vector):
        x = self._y_ * vector._z_ - self._z_ * vector._y_
        y = self._z_ * vector._x_ - self._x_ * vector._z_
        z = self._x_ * vector._y_ - self._y_ * vector._x_
        return Vector(x, y, z)

    def __str__(self):
        return "%f, %f, %f" %(self._x_, self._y_, self._z_)

    def __add__(self, vector):
        return Vector(self._x_ + vector._x_, self._y_ + vector._y_, self._z_ + vector._z_)

    def __sub__(self, vector):
        return Vector(self._x_ - vector._x_, self._y_ - vector._y_, self._z_ - vector._z_)

    def __mul__(self, n):
        return Vector(n * self._x_, n * self._y_, n * self._z_)

# Rotation operator
#      cosQ+Nx^2(1-cosQ)        NxNy(1-cosQ) - Nz*sinQ   NxNz(1-cosQ) + Ny*sinQ     x1   x2   x3
# R =  NyNz(1-cosQ) + Nz*sinQ   cosQ + Ny^2(1-cosQ)      NyNz(1-cosQ) - Nz*sinQ  =  y1   y2   y3
#      NzNx(1-cosQ) - Ny*sinQ   NzNy(1-cosQ) + NxsinQ    cosQ + Nz^2(1-csoQ)a       z1   z2   z3
#
# angle degree to radian
#    def rotate(axis_vector, angle):
    def rotate(self, axis_vector, angle):
        angle = math.radians(angle)
        x1 = math.cos(angle) + axis_vector._x_ * axis_vector._x_ * (1 -math.cos(angle) )
        x2 = axis_vector._x_ * axis_vector._y_ * (1 - math.cos(angle) ) - axis_vector._z_ * math.sin(angle)
        x3 = axis_vector._x_ * axis_vector._z_ * (1 - math.cos(angle) ) + axis_vector._y_ * math.sin(angle)

        y1 = axis_vector._y_ * axis_vector._z_ * (1- math.cos(angle) ) + axis_vector._z_ * math.sin(angle)
        y2 = math.cos(angle) + axis_vector._y_ * axis_vector._y_ * (1- math.cos(angle) )
        y3 = axis_vector._y_ * axis_vector._z_ * (1- math.cos(angle) ) - axis_vector._z_ * math.sin(angle)

        z1 = axis_vector._z_ * axis_vector._x_ * (1- math.cos(angle) ) - axis_vector._y_ * math.sin(angle)
        z2 = axis_vector._z_ * axis_vector._y_ * (1- math.cos(angle) ) + axis_vector._x_ * math.sin(angle)
        z3 = math.cos(angle) + axis_vector._z_ * axis_vector._z_ * (1- math.cos(angle) )

        x = x1 * self._x_ + x2 * self._y_ + x3 * self._z_
        y = y1 * self._x_ + y2 * self._y_ + y3 * self._z_
        z = z1 * self._x_ + z2 * self._y_ + z3 * self._z_
        return Vector(x, y, z)


def lineScan(poscar, distance, nstep, ref_indexes, mot_indexes, grp_indexes):
    ref_atm = poscar._atoms_[ref_indexes[0]]
    mot_atm = poscar._atoms_[mot_indexes[0]]
    x1, y1, z1 = ref_atm.getCoordinate()
    x2, y2, z2 = mot_atm.getCoordinate()
    vec = Vector(x2-x1, y2-y1, z2-z1)
    vec = vec.normalized()

    poscars = []
    tmpIndexes = mot_indexes + grp_indexes

    for i in xrange(nstep + 1):
        v = vec*i*distance
        tmpPOSCAR = copy.deepcopy(poscar)
#        x, y, z = v.getBasis()
#        tmpPOSCAR.setAtomCoordinate(mot_indexes[0], x2+x, y2 + y, z2 + z)

        for j in grp_indexes:
            tmpX, tmpY, tmpZ = poscar._atoms_[j].getCoordinate()
            tmpPOSCAR.setAtomCoordinate(j, tmpX+x, tmpY+y, tmpZ+z)
#            tmpX, tmpY, tmpZ = poscar._atoms_[j-1].getCoordinate()
#            tmpPOSCAR.setAtomCoordinate(j-1, tmpX+x, tmpY+y, tmpZ+z)

#        print i, x, y, z
        poscars.append(tmpPOSCAR)
    return poscars


def angleScan(poscar, angle, nstep, ref_indexes, mot_indexes, grp_indexes):
# ref atm, fix/basic atm, mot atm
    ref_atm = poscar._atoms_[ref_indexes[0] ]
    bas_atm = poscar._atoms_[ref_indexes[1] ]
    mot_atm = poscar._atoms_[mot_indexes[0] ]

    x1, y1, z1 = ref_atm.getCoordinate()
    x2, y2, z2 = bas_atm.getCoordinate()
    x3, y3, z3 = mot_atm.getCoordinate()
    vec1 = Vector(x1 - x2, y1 - y2, z1 - z2)
    vec2 = Vector(x3 - x2, y3 - y2, z3 - z2)
    normal_vector = vec1.cross(vec2)

    poscars = []
    tmpIndexes = mot_indexes + grp_indexes

    for i in xrange(nstep):
        a = i * angle
        tmpPOSCAR = copy.deepcopy(poscar)

#        for j in grp_indexes:
        for j in tmpIndexes:
            tmpX, tmpY, tmpZ = poscar._atoms_[j].getCoordinate()
            tmpV = Vector(tmpX - x2, tmpY - y2, tmpZ - z2)
            tmpV = tmpV.rotate(normal_vector, a)
            tmpX, tmpY, tmpZ = tmpV.getBasis()
            tmpPOSCAR.setAtomCoordinate(j, tmpX + x2, tmpY + y2, tmpZ + z2)
        poscars.append(tmpPOSCAR)
    return poscars


def makeScanJob(poscars):
    i = 0
    for p in poscars:
        dir = "0%d" %(i) if i < 10 else "%2d" %(i)
        os.mkdir(dir)
        print os.path.join(dir, 'POSCAR')
        p.writePOSCAR(os.path.join(dir, 'POSCAR'))
        i = i + 1
    pass


def main():
    def usage():
        print "Usage: vscan -i POSCAR -r 1   -m 2 -g 3,4,5 -n 4 -d 1.0     # line  scan"
        print "       vscan -i POSCAR -r 1,2 -m 3 -g 4,5,6 -n 4 -d 30.0    # angle scan"
        print " -h : help"
        print " -i : input file, POSCAR"
        print " -r : reference atoms"
        print " -m : motion atom"
        print " -g : atom with motion atom"
        print " -n : number of step"
        print " -d : displacement (distance/angle)"

    def checkFile(f):
        if os.path.exists(f):
            return os.path.abspath(f)
        print "File: " + f + " didn't exist."
        sys.exit(2)
        return False

    try:
        opt_list, args = getopt.getopt(sys.argv[1:], "hi:r:m:g:n:d:")

    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)

    infile = None
    r_indexes = None
    m_indexes = None
    g_indexes = None
    nstep = None
    displacement = None
    for o, a in opt_list:
        if o in ('-h'):
            usage()
            sys.exit()
        elif o in ('-i'):
            infile = a
        elif o in ('-r'):
#            r_indexes = a
            r_indexes = [int(i)-1 for i in a.split(',')]
        elif o in ('-m'):
#            m_indexes = a
            m_indexes = [int(i)-1 for i in a.split(',')]
        elif o in ('-g'):
#            g_indexes = a
            g_indexes = [int(i)-1 for i in a.split(',')]
        elif o in ('-n'):
            nstep = int(a)
        elif o in ('-d'):
            displacement = float(a)

    if infile is None:
        print "Intput file: "
        infile = sys.stdin.readline().rstrip()
#        infile = checkFile(sys.stdin.readline().rstrip())
    poscar = POSCAR(infile)

    if r_indexes is None:
        print "reference atoms: "
        r_indexes = sys.stdin.readline().rstrip()
        r_indexes = [int(i)-1 for i in r_indexes.split(',')]

    if m_indexes is None:
        print "motion atom: "
        m_indexes = sys.stdin.readline().rstrip()
        m_indexes = [int(i)-1 for i in m_indexes.split(',')]

    if g_indexes is None:
        print "group atoms: "
        g_indexes = sys.stdin.readline().rstrip()
        g_indexes = [int(i)-1 for i in g_indexes.split(',')]

    print r_indexes, m_indexes, g_indexes

    if nstep is None:
        print "number of step: "
        nstep = sys.stdin.readline().rstrip()
        nstep = int(nstep)

    if displacement is None:
        print "displacement distance/angle: "
        displacement = sys.stdin.readline().rstrip()
        displacement = float(displacement)

    if len(r_indexes) == 1:
#    line scan
        poscars = lineScan(poscar, displacement, nstep, r_indexes, m_indexes, g_indexes)
    elif len(r_indexes) == 2:
#    angle scan
        poscars = angleScan(poscar, displacement, nstep, r_indexes, m_indexes, g_indexes)
    else:
        print "input error of reference atom"
        sys.exit(2)

    makeScanJob(poscars)


if __name__ == "__main__":
    main()
#    file = "iPOSCAR"
#    poscar = POSCAR(file)

#    dihedral angle split
#   r: reference atom
#   m: motion atom
#   m_angle: motion angle
#   nstep: number of step
#   input
#    ref_indexes = [0, 1, 2]
#    mot_indexes = [3]
#    grp_indexes = [4, 5]
#    nstep = 8
#    angle = 90.0
#
