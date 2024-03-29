#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura
#
# $Date$
# $Rev$
# $Author$
#
# standard modules
import os, sys

nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from utils.event import NagaraEvent, EventBindManager
from core.exception import NagaraException

#-------------------------------------------------------------------------------

class AmberException(NagaraException): pass

#-------------------------------------------------------------------------------

from core.command import Command
class Amber(Command):

    """
    The class to define the remote Amber command
    """
    # class variables
    options = dict(
        setting_file    = '-i'   , 
        log_file        = '-o'   , 
        prmtop_file     = '-p'   , 
        ip_restart_file = '-c'   , 
        restraint_file  = '-ref' , 
        op_restart_file = '-r'   , 
        crds_file       = '-x'   , 
        vels_file       = '-v'   , 
        enes_file       = '-e'   , 
        # output = 'ARG1',
        # output = 'ARG2',
        # input = 'STDIN',
        # output2 = 'STDOUT',
    )

    # { option : default value }
    default_options = dict(
        setting_file    = 'amber.inp'    , 
        log_file        = 'amber.log'    , 
        prmtop_file     = 'amber.prmtop' , 
        ip_restart_file = 'old.rst'      , 
        restraint_file  = 'rst.rst'      , 
        op_restart_file = 'amber.rst'    , 
        crds_file       = 'amber.mdcrd'  , 
        vels_file       = 'amber.vel'    , 
        enes_file       = 'amber.ene'    , 
    )

    # input and output for amber
    input_formats = dict(
        prmtop_file     = 'AMBER_PRMTOP'  , 
        ip_restart_file = 'AMBER_RESTART' , 
    )
    setting_formats = dict(
        setting_file = 'AMBER_SETTING'
    )
    log_formats = dict(
        log_file = 'AMBER_LOG'
    )
    output_formats = dict(
        op_restart_file = 'AMBER_RESTART'        , 
        crds_file       = 'AMBER_CRD_TRAJECTORY' , 
        vels_file       = 'AMBER_VEL_TRAJECTORY' , 
        enes_file       = 'AMBER_ENE_TRAJECTORY' , 
    )
    type_format_table = dict(
        System  = ['AMBER_PRMTOP', 'AMBER_RESTART'],
        Setting = ['AMBER_SETTING']

    )
    environments = dict(
        AMBERHOME = '/home/ishikura/opt/amber10.eth'
    )
    use_mpi = True

    def __init__(self, configs, use_single=False):
        Command.__init__(self, configs)
        if use_single:
            self._path = self._envs['AMBERHOME']+'/exe/sander'
            use_mpi = False
        else:
            self._path = self._envs['AMBERHOME']+'/exe/sander.MPI'

    # def setInputFiles(self, **files):
    #     # prepare
    #     local = self.__task.local
    #     local.create()

    #     # internal amber file names
    #     input_fns_default = dict(
    #         input_file      = 'amber.inp'    , 
    #         prmtop_file     = 'amber.prmtop' , 
    #         ip_restart_file = 'old.rst'      , 
    #     )

    #     # copy the external amber file to internal amber file
    #     for key, dst_fn in input_fns_default.items():
    #         if files.get(key):
    #             local.putFile(files[key], dst_fn)
    #             # test code
    #             rdir = self._task.remote.getPath()
    #             self._opts[key] = rdir + '/' + dst_fn

    # def copyInputFile(self, input_fn=None):
    #     """Generate a input data file on the local host."""
    #     self._task.local.create()
    #     src_path = input_fn
    #     fn = os.path.split(input_fn)[1]
    #     ldir = self.task.getDir()
    #     dst_path = os.path.join(ldir, fn)

    #     src_file = open(src_path, 'rb')
    #     dst_file = open(dst_path, 'wb')
    #     dst_file.write(src_file.read())
    #     src_file.close()
    #     dst_file.close()

    def __judgeCommand(self):
        """Decide a command of amber, which is sander, sander.MPI or pmemd."""
        pass

    def isAvailable(self):
        return True

    def log(self, message):
        if self.__log: self.__log.write(message)




#-------------------------------------------------------------------------------


def main():
    settings = dict(
        method = 'Optimize',
        dt = 0.002,
        time_limit = 10,
        temp_ctrl = {'langevin': [5]},
    )

    configs = dict(
        path = '/home/ishikura/opt/amber10.eth/exe/amber_mock.exe',
        envs = { 'AMBERHOME':'/home/ishikura/opt/amber10.eth' }
    )

    amber = Amber(configs)

    #for key, val in a.convert().items():
    #    print '{0} = {1}'.format(key, val)


if __name__ == '__main__':
    main()


