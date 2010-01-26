# _*_ coding: utf-8 _*_
# Copyright (C)  2009 Takakazu Ishikura

import os, sys
from exception import NagaraException
from command import Command

#-------------------------------------------------------------------------------

class MarvinException(NagaraException): pass

#-------------------------------------------------------------------------------

class Marvin(Command):

    """
    The class to the remote Marvin command.
    """

    # class variables for command line options
    opts_dict = dict(
        ref_temp = '-T',
        step_size = '-s',
        numstep  = '-n',
        print_freq  = '-p',
        restart  = '-i',
        print_info = '-o',
        res_mass = '-m',
        ip_crd_file = 'STDIN',
        op_crd_file = 'STDOUT',
    )

    args = []

    envs_default = {}

    opts_default = dict(
        ref_temp = 0.100,
        step_size = 10,
        numstep  = 10000,
        print_freq  = 10,
        restart  = 0,
        print_info = 0,
        res_mass = 1.00,
        ip_crd_file = 'input.xyz',
        op_crd_file = 'output.xyz',
    )

    # input and output for marvin
    input_objs = dict(
        marvin_system = 1
    )
    input_fns = dict(
        marvin_xyz = 1
    )
    output_objs = dict(
        marvin_system = 1
    )
    output_fns = dict(
        marvin_xyz = 1
    )


    inputs =  ['ip_crd_file']
    input_fmts = dict(
        ip_crd_file = ('obj', 'system_marvin')
    )
    # self.__input_fmts['ip_crd_file'] = ('obj','system_marvin')
    outputs = ['op_crd_file']

    # mpi support
    mpi_support = False

    # input, output and settings for task


    def __init__(self, task, log=None):
        Command.__init__(self, task, log=log)
        self._task = task
        self._log = log
        self.setPath('/home/ishikura/Nagara/app/bin/marvin')
        self.__input_fmts = {}
        # self.initDefault()

    def log(self, message):
        if self._log: self._log.write(message)

    def setSettings(self, settings):
        """Convert from Nagara settings to marvin-specific settings."""
        keys_excludes = ['restart', 'ip_crd_file', 'op_crd_file']
        keys = set(self._opts.keys()) ^ set(keys_excludes)
        opts = {}
        for key in list(keys):
            try:
                opts[key] = settings[key]
            except KeyError:
                raise key+ ' : option for marvin was not found.'
        
        # restart
        try:
            opts['restart'] = 1 if settings['restart'] else 0
        except KeyError:
            raise 'restart : option for marvin was not found.'

        # inputs and outputs, using constant value basically
        opts['ip_crd_file'] = 'input.xyz'
        opts['op_crd_file'] = 'output.xyz'
        
        self._opts = opts
        self._opts['step_size'] = opts['step_size']/1000.0

    def getSettings(self):
        """Convert from the marvin-specific settings to Nagara settings."""
        settings = {}

        # input and outputs

        # restart
        if self._opts['restart']==1:
            settings['restart'] = True
        else:
            settings['restart'] = False

        # others
        keys_excludes = ['restart', 'ip_crd_file', 'op_crd_file']
        keys = set(self._opts.keys()) ^ set(keys_excludes)
        for key in list(keys):
            settings[key] = self._opts[key]

        return settings

    def setSettingsIO(self, ip_crd_file, op_crd_file):
        """Directly set the input and output coordinate file."""
        self.settings['ip_crd_file'] = ip_crd_file
        self.settings['op_crd_file'] = op_crd_file

    def setInputs(self, marvin_xyz):
        """Set the input object(marvin_xyz type)."""
        self._inputs['ip_crd_file'] = 'marvin_xyz'
        self.__input_fmts['ip_crd_file'] = ('obj','system_marvin')

    def setInputByFiles(self, **files):
        # prepare
        local = self._task.local
        local.create()

        # internal amber file names
        input_fns_default = dict(
            ip_crd_file = 'input.xyz'
        )

        # copy the external marvin file to internal marvin file
        for key, dst_fn in input_fns_default.items():
            # print 'bbbbb', self._opts[key], dst_fn
            if files.get(key): local.putFile(files[key], dst_fn)

        self.__input_fmts['ip_crd_file'] = ('file','marvin_xyz')

    def showOutput(self):
        """Show the output data into the outview object."""
        self.log.write(self.__output_file)

    def writeOutput(self, ex_file):
        """Save the output data to the specified file."""
        copy(self.__outputs_file, ex_file)

    def getOutput(self):
        """Return the output by object."""
        return system.System(self.__output_file).Read()

class MarvinSetting(object):

    import setting_helper
    option = setting_helper.ConvertManager()

    def __init__(self, settings):
        self.__settings = settings
        self.option.convert_all(self) 

    def convert(self):
        return self.option.get_converted_options()

    @option
    def step_size(self):
        return self.__settings['dt']

    @option
    def ref_temp(self):
        return self.__settings['ref_temp']

    @option
    def numstep(self):
        l = self.__settings['time_limit']
        dt = self.__settings['dt']
        nstep = l / dt
        return int(nstep)

    @option
    def restart(self):
        ret = 0 if self.__settings['use_restart'] else 1
        return ret

    @option
    def ref_mass(self):
        temp_ctrl = self.__settings['temp_ctrl']
        if temp_ctrl.get('nose'):
            opts= temp_ctrl.get('nose')
            opt = opts[0]
            ret = opt
        else:
            ret = False
        return ret

    @option
    def print_freq(self):
        return self.__settings['print_frequency']

    @option
    def print_info(self):
        options = self.__settings['print_option']
        return 0
