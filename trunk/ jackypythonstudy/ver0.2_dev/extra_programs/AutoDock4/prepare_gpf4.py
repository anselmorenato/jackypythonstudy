#!/usr/bin/env python2.4
#
# 
#
# $Header: /export/cvs/python/packages/share1.5/AutoDockTools/Utilities24/prepare_gpf4.py,v 1.3 2006/04/13 21:19:59 rhuey Exp $
#

import string
import os.path
import glob
import Numeric
from math import ceil
from MolKit import Read
from AutoDockTools.GridParameters import GridParameters, grid_parameter_list4
from AutoDockTools.GridParameters import GridParameter4FileMaker
from AutoDockTools.atomTypeTools import AutoDock4_AtomTyper


def usage():
    print "Usage: prepare_gpf4.py -l pdbqt_file -r pdbqt_file "
    print "     -l ligand_filename"
    print "     -r receptor_filename"
    print
    print "Optional parameters:"
    print "    [-i reference_gpf_filename]"
    print "    [-o output_gpf_filename]"
    print "    [-p parameter=newvalue]"
    print "    [-d directory of ligands to use to set types]"
    print "    [-v]"
    print
    print "Prepare a grid parameter file (GPF) for AutoDock4."
    print
    print "   The GPF will by default be <receptor>.gpf. This"
    print "may be overridden using the -o flag."

    
if __name__ == '__main__':
    import getopt
    import sys

    try:
        opt_list, args = getopt.getopt(sys.argv[1:], 'vl:r:i:o:p:d:')
    except getopt.GetoptError, msg:
        print 'prepare_gpf4.py: %s' % msg
        usage()
        sys.exit(2)

    receptor_filename = ligand_filename = None
    list_filename = gpf_filename = gpf_filename = None
    output_gpf_filename = None
    directory = None
    parameters = []
    verbose = None
    for o, a in opt_list:
        if o in ('-v', '--v'):
            verbose = 1
        if o in ('-l', '--l'):
            ligand_filename = a
            if verbose: print 'ligand_filename=', ligand_filename
        if o in ('-r', '--r'):
            receptor_filename = a
            if verbose: print 'receptor_filename=', receptor_filename
        if o in ('-i', '--i'):
            gpf_filename = a
            if verbose: print 'reference_gpf_filename=', gpf_filename
        if o in ('-o', '--o'):
            output_gpf_filename = a
            if verbose: print 'output_gpf_filename=', output_gpf_filename
        if o in ('-p', '--p'):
            parameters.append(a)
            if verbose: print 'parameters=', parameters
        if o in ('-d', '--d'):
            directory = a
            if verbose: print 'directory=', directory
        if o in ('-h', '--'):
            usage()
            sys.exit()


    if (not receptor_filename) or (ligand_filename is None and directory is None):
        print "prepare_gpf4.py: ligand and receptor filenames"
        print "                    must be specified."
        usage()
        sys.exit()

    gpfm = GridParameter4FileMaker(verbose=verbose)
    if gpf_filename is not None:
        gpfm.read_reference(gpf_filename)
    if ligand_filename is not None:
        gpfm.set_ligand(ligand_filename)
    gpfm.set_receptor(receptor_filename)
    if directory is not None:
        gpfm.set_types_from_directory(directory)
    for p in parameters:
        key,newvalue = string.split(p, '=')
        kw = {key:newvalue}
        apply(gpfm.set_grid_parameters, (), kw)
    #gpfm.set_grid_parameters(spacing=1.0)
    gpfm.write_gpf(output_gpf_filename)


#prepare_gpf4.py -l 1ebg_lig.pdbqt -r 1ebg_rec.pdbqt -p spacing=0.4 -p npts=[60,60,60] -i ref.gpf -o testing.gpf 

