# _*_ coding: utf-8 _*_
# Copyright (C)  2009 Takakazu Ishikura

import os,sys
from exception import NagaraException
from command import Command

#-------------------------------------------------------------------------------

class PaicsException(NagaraException): pass

#-------------------------------------------------------------------------------

class Paics(Command):

    """
    The class to the remote PAICS command.
    """

    # class variables for command line
    opts_dict = dict(
        paics_input_file = 'ARG1',
        paics_log_file   = 'STDOUT',
    )
    opts_default = dict(
        paics_input_file = 'paics.inp',
        paics_log_file = 'paics.log',
    )
    args = {}

    envs_default = dict(
        PAICS_ROOT = '/home/ishi/paics/paics-20081214'
    )

    # input and output for paics
    input_objs = dict(
        xyz = 1,  fragment = 1
    )
    # setting_type = {}
    input_fns = dict(
        paics_input = 1
    )
    output_objs = dict(
        paics_log = 1, decomp_energy = 0
    )
    output_fns = dict(
        paics_log = 1
    )

    mpi_support = True


    def __init__(self, task, log=None):
        Command.__init__(self, task, log=log)
        self._task = task
        self._log = log
        self.__input_fmts = {}

    def log(self, message):
        if self._log: self._log.write(message)

    # def initDefault(self):
    #     """Initialize settings and environments to default."""
    #     self._opts_dict = Paics.opts_dict
    #     self._opts = Paics.opts_default
    #     self._envs = Paics.envs
    #     self._mpi  = Paics.mpi_support
    #     self.envs = Paics.envs_dict
    #     print self.settings
    #     print self.envs

    def __mkInputData(self):
        opts_content = self.__mkInputSection()
        xyz_content = self.__mkXYZSection()
        vec_content = self.__mkVecSection()
        content = '\n'.join([opts_content, xyz_content, vec_content])
        return content

    def setSettings(self, settings):
        pass

    def getSettings(self):
        pass

    def setInputs(self):
        pass

    def __mkInputSection():
        return ''

    def __mkXYZSection():
        return ''

    def __mkVecSection():
        return ''

    def setConfigs(self, configs):
        """Set the configs for paics."""
        self._opts = configs

    def setCrd(self):
        pass

    def getCrd(self):
        pass

    # def aasetup(self):
    #     f = self.task.getInput().isFile()
    #     if f=='paics_input':
    #         use paics_input_fn
    #     else:
    #         make paics_input_fn

    def setInputByFiles(self, **files):
        # prepare
        local = self._task.local
        local.create()

        # internal amber file names
        input_fns_default = dict(
            paics_input_file = 'paics.inp'
        )
        # dst_fn = os.path.basename(self.opts_default['paics_input_file'])
        # copy the external marvin file to internal marvin file
        for key, dst_fn in input_fns_default.items():
            if files.get(key): local.putFile(files[key], dst_fn)

        # rdir = self._task.remote.getPath()
        # self._opts['paics_input_file'] = rdir + '/' + input_fns_default['paics_input_file']
        # ldir = local.getPath()
        # input_path = os.path.join(ldir, input_fns_default['paics_input_file'])
        # log_path = os.path.join(ldir, 'paics.log')
        self._opts['paics_input_file'] = 'paics.inp'
        self._opts['paics_log_file'] = 'paics.log'

        self.__input_fmts['paics_input_file'] = ('file', 'paics_input')

    # def genFragment(self):
    #     type = self.task.getInput().getTypes()
    #     if type=='fragment':
    #         return 'ok'
    #     else:
    #         raise 'ng'


#-------------------------------------------------------------------------------

def main(): pass
# def main():
#     def parseOptions():
# 
#         usage = 'usage: %prog [options]'
#         parser = optparse.OptionParser(usage)
# 
#         parser.add_option(
#             '-c', '--check-all', dest='use_check', metavar='CHECK_FLAG',
#             action='store_false',
#             help='check paics method'
#         )
# 
#         (opts, args) = parser.parse_args()
#         return opts, args
# 
#     opts, args = parseOptions()
#     print args
#     input_fn = args[0]
#     input_contents = open(input_fn, 'r').read()
# 
#     project_name = 'paics-test'
#     project_root = '/home/ishikura/Nagara/projects'
#     project_dir = '/'.join([project_root, project_name])
# 
#     import connection
# 
#     host = '133.66.117.139'
#     password = 'xxxxxxxxx'
# 
#     socket = connection.Connection(host, password=password)
#     # output = socket.execute('ls')
#     # for o in output:
#     #     print o
# 
#     print 1
# 
#     paics = Paics(socket)
#     print 2
#     #paics.setup2(input_contents)
#     paics.setup(PAICS_ROOT, project_dir, input_contents)
#     output = paics.run(lsf=False)
#     for o in output:
#         print(o.rstrip())


if __name__ == '__main__':
    main()

