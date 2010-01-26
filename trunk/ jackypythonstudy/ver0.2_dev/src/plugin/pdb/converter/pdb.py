# _*_ coding: utf-8 _*_
# Copyright (C)  2009 Takakazu Ishikura

import sys, os

# NAGARA_PATH
# NAGARA_PLUGIN_PATH


# append the nagara's core path
# nagara_plugin_path = os.path.join(os.environ['NAGARA_PATH'], 'core')
# sys.path.append(nagara_plugin_path)

nagara_path = os.environ['NAGARA_PATH'] 
sys.path.append( os.path.join(nagara_path, 'src') )

# sys.path.append

from core.exception  import NagaraException
from core.system import System, Atom, Trajectory, Group
from core.iconverter  import IParser, IFormatter, InvalidFormatException
from core.iconverter  import MoleculeFormatException


class PDBParseError(MoleculeFormatException):
    def __init__(self, line_num=0, column=-1):
        MoleculeFormatException.__init__(self)
        self.line_num = line_num
        self.column = column

        self.pdbformat_list = dict(
            record = "Record name : line[1:6]", #0
            id     = "Atom serial number : line[7:11]",#1
            name   = "Atom name : [line[13:16]",#2
            indi   = "Alternate location indicator : line[17]",#3
            rname  = "Residue name : line[18:20]",#4
            cid    = "Chain identifier : line[22]",#5
            rid    = "Residue sequence number : line[23:26]",#6
            rcode  = "Code for insertion of residues : line[27]",#7
            crd    = ("Orthogonal coordinate for (x, y, z) in Angstroms :"
                      "line[31-38, 39-46, 47-54]"),#8
            # "Orthogonal coordinate for X in Angstroms : line[31-38]",#8
            # "Orthogonal coordinate for Y in Angstroms : line[39-46]",#9
            # "Orthogonal coordinate for Z in Angstroms : line[47-54]",#10
            occ    = "Occupancy : line[55:60]",#9
            bfact  = "Temperature factor (Default=0.0) : line[61:66]",#10
            segid  = "Segment identifier, left-justified : line[73-76]",#11
            elem   = "Element symbol, right-justified : line[77:78]",#12
            charge = "Charge on the atom : line[79:80]",#13
            rest   = "rest of line : line[67:80"#14(-1)
        )

    def __repr__(self):
        message = 'Error ! line : %s , culumn : %s.' % (self.line, self.column)
        return error

                #message = ( "line : " + str(iline) + "\n"
                #            "column error, " + column [icol] )



