#  -*- encoding: utf-8 -*-

# standard modules
import re
import operator
import copy

# Nagara modules
import exception


ATMNUM_ELEM_DICT = {
    1 : ('H',  'h'),
    2 : ('He', 'he', 'HE'),
    6 : ('C',  'c'),
    7 : ('N',  'n'),
    8 : ('O',  'o'),
    9 : ('F',  'f'),
    11: ('Na', 'na', 'NA', 'Na+', 'na+', 'NA+'),
    14: ('Si', 'si', 'SI'),
    15: ('P',  'p'),
    16: ('S',  's'),
    17: ('Cl', 'cl', 'CL', 'Cl-', 'cl-', 'CL-'),
    18: ('Ar', 'ar', 'AR'),
    19: ('K',  'k' , 'K+', 'k+'),
    20: ('Ca', 'ca', 'CA', 'Ca+', 'ca+', 'CA+'),
}

ELEM_ATMNUM_DICT = {}
for an, elem_list in ATMNUM_ELEM_DICT.items():
    for e in elem_list:
        ELEM_ATMNUM_DICT[e] = an


class SystemException(exception.NagaraException): pass

class GroupKeyError(SystemException): pass

class System(object):

    def __init__(self, name=''):
        self.__header     = ""    # PDB header
        self.__title      = ""    # Title of this system
        self.__name       = name  # Name for this system
        self.__atom_list  = []    # All of atoms in this system : [Atom]
        self.__group_list = {}    # All of groups in this system : {type:Group}
        self.__trajectory = None  # Trajectory info : [Trajectory]

    # def __str__(self):
    #     name_list = [ atom.name for atom in self.__atom_list]
    #     return names

    # def __str__(self):
    #     """Return the pdb-formatted data of the molecules."""
    #     return self.__tostr(self.trajectory[0]) 

    # def __repr__(self):
    #     """Return the data of the molecules in detail."""
    #     pass

    # name property
    def get_name(self):
        """Get the system name."""
        return self.__name
    def set_name(self,name):
        """Set the name to system object."""
        self._name = __name
    name = property(get_name, set_name)

    def write_molecule(self, filename):
        """"""
        pass
                                       
    @property
    def size(self):
        """Return the number of atoms in the system."""
        return len(atoms)

    def get_group_type_list(self):
        """Return the information for group type and name."""
        pass

    def search(self): pass
    
    def get_atominfo(self): pass 

    def position(self):
        """Return the position of atom specified by argument."""
        pass

    def make_group(self):
        pass

    def make_group_by_group(self):
        pass

    def __make_group_by_res(self, group_name, name_list):
        """Make a group named by group_name from the residue groups."""
        if group_name not in self.groups:
            res_group = self.group['Residue'].getChildGrps()
            groups = [ res for res in res_groups if res.name in name_list ]
            new_group = Group(parent=[], id=-1, type=group_name, childs=groups)
            self.groups[group_name] = new_group

    def __make_group_by_atom(self, group_name, name_list):
        """Make a group named by group_name."""
        pass

    def make_group_by_keyword(self, keyword):
        """Make user defined groups by keyword."""
        pass

    def make_protein_group(self):
        """Make a protein group from residue groups."""
        prot_names = [
            'Ala', 'Arg', 'Asn', 'Asp', 'Cys', 'Gln', 'Glu',
            'Gly', 'His', 'Ile', 'Leu', 'Lys', 'Met', 'Phe',
            'Pro', 'Ser', 'Thr', 'Trp', 'Tyr', 'Val'
        ]
        self.__make_group_by_res('Protein', prot_names)

    def make_water_group(self):
        """Make water group from the residue type groups."""
        waters_names = ['SPC', 'TIP3', 'TIP4', 'TIP5', 'WAT']
        self.__mkGroupByRes('Water', water_names)

    def make_CA_group(self):
        """Make CA group from All atoms."""
        if 'CA' not in self.groups:
            if 'Protein' not in self.groups:
                self.mkProteinGrp()
            atoms = self.groups('Protein').getChildGrps().getAtoms
            groups = [ atom for atom in atoms if atom.name == 'CA' ]
            self.mkGroup('CA', groups)

    def make_solvent_group(self):
        """Make a solvent group."""
        solv_names = ['SPC', 'TIP3', 'TIP4', 'TIP5', 'WAT', 'Na+', 'Cl-']
        self.__mkGroupByRes('Solvent', solv_names)

    def get_groupatom_list(self, group_name):
        """Return atoms by the list in the specified group."""
        return self.groups[group_name].atoms

    # property: trajectory
    def get_trajectory(self):
        return self.__trajectory
    def set_trajectory(self, trajectory):
        """Set trajectory."""
        self.__trajectory = trajectory
    trajectory = property(get_trajectory, set_trajectory)
    
    def get_crd(self):
        """Get the first frame of the trajectory."""
        return self.__trajectory.get_crd_list()

    # atoms property
    def get_atom_list(self):
        """Get atoms object."""
        return self.__atom_list
    def set_atom_list(self, atom_list):
        """Set atoms as new list."""
        self.__atom_list = atom_list
    atoms = property(get_atom_list, set_atom_list)
    
    def append_group_list(self, name, group_list):
        """Set groups as a list and its name."""
        self.__group_list[name] = group_list

    def get_group_list(self, group_name):
        """Get the group list by group name."""
        assert group_name in self.__group_list.keys(), group_name
        try:
            group_list = self.__group_list[group_name]
        except KeyError:
            raise GroupKeyError()
        return group_list

    def get_group_name_list(self):
        """Get the all group names."""
        return self.__group_list.keys()


    def copy(self):
        """Return the copied system object."""
        return copy.copy(self)

    @property
    def header(self):
        """Return the header of system data."""
        return self.__header

