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


class AMBER_RESTART_Parser(IParser):
    def __init__(self):
        pass


    def setCrds(self, traj_fn, format='Amber'):
        """Get the trajectory and store into this object."""
        traj_file = open(traj_fn, 'r')
        title = int(traj_file.next())
        natm = int(traj_file.next())
        even = 0; odd  = 1
        if natm%2 == 0:
            cond = even
        else:
            cond = odd

        frame = []
        for line in traj_file:
            x1,y1,z1,x2,y2,z2 = [ float(v) for v in line.split() ]
            frame.extend([(x1,y1,z1),(x2,y2,z2)])
            n += 2
            if cond == even:
                if n == natm: self.frames.append(frame)
            else:
                if n == natm-1:
                    x,y,z = [ float(v) for v in line.split() ]
                    frame.append((x,y,z))
                    self.frames.append(frame)
        
            traj_file.next()


    def readAmberTraj(self, filename):
        """Read the amber restart file and store the coordinates, velocities,
        and box informations.
        """
        file = open(filename, "r")
        nline = len(file.readlines())
        file.close()

        file = open(filename, "r")

        title = file.next().strip()
        cols = file.next().split()
        if len(cols)==1:
            natm = int(cols[0])
            time = 0.0
        elif len(cols)==2:
            natm = int(cols[0])
            time = float(cols[1])
        else:
            sys.exit(1)

        # the condition judgement for the velocity
        has_velocity = True if nline > natm else False

        # for coordinate
        rst_crd = []
        for i, line in enumerate(file):
            x1,y1,z1,x2,y2,z2 = [
                float(line[12*j:12*(j+1)]) for j in range(6)
            ]
            rst_crd.append([x1,y1,z1])
            rst_crd.append([x2,y2,z2])
            if (i+1)*2 == natm:
                break
            elif (i+1)*2 == natm-1:
                line = file.next()
                x,y,z = [ float(line[12*j:12*(j+1)]) for j in range(3) ]
                rst_crd.append([x,y,z])
                break
            else:
                continue

        # for velocity
        rst_vel = []
        if has_velocity:
            for i, line in enumerate(file):
                x1,y1,z1,x2,y2,z2 = [ 
                    float(line[12*j:12*(j+1)]) for j in range(6)
                ]
                rst_vel.append([x1,y1,z1])
                rst_vel.append([x2,y2,z2])
                if (i+1)*2 == natm:
                    break
                elif (i+1)*2 == natm-1:
                    line = file.next()
                    x,y,z = [ float(line[12*j:12*(j+1)]) for j in range(3) ]
                    rst_vel.append([x,y,z])
                    break
                else:
                    continue
        
        # for box
        line = file.next()
        box = [ float(line[12*j:12*(j+1)]) for j in range(6) ]

        file.close()
        retval = dict(title=title, natm=natm, time=time, 
                      crd=rst_crd, vel=rst_vel, box=box)
        return  retval

class AMBER_RESTART_Formatter(IFormatter):
    """docstring for AMBER_RESTART_Formatter"""
    def __init__(self, ndo):
        self.__trajectory = ndo
    def writeAmberTraj(self, filename):
        pass

        

def main():
    pass

if __name__ == '__main__':
    main()