class PDB_Parser(IParser):

    """
    Class to treat PDB file format.
    This class create the Nagara System object by file name.
    """

    def __init__(self):

        self.__atom_list     = []
        self.__residue_list  = []
        self.__molecule_list = []
        self.__pos_list      = []
        self.__header        = []

        # flags
        self.mol_flag   = False
        self.mol_cnt    = 0
        self.traj_flag  = False
        self.cur_mol    = []

        # create System object
        self.__system = System()

    def set_file_dict(self, file_dict):
        file = file_dict.get('PDB')
        if file:
            self.__file = file
        else:
            raise 



    def get_ndo(self):
        self.parse()
        return self.__system

    def parse(self):
        self.__parse_content()
        self.__file.close()
        self.__to_system()

    def __parse_content(self):
        """Parse the pdb file."""
        for i, line in enumerate(self.__file):
            record = line[0:6].strip()
            
            if record in ('END', 'ENDMDL'):
                if not self.traj_flag:
                    self.traj_flag = True

            elif record in ('ATOM', 'HETATM'):
                try:
                    if not self.traj_flag:
                        self.__parse_atom_line(line)
                    else:
                        self.__parse_traj_line(line)

                except PDBParseError, e:
                    e.line_num = i
                    print e

            elif record == 'TER':
                if not self.mol_flag:
                    self.mol_flag = True
                    # mol = [ r for r in self.residues ]
                    mol = self.__residue_list
                    self.mol_cnt += 1
                    self.__molecule_list.append(
                        Group(name='Mol'+str(self.mol_cnt), child_list=mol)
                    )
                else:
                    mol = self.cur_mol.append(self.residues[-1])
                    self.mol_cnt += 1
                    self.__molecule_list.append(
                        Group(name='Mol'+str(self.mol_cnt), childs=mol)
                    )
                    self.cur_mol = []

            elif record in ('MASTER', 'CONECT'):
                pass

            else: # for Header
                self.__header.append(line[6:])

        if __debug__: pass
            # print __name__
            # for res in self.residues:
            #     print res, res.getAtoms()

    def __parse_atom_line(self, line):
        """Parse one ATOM record line in PDB format."""
        try:
            # for atom
            atom = Atom(
                id = int(line[6:11]), # icol=1
                name = line[12:16].strip(), # icol=2
                # icol = 3; atom.alt_id = line[16]
            )
            occ = line[56:60].strip()
            if occ: atom.occupancy = float(occ)

            bfact = line[60:66].strip()
            if bfact: atom.bfactor = float(bfact)

            elem = line[76:78].strip()
            if elem:
                atom.elem = elem
            else:
                atom.elem = line[13]

            charge = line[78:80].strip()
            if charge: atom.charge = float(charge)

            atom.rest = line[66:80].strip()

            self.__atom_list.append(atom)

            # for coordinate
            pos = (
                float(line[30:38]), # icol=8
                float(line[38:46]), # icol=9
                float(line[46:54])  # icol=10
            ) 
            self.__pos_list.append(pos)

            # for residue
            resid = int(line[22:26]) # icol=6

            if not self.__residue_list:
                # first residue
                res = Group(
                    id = resid,
                    name = line[17:20].strip(), # icol=4
                    code = line[26:27],  # icol=7
                )
                res.atoms.append(atom)
                self.__residue_list.append(res)

            elif self.__residue_list[-1].id != resid:
                res = Group(
                    id = resid,
                    name = line[17:20].strip(), # icol=4
                    code = line[26:27], # icol=7
                )
                
                res.append_atom(atom)
                self.__residue_list.append(res)

                if self.mol_flag:
                    self.cur_mol.append(res)

            else:
                self.__residue_list[-1].atoms.append(atom)

            self.cur_mol.append(self.__residue_list[-1])

            # if __debug__: print res, res.atoms


        except ValueError:
            raise PDBParseError(icol=1)

    def __parse_traj_line(self, line):
        """Parse one ATOM record line to extract coordinates."""
        try:
            # for coordinate
            pos = (
                float(line[30:38]), # icol=8
                float(line[38:46]), # icol=9
                float(line[46:54])  # icol=10
            ) 
            self.__pos_list.append(pos)

        except ValueError:
            raise PDBParseError(icol=1)

    def __to_system(self):
        """Convert internally from this class to System class."""
        self.__system.atoms = self.__atom_list
        self.__system.append_group_list('Residues', self.__residue_list)
        if self.mol_flag:
            self.__system.append_group_list('Molecules', self.__molecule_list)

        traj = Trajectory(crd_list=[self.__pos_list])
        self.__system.trajectory = traj


