#  -*- encoding: utf-8 -*-
# Copyright (C)  2009 Takakazu Ishikura
import os, sys
import yaml

# append the nagara's library path
if __name__ == '__main__':
    sys.path.append('../')
from utils.pattern import Singleton
import warnings  
# warnings.filterwarnings('ignore', category=DeprecationWarning,
#                         message=r'Crypto')
warnings.filterwarnings('ignore', category=DeprecationWarning,
                        message=r'Singleton')


class TaskObject(Singleton):

    def __init__(self, object_config, command_module_name=None):

        # properties
        self.__name         = object_config['name']
        self.__description  = object_config['description']
        self.__help         = object_config['help']
        self.__inputs       = object_config['input']
        self.__outputs      = object_config['output']
        self.__setting      = object_config['setting']
        self.__log          = object_config['log']
        self.__concomitance = object_config['concomitance']
        self.__commands = set()

        # criterias
        self.__type = None
        self.__multi = None
        self.__optional = None

    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__description

    @property
    def help(self):
        return self.__help

    @property
    def inputs(self):
        return self.__get_sockets(self.__inputs)

    @property
    def outputs(self):
        return self.__get_sockets(self.__outputs)

    @property
    def setting(self):
        return self.__setting

    @property
    def log(self):
        return self.__log

    @property
    def concomitance(self):
        return self.__concomitance

    @property
    def commands(self):
        return list(self.__commands)

    def append_commands(self, command_list):
        self.__commands = self.__commands | set(command_list)

    def set_criteria(self, type=None, multi=None, optional=None):
        self.__type = type
        self.__multi = multi
        self.__optional = optional

    def __search_keyword(self, sockets, field=None, value=None):
        if value:
            socket_list = []
            for key, opts in sockets.items():
                if value == opts[field]:
                    socket_list.append(key)
        else:
            socket_list = sockets.keys()
        return set(socket_list)

    def __get_sockets(self, sockets):
        type_list = self.__search_keyword(
            sockets, field='type', value=self.__type)
        multi_list = self.__search_keyword(
            sockets, field='multi', value=self.__multi)
        opt_list = self.__search_keyword(
            sockets, field='optional', value=self.__optional)
        enable_list = list( type_list & multi_list & opt_list )
        self.__type = None
        self.__multi = None
        self.__optional = None
        return dict( [ (key, sockets[key]) for key in enable_list ] )