#-------------------------------------------------------------------------------

class Atom(object):

    def __init__(self, id=-1, name=None, type=None, elem=None,
                 charge=0.0, occ=0.0, bfact=0.0,
                 connect_dict=None, group_list=None, rest_str=None):
        self.id = id      # Atom number of sub unit : Int
        self.name = name  # Atom name : String
        self.type = type  # Atom type : String
        self.elem = elem  # Element symbol : Int
        self.charge = charge    # Charge of atom : Float
        self.occ = occ          # Occupancy of atom : Float
        self.bfact = bfact      # Temperature factor : Float
        # Connected atoms : [Atom]
        self.connect_dict = connect_dict if connect_dict else {}
        # Parent group identifier : {type:[Group]}
        self.__group_list = group_list if group_list else []
        self.rest_str = rest_str    # Rest string : String

    def __repr__(self):
        message = '%s : %s' % (str(self.id), self.name) 
        return message

    def get_group_list(self):
        """Get group identifier list."""
        return self.__groups
    def append_group_list(self, *group_list):
        """Append group identifier list."""
        self.__group_list
        
        for g in groups:
            self.__groups.append(g)

    def get_atom_number(self):
        """Return the atomic number by Integer."""
        ELEM_ATMNUM_DICT.get(self.elem)
        try:
            return ELEM_ATMNUM_DICT[self.elem]
        except KeyError:
            raise 'Atom Element Error'

#-------------------------------------------------------------------------------

class Group(object):

    def __init__(self, parent=None, id=-1, name=None, child_list=[],
                 atom_list=[], code=None, connect_list=None):
        # All of parent groups in this group : [Group]
        self.__parent_list = [parent] if parent else []
        self.id = id            # Group number of sub unit : Int
        # code = ALA, LIP, TIP3P, TIP4P...
        self.__name = name        # Group name : String
        self.code = code        # Code
        # group type : amino acid residue, RNA, DNA, saccharide, lipid etc...
        # side chain, main chain, solvent, solute, water, ions,
        # user-defined, .. : String
        self.type = type
        # All of atoms in this group : [Atom]
        self.__atom_list = atom_list if atom_list else []
        # All of child group in this group_list : [Group]
        self.__child_list = child_list if child_list else []
        # Connected group_list : [Group]
        self.__connect_list = connect_list if connect_list else []

    def __repr__(self, ):
        message = '%s : %s' % (str(self.id), self.name)
        return message

    def append_child_list(self, *group_list):
        """Append child group_list to this object."""
        self.__child_list.extend( group_list )

    def get_child_list(self):
        """Get the child groups by list."""
        return self.__child_list

    def get_parent_list(self):
        """Get the parent group list"""
        return self.__parent_list

    def append_parent_list(self, parent_list):
        """Append the parent group list."""
        self.__parent_list.extend(parent_list)

    @property
    def atoms(self):
        """Get the atoms by list."""
        if not self.__atom_list:
            self.__make_atom_list()
        return self.__atom_list

    def __make_atom_list(self):
        """Make a list of atoms."""
        group_list = self.__child_list
        atom_list = []
        for grp in group_list:
            atom_list.append(grp.atoms)
        self.__atom_list = sorted(set(atom_list), key=operator.attrgetter('id'))

    def get_atom_list_by(self, keyword):
        pass

    @property
    def name(self):
        """Return the name of this group."""
        return self.__name

    def append_atom(self, atom):
        """Append the atom into the group."""
        self.__atom_list.append(atom)

    def __lshift__(self, obj):
        if isinstance(obj, Atom):
            self.__atom_list.append(obj)
        elif isinstance(obj, Group):
            self.__group_list.append(obj)