#class MULTI_PDB_Parser(IParser):
#
#    """
#    Class to treat PDB file format.
#    This class create the Nagara System object by file name.
#    """
#
#    def __init__(self, file):
#        self.__file = file
#
#        self.__atom_list      = []
#        self.__residue_list   = []
#        self.__molecule_list  = []
#        self.__trajectory = [[]]
#        self.__header     = []
#
#        # flags
#        self.mol_flag   = False
#        self.mol_cnt    = 0
#        self.traj_flag  = False
#        self.cur_mol    = []
#
#        # create System object
#        dirname, basename = os.path.split(filename)
#        name, suffix = basename.rsplit('.',1)
#        self.__system = system.System(name)
#
#    def to_ndo(self):
#        self.parse()
#        return self.__system
#
#    def parse(self):
#        self.__parse_content()
#        self.__file.close()
#        self.__to_system()
#
#    def __parse_content(self):
#        """Parse the pdb file."""
#        for i, line in enumerate(self.file):
#            record = line[0:6].strip()
#            
#            if record in ('END', 'ENDMDL'):
#                if not self.traj_flag:
#                    self.traj_flag = True
#
#            elif record in ('ATOM', 'HETATM'):
#                try:
#                    if not self.traj_flag:
#                        self.__parseAtomLine(line)
#                    else:
#                        self.__parseTrajLine(line)
#
#                except PDBParseError, e:
#                    e.line_num = i
#                    print e
#
#            elif record == 'TER':
#                if not self.mol_flag:
#                    self.mol_flag = True
#                    # mol = [ r for r in self.residues ]
#                    mol = self.__residue_list
#                    self.mol_cnt += 1
#                    self.__molecule_list.append(
#                        Group(name='Mol'+str(self.mol_cnt), childs=mol)
#                    )
#                else:
#                    mol = self.cur_mol.append(self.residues[-1])
#                    self.mol_cnt += 1
#                    self.__molecule_list.append(
#                        Group(name='Mol'+str(self.mol_cnt), childs=mol)
#                    )
#                    self.cur_mol = []
#
#            elif record in ('MASTER', 'CONECT'):
#                pass
#
#            else: # for Header
#                self.__header.append(line[6:])
#
#        if __debug__: pass
#            # print __name__
#            # for res in self.residues:
#            #     print res, res.getAtoms()
#
#    def __parse_atom_line(self, line):
#        """Parse one ATOM record line in PDB format."""
#        try:
#            # for atom
#            atom = Atom(
#                id = int(line[6:11]), # icol=1
#                name = line[12:16].strip(), # icol=2
#                # icol = 3; atom.alt_id = line[16]
#            )
#            occ = line[56:60].strip()
#            if occ: atom.occupancy = float(occ)
#
#            bfact = line[60:66].strip()
#            if bfact: atom.bfactor = float(bfact)
#
#            elem = line[76:78].strip()
#            if elem:
#                atom.elem = elem
#            else:
#                atom.elem = line[13]
#
#            charge = line[78:80].strip()
#            if charge: atom.charge = float(charge)
#
#            atom.rest = line[66:80].strip()
#
#            self.__atom_list.append(atom)
#
#            # for coordinate
#            pos = (
#                float(line[30:38]), # icol=8
#                float(line[38:46]), # icol=9
#                float(line[46:54])  # icol=10
#            ) 
#            self.__trajectory[-1].append(pos)
#
#            # for residue
#            resid = int(line[22:26]) # icol=6
#
#            if not self.__residue_list:
#                # first residue
#                res = Group(
#                    id = resid,
#                    name = line[17:20].strip(), # icol=4
#                    code = line[26:27],  # icol=7
#                )
#                res.append(atom)
#                self.__residue_list.append(res)
#
#            elif self.__residue_list[-1].id != resid:
#                res = Group(
#                    id = resid,
#                    name = line[17:20].strip(), # icol=4
#                    code = line[26:27], # icol=7
#                )
#                
#                res.append_atom(atom)
#                self.__residue_list.append(res)
#
#                if self.mol_flag:
#                    self.cur_mol.append(res)
#
#            else:
#                self.__residue_list[-1].append(atom)
#
#            self.cur_mol.append(self.residues[-1])
#
#            # if __debug__: print res, res.atoms
#
#
#        except ValueError:
#            raise PDBParseError(icol=1)
#
#    def __parse_traj_line(self, line):
#        """Parse one ATOM record line to extract coordinates."""
#        try:
#            # for coordinate
#            pos = (
#                float(line[30:38]), # icol=8
#                float(line[38:46]), # icol=9
#                float(line[46:54])  # icol=10
#            ) 
#            self.__trajectory[-1].append(pos)
#
#        except ValueError:
#            raise PDBParseError(icol=1)
#
#    def __to_system(self):
#        """Convert internally from this class to System class."""
#        self.__system.atoms = self.__atom_list
#        self.__system.append_groups('Residues', self.__residue_list)
#        if self.mol_flag:
#            self.__system.append_groups('Molecules', self.__molecule_list)
#        traj = Trajectory(crds=self.__trajectory)
#        self.__system.trajectory = traj


import cStringIO as sio
class PDB_Formatter(IFormatter):

    def __init__(self):
        self.__atom_list      = []
        self.__residue_list   = []
        self.__molecule_list  = []
        self.__trajectory = [[]]
        self.__header     = []

        # flags
        self.mol_flag   = False
        self.mol_cnt    = 0
        self.traj_flag  = False
        self.cur_mol    = []

    def set_ndo(self, ndo):
        self.__system = ndo

    def get_file_dict(self):
        """Return the file object."""
        file = sio.StringIO()
        # print self.__parse(self.__system.get_crd())
        file.write(self.__system.header)
        file.write(self.__parse(self.__system.get_crd()))
        file.seek(0)
        return {'PDB': file}

    def __parse(self, crd):
        """Return the pdb-formatted data of the molecules from the crd."""
        pdblines = []
        i = 0
        for res in self.__system.get_group_list('Residues'):
            rname = res.name
            rid   = res.id
            for atom in res.atoms:
                id = atom.id
                x, y, z = crd[i]
                # old style formatting: version <= 2.5 
                # pdbline = (
                #     "ATOM  %5d %4s %3s  %4d    %8.3f%8.3f%8.3f%6.2f%6.2f"
                #     % (id, atom.name, rname, rid, x, y, z, atom.occ, atom.bfact)
                # )
                # new style formatting: version >= 2.6 
                line_template = (
                    'ATOM  {id:>5} {name:>4} {rname:>3}  {rid:>4}'
                    '{x:8.3}{y:8.3}{z:8.3}{occ:6.2}{bfact:6.2}'
                )
                pdbline = line_template.format(
                    id=id, name=atom.name, rname=rname, rid=rid,
                    x=x, y=y, z=z, occ=atom.occ, bfact=atom.bfact
                )
                pdblines.append(pdbline)
                i += 1

        return '\n'.join(pdblines)

    def __parse_traj(self):
        """Return the pdb-formatted trajectory data with pdb format."""
        frames = []
        for crd in self.__system.get_crd():
            frames.append(self.__toPDB(crd))

        contents = '\nEND\n'.join(frames)
        contents += '\nEND'
        return contents


