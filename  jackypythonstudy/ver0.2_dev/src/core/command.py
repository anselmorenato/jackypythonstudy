# _*_ coding: utf-8 _*_
# Copyright (C)  2009 Takakazu Ishikura

# Standard modules
import os, sys
import datetime
import shutil
from abc import abstractmethod, abstractproperty, ABCMeta

# Nagara modules 
from exception import NagaraException
from log       import Log

### Exception definitions ######################################################
class CommandException(NagaraException): pass
class SettingError(CommandException): pass
class CommandPreparingError(CommandException): pass

#-------------------------------------------------------------------------------

class Command():
    __metaclass__ = ABCMeta

    """
    The abstract class to define a remote or local command.
    Examples:

    # class variables
    options = dict(
        setting_file = '-i',
        log_file = '-o',
        prmtop_file = '-p',
        ip_restart_file = '-c',
        restraint_file = '-ref',
        op_restart_file = '-r',
        crds_file = '-x',
        vels_file = '-v',
        enes_file = '-e',
        # output = 'ARG1',
        # output = 'ARG2',
        # input = 'STDIN',
        # output2 = 'STDOUT',
    )

    # { option : default value }
    default_options = dict(
        setting_file = 'amber.inp',
        log_file = 'amber.log',
        prmtop_file = 'amber.prmtop',
        ip_restart_file = 'old.rst',
        restraint_file = 'rst.rst',
        op_restart_file = 'amber.rst',
        crds_file = 'amber.mdcrd',
        vels_file = 'amber.vel',
        enes_file = 'amber.ene',
    )

    # input and output for amber
    input_formats = dict(
        prmtop_file = 'AMBER_PRMTOP',
        ip_restart_file = 'AMBER_RESTART',
    )
    setting_formats = dict(
        setting_file = 'AMBER_SETTING'
    )
    log_formats = dict(
        log_file = 'AMBER_LOG'
    )
    output_formats = dict(
        op_restart_file = 'AMBER_RESTART',
        crds_file = 'AMBER_CRD_TRAJECTORY',
        vels_file = 'AMBER_VEL_TRAJECTORY',
        enes_file = 'AMBER_ENE_TRAJECTORY',
    )
    type_format_table = dict(
        System = ['AMBER_PRMTOP', 'AMBER_RESTART'],
        Setting = ['AMBER_SETTING']

    )
    environments = dict(
        AMBERHOME = '/home/ishikura/opt/amber10.eth'
    )
    use_mpi = True

    """

    # class variables
    options = {}
    default_options = {}
    environments = {}

    # a list of input and output files for a task.
    # specify from settings keys
    # options <=> inputs, outputs
    # { input_key : data_format }
    input_formats = {}
    setting_formats = {}
    log_formats = {}
    outputs_formats = {}
    type_format_table = {}
    use_mpi = False

    def __init__(self, configs=None):
        """Constructor."""
        self.init_config(configs)

    def set_command_settings(self, configs):
        """Read and """

    def init_config(self, configs):
        """Initialize configs and environments to default."""
        self.__use_mpi = self.use_mpi
        self.__cmdopts = self.cmd_opt_defaults.copy()
        self.__envs = configs['envs']
        self.__path = configs['path']

    def set_options(self, opts):
        """Set options for this command."""
        self._opts.update(opts)

    @property
    def input_formats(self):
        """Return input files for a task."""
        return self.input_formats.values()

    @property
    def output_formats(self):
        """Return output files for a task."""
        return self.output_formats.values()

    @property
    def envs(self):
        return self.__envs

    # this method is @classmethod
    @abstractmethod
    def is_available(self, settings):
        pass

    def __make_input_data(self):
        """Make a input data from the setting dictionary."""
        raise NotImplementationError

    def __correct_file_options(self):
        """Set up the command options from setting dictionary."""
        for key, value in self.__cmdopts.items():
            if key.split('_')[-1] == 'file':
                base_fn = os.path.basename(value)
                self.__cmdopts[key] = '$TASK_PATH/' + base_fn

    def __make_cmdline(self):
        """Make the command line in a run script."""
        # options for the target command
        # ex) marvin_path -f <partopfile> -s <stepsize> -n <maxstep> ...

        self.__correct_file_options()
        opts = []
        arg_dict = {}
        stdios = {}
        # Options
        for key, opt in self.cmd_options.items():
            if opt[0:3] == 'ARG':
                # arguments
                arg_dict[opt] = self.__cmdopts[key]
            elif opt not in ('STDIN', 'STDOUT', 'STDERR'):
                opts.append(str(opt) + ' ' + str(self.__cmdopts[key]))
            else:
                pass

        # Arguments
        args = [ arg_dict[opt] 
                for opt in sorted(arg_dict, key=lambda h: int(h[3:])) ]

        # Standard input
        cmdopts_rev = dict([ (opt, key)
                        for key, opt in self.cmd_options.items() ])
        key_in = cmdopts_rev.get('STDIN')
        if key_in:
            opts.append('<' + ' '+ str(self.__cmdopts[key_in]))
        # Standard output and error
        key_out, key_err = cmdopts_rev.get('STDOUT'), cmdopts_rev.get('STDERR')
        if key_out:
            if key_out == key_err:
                opts.append('>&' + ' ' + str(self.__cmdopts[key_out]))
            elif key_err:
                opts.appned('>' + ' '  + str(self.__cmdopts[key_out]))
                opts.appned('2>' + ' ' + str(self.__cmdopts[key_err]))
            else:
                opts.append('>&' + ' ' + str(self.__cmdopts[key_out]))

        return self.__path + ' ' + ' '.join(args) + ' ' + ' '.join(opts)

    def setup(self):
        # self.__genInputFile(input_fn=input_fn)
        self.__correct_file_options()
        cmdline = self.__make_cmdline()

    def hook_before(self):
        """Preprocess before self.setup."""
        raise NotImplementationError

    def hook_after(self): pass

    @property
    def name(self):
        """Return a command name."""
        name = self.__class__.__name__
        return name.lower()

#-------------------------------------------------------------------------------

# command_dict = dict(
#     Amber = Amber,
#     Marvin = Marvin,
#     Paics = Paics,
# )


def main(): pass

if __name__ == '__main__':
    main()
