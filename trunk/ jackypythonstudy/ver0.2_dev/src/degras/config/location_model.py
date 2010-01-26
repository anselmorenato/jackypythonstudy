#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura

# standard modules
import os, sys

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from utils.event import NagaraEvent

from interfaces.ilocation_model import ILocationModel
class LocationModel(ILocationModel):
    def __init__(self):

        # define properties
        self.__command_dict = None
        self.__environ_dict = None
        self.__init_file = '/etc/profile.local'
        self.__jms_default = None
        self.__jms_dict = None
        self.__mpi = 'mpijob mpirun'
        self.__name = 'hpcs'
        self.__shell = None
        self.__ssh_address = 'hpcs.med.nagaoya-u.ac.jp'
        self.__ssh_password = 'aaaaaaa'
        self.__ssh_port = 22
        self.__ssh_username = 'ishikura'
        self.__workdir = '/home/ishikura/Nagara/projects'

        # generate events
        self.__init_event = NagaraEvent()
        self.__update_event = NagaraEvent()

    # events
    @property
    def init_event(self):
        return self.__init_event

    @property
    def update_event(self):
        return self.__update_event

    # properties with setter
    def get_command_dict(self):
        return self.__command_dict
    def set_command_dict(self, command_dict):
        self.__command_dict = command_dict
    command_dict = property(get_command_dict, set_command_dict)

    def get_environ_dict(self):
        return self.__environ_dict
    def set_environ_dict(self, environ_dict):
        self.__environ_dict = environ_dict
    environ_dict = property(get_environ_dict, set_environ_dict)

    def get_init_file(self):
        return self.__init_file
    def set_init_file(self, init_file):
        self.__init_file = init_file
    init_file = property(get_init_file, set_init_file)

    def get_jms_default(self):
        return self.__jms_default
    def set_jms_default(self, jms_default):
        self.__jms_default = jms_default
    jms_default = property(get_jms_default, set_jms_default)

    def get_jms_dict(self):
        return self.__jms_dict
    def set_jms_dict(self, jms_dict):
        self.__jms_dict = jms_dict
    jms_dict = property(get_jms_dict, set_jms_dict)

    def get_mpi(self):
        return self.__mpi
    def set_mpi(self, mpi):
        self.__mpi = mpi
    mpi = property(get_mpi, set_mpi)

    def get_name(self):
        return self.__name
    def set_name(self, name):
        self.__name = name
    name = property(get_name, set_name)

    def get_shell(self):
        return self.__shell
    def set_shell(self, shell):
        self.__shell = shell
    shell = property(get_shell, set_shell)

    def get_ssh_address(self):
        return self.__ssh_address
    def set_ssh_address(self, ssh_address):
        self.__ssh_address = ssh_address
    ssh_address = property(get_ssh_address, set_ssh_address)

    def get_ssh_password(self):
        return self.__ssh_password
    def set_ssh_password(self, ssh_password):
        self.__ssh_password = ssh_password
    ssh_password = property(get_ssh_password, set_ssh_password)

    def get_ssh_port(self):
        return self.__ssh_port
    def set_ssh_port(self, ssh_port):
        self.__ssh_port = ssh_port
    ssh_port = property(get_ssh_port, set_ssh_port)

    def get_ssh_username(self):
        return self.__ssh_username
    def set_ssh_username(self, ssh_username):
        self.__ssh_username = ssh_username
    ssh_username = property(get_ssh_username, set_ssh_username)

    def get_workdir(self):
        return self.__workdir
    def set_workdir(self, workdir):
        self.__workdir = workdir
    workdir = property(get_workdir, set_workdir)

    # methods
    def start(self):
        pass

    def set_config(self):
        pass

    def close(self):
        pass

    def append_command(self):
        pass

    def delete_command(self):
        pass

    def append_env_for_command(self):
        pass

    def delete_env_for_command(self):
        pass

    def edit_env_for_command(self):
        pass

    def append_jms(self):
        pass

    def delete_jms(self):
        pass

    def append_env_for_jms(self):
        pass

    def delete_env_for_jms(self):
        pass

    def edit_env_for_jms(self):
        pass