#class MULTI_PDB_Formatter(IFormatter):
#
#    def __init__(self):
#
#
#
#        self.__filename   = filename
#        self.__file       = None
#        self.__atom_list      = []
#        self.residues   = []
#        self.molecules  = []
#        self.trajectory = [[]]
#        self.header     = []
#
#        # flags
#        self.mol_flag   = False
#        self.mol_cnt    = 0
#        self.traj_flag  = False
#        self.cur_mol    = []
#
#        # create System object
#        dirname, basename = os.path.split(filename)
#        name, suffix = basename.rsplit('.',1)
#        self.system = system.System(name)
#
#
#
#    def write(self, system):
#        """Write the system molecules data into a file."""
#        self.__fromSystem(system)
#        try:
#            self.file = open(self.filename, 'w')
#            self.file.write(self.__toPDB(self.trajectory[0]))
#        except IOError, error:
#            print error
#        finally:
#            self.file.close()
#    pass
#
#
#    def read(self):
#        """Read a pdb file and return a system data."""
#        try:
#            self.file = open(self.filename, 'r')
#            self.__parseContent()
#        except IOError, error:
#            print error
#        finally:
#            self.file.close()
#
#        # if __debug__:
#        #     for res in self.residues:
#        #         print res, res.getAtoms()
#
#        self.__toSystem()
#        # if __debug__:
#        #     print self.system
#        return self.system
#
#    def __fromSystem(self, system):
#        """Convert internally from the System class to this class."""
#        self.atoms = system.getAtoms()
#        self.residues = system.getGroups('Residues')
#        self.trajectory = system.getCrds()
#        self.header     = system.getHeader()
#
#    def __toPDB(self, crds):
#        """Return the pdb-formatted data of the molecules from the crds."""
#        pdblines = []
#        for res in self.residues:
#            rname = res.name
#            rid   = res.id
#            for atom in res.getAtoms():
#                id = atom.id
#                x, y, z = crds[id-1]
#                pdbline = (
#                    "ATOM  %5d %4s %3s  %4d    %8.3f%8.3f%8.3f%6.2f%6.2f"
#                    % (id, atom.name, rname, rid, x, y, z, atom.occ, atom.bfact)
#                )
#                pdblines.append(pdbline)
#        return '\n'.join(pdblines)
#
#    def __toPDBs(self):
#        """Return the pdb-formatted trajectory data with pdb format."""
#        frames = []
#        for crds in self.trajectory:
#            frames.append(self.__toPDB(crds))
#
#        contents = '\nEND\n'.join(frames)
#        contents += '\nEND'
#        return contents




def main():
    nagara_path = os.environ['NAGARA_PATH']
    pdb_file = os.path.join(
        nagara_path, 'examples/structures/1HEW.pdb'
    )

    # print os.path.exists(pdb_file)
    # print pdb_file


    
    file = open(pdb_file, 'r')
    parser = PDB_Parser()
    parser.set_file_dict({'PDB': file})
    system = parser.get_ndo()
    #print '*'*80
    #for pos in system.get_crd():
    #    print pos
    # print len(system.get_crd())
    # print len(system.atoms)
    #print '*'*80

    # print type(system.trajectory)
    # print system.trajectory.getCrds()
    # file2 = PDB_Formatter(system).to_file()

    # for atom in system.atoms:
    #     print(atom)

    # print system
    formatter = PDB_Formatter()
    formatter.set_ndo(system)
    pdb_file_dict = formatter.get_file_dict()

    print pdb_file_dict.get('PDB').read()


    

    # for t in a.getCrds():
    #     print(t)
    

if __name__ == '__main__':
    main()

