#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura

# standard modules
import os, sys
from abc import ABCMeta, abstractmethod, abstractproperty

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from utils.event import NagaraEvent


class ILocationView():
    __metaclass__ =  ABCMeta

    # events
    @abstractproperty
    def ok_event(self): pass

    @abstractproperty
    def cancel_event(self): pass

    @abstractproperty
    def close_event(self): pass

    @abstractproperty
    def update_event(self): pass

    # properties with setter
    @abstractmethod
    def get_command_dict(self): pass
    @abstractmethod
    def set_command_dict(self, command_dict): pass
    command_dict = abstractproperty(get_command_dict, set_command_dict)

    @abstractmethod
    def get_env_dict(self): pass
    @abstractmethod
    def set_env_dict(self, environ_dict): pass
    env_dict = abstractproperty(get_env_dict, set_env_dict)

    @abstractmethod
    def get_init_file(self): pass
    @abstractmethod
    def set_init_file(self, init_file): pass
    init_file = abstractproperty(get_init_file, set_init_file)

    # @abstractmethod
    # def get_jms_default(self): pass
    # @abstractmethod
    # def set_jms_default(self, jms_default): pass
    # jms_default = abstractproperty(get_jms_default, set_jms_default)

    # @abstractmethod
    # def get_jms_dict(self): pass
    # @abstractmethod
    # def set_jms_dict(self, jms_dict): pass
    # jms_dict = abstractproperty(get_jms_dict, set_jms_dict)

    @abstractmethod
    def get_mpi(self): pass
    @abstractmethod
    def set_mpi(self, mpi): pass
    mpi = abstractproperty(get_mpi, set_mpi)

    @abstractmethod
    def get_name(self): pass
    @abstractmethod
    def set_name(self, name): pass
    name = abstractproperty(get_name, set_name)

    @abstractmethod
    def get_shell(self): pass
    @abstractmethod
    def set_shell(self, shell): pass
    shell = abstractproperty(get_shell, set_shell)

    @abstractmethod
    def get_ssh_address(self): pass
    @abstractmethod
    def set_ssh_address(self, ssh_address): pass
    ssh_address = abstractproperty(get_ssh_address, set_ssh_address)

    @abstractmethod
    def get_ssh_password(self): pass
    @abstractmethod
    def set_ssh_password(self, ssh_password): pass
    ssh_password = abstractproperty(get_ssh_password, set_ssh_password)

    @abstractmethod
    def get_ssh_port(self): pass
    @abstractmethod
    def set_ssh_port(self, ssh_port): pass
    ssh_port = abstractproperty(get_ssh_port, set_ssh_port)

    @abstractmethod
    def get_ssh_username(self): pass
    @abstractmethod
    def set_ssh_username(self, ssh_username): pass
    ssh_username = abstractproperty(get_ssh_username, set_ssh_username)

    @abstractmethod
    def get_workdir(self): pass
    @abstractmethod
    def set_workdir(self, workdir): pass
    workdir = abstractproperty(get_workdir, set_workdir)

    # methods
    @abstractmethod
    def close(self): pass

    @abstractmethod
    def show(self): pass

