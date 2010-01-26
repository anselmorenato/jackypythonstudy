# _*_ coding: utf-8 _*_
# Copyright (C)  2009 Takakazu Ishikura

import sys, os

# append the nagara's library path
if __name__ == '__main__':
    sys.path.append('../../..')
from core import system
from core.exception  import NagaraException
from core.systeminfo import Atom, Trajectory, Group
from core.converter  import IParser, IFormatter, MoleculeFormatException
#  
#  XYZ Format
#  
#  Format:
#  60 
#  C60 fullerene 
#  C +2.226730 +0.594920 +2.684200 
#  ... 
#  C +0.023000 -0.074940 -3.552420 
#  
class XYZ_Parser(IParser):

    def __init__(self, file):
        """Constructor."""
        self.__file = file
        self.__system = system.System()

        self.pdbfile    = None 
        self.atoms      = [] #: [Atom]
        self.crds       = [] #: [(Float,Float,Float)]
        self.trajectory = [[]] #: [[(Float,Float,Float)]]
        self.residues   = [] #: [Group]
        self.molecules  = [] #: [Group]
        pass

    def __str__(self):
        """Return the pdb-formatted data of the molecules."""
        return self.__tostr(self.crds) 


    def to_ndo(self):
        pass

    def parse(self):
        self.__parseContent(self.__file)
        self.__file.close()

    def read(self, filename):
        """Read a xyz file and store the molecule data."""
        assert filename.split('.')[-1] in ['xyz', 'XYZ'], \
               'Error occured, reading xyz file'
        try:
            self.xyzfile = open(filename, 'r')
            self.__parseContent(xyzfile)
        except IOError, error:
            print error
        finally:
            xyzfile.close()

    def __parseContent(self):
        """Parse the xyz file."""
        file = self.__file
        if not self.molecules:
            self.molecules.append(Molecule())

        natm = int(file.next())
        self.__system.header = file.next().strip()

        for i, line in enumerate(xyzfile):
            cols = line.split()
            # Atom information
            atom = Atom(
                id = i,
                elem = cols[0],
                name = cols[0] + str(i),
            )
            # for coordinate
            crd = ( float(line[1]), float(line[2]), float(line[3]) ) 
            self.__system.crds.append(crd)


class XYZ_Formatter(IFormatter):
    def write(self, ndo):
        """Write the system molecules data to a file."""
        self.__system = odn
        xyzfile = open(filename, 'w')
        xyzfile.write(str(len(self.atoms)))
        xyzfile.write(self.header)
        xyzfile.write(self)


    def __str__(self):
        """Return the pdb-formatted data of the molecules."""
        return self.__tostr(self.crds) 

    def __repr__(self):
        """Return the data of the molecules in detail."""
        pass

    def __tostr(self, crds):
        """Return the pdb-formatted data of the molecules from the crds."""
        xyzlines = []
        for atom in self.atoms:
            elem = atom.elem
            x, y, z = self.crds[id-1]
            xyzline = ( "%3s   %8.3f %8.3f %8.3f" % (elem, x, y, z) )
            xyzlines.append(xyzline)

        return '\n'.join(xyzlines)


def main():
    pass

if __name__ == '__main__':
    main()

