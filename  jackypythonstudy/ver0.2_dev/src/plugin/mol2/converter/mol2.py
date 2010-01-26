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


"""Read mol2 file and put the molecule data.

file_name -- mol2 file name : String
""" 
class MOL2_Parser(IParser):
    pass


class MOL2_Formatter(IFormatter):
    pass


def main():
    pass

if __name__ == '__main__':
    main()