class Trajectory(object):
    
    # coordinate format
    # [(float, float, float)]

    # frame is [each values]

    def __init__(self, crd_list=None):
        self.__crd_list = crd_list if crd_list else []
        self.__vel_list = []
        self.__ene_list = {}
        self.__box_lsit = []
        self.__other_list = {}

    def check_traj(self, natm):
        """Check whether the number of trajectory is unit one."""
        if self.unit == natm:
            ret = True
        else:
            ret = False

        return ret

    def get_numframe(self):
        """Return the number of frame of trajectory."""
        return len(self.__crd_list)

    def get_numatm(self):
        """Return the number of atoms."""
        return len(self.__crd_list[0])

    def get_crd_list(self, start=1, end=1, step=1):
        """Return the coordinates of the frame from start to end by step."""
        if start <= 0 or end < 0 or step <= 0:
            raise 'Get trajectory error!'
        elif start == end:
            # then return one frame only
            return self.__crd_list[(start-1)]
        elif end == 0:
            # then return all of the frames from start
            return self.__crd_list[(start-1)::step]
        else:
            return self.__crd_list[(start-1):(end-1):step]

    def get_vel_list(self, start=1, end=1, step=1):
        """Return the velocities of the frame from start to end by step."""
        if start <= 1 or end < 0 or step <= 0:
            raise 'Get trajectory error!'
        elif start == end:
            # then return one frame only
            return self.__vel_list[(start-1)]
        elif end == 0:
            # then return all of the frames from start
            return self.__vel_list[(start-1)::step]
        else:
            return self.__vel_list[(start-1):(end-1):step]
        
    def get_ene_list(self, start=1, end=1, step=1, type='Total'):
        """Return the energy of the specified type."""
        enes = self.energies[type]
        if start <= 1 or end < 0 or step <= 0:
            raise 'Get trajectory error!'
        elif start == end:
            # then return one frame only
            return self.__ene_list[(start-1)]
        elif end == 0:
            # then return all of the frames from start
            return self.__ene_list[(start-1)::step]
        else:
            return self.__ene_list[(start-1):(end-1):step]

    def get_box_list(self, start=1, end=1, step=1):
        """Return the box information."""
        if start <= 1 or end < 0 or step <= 0:
            raise 'Get trajectory error!'
        elif start == end:
            # then return one frame only
            return self.__box_list[(start-1)]
        elif end == 0:
            # then return all of the frames from start
            return self.__box_list[(start-1)::step]
        else:
            return self.__box_list[(start-1):(end-1):step]

    def append_frame(self, crd, vel=None, ene=None, box=None, other=None):
        """Append the frame at the last frame of trajectory."""
        self.__crd_list.append(crd)
        if vel:
            self.__vel_list.append(vel)
        if energy:
            self.__ene_list.append(energy)
        if box:
            self.__box_list.append(box)
        if other:
            self.__other_list.append(other)


def main():
    # import molformat
    # filename = 'user-dir/1ag2.pdb'
    # system = molformat.PDB(filename).read()
    
    residue_list = system.get_group_list('Residues')
    for res in residues:
        print res
        print res.atoms

if __name__ == '__main__':
    pass
