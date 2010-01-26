#  -*- encoding: utf-8 -*-
# Copyright (C)  2009 Takakazu Ishikura

# available attribute
__all__ =['Config']

# Standard modules
import os, sys
import yaml, pickle
import copy

# Nagara  modules
sys.path.append('..')
from utils.pattern import Singleton
from exception  import NagaraException

# exceptions ===================================================================
class ConfigException(NagaraException): pass
class ConfigFormatException(ConfigException): pass
class ConfigLoadException(ConfigException): pass

# variables ====================================================================
config_filename = 'configs/configs.dump'
init_config_yaml = """
nagara:
    user plugin: ~/Dropbox/Office/myNagara/src/plugin_user
    email: ishikura@gifu-u.ac.jp
    rootdir: ~/workspace/Nagara
    plugin path: hoge

location:
    default: hpcs
    local:
        name: local
        usable: true
        workdir: /absolute/path/to/working/directory
        ssh: 
        jms: 
            Single:
                envs:
                path:
            Thread:
        commands:

    hpcs:
        name: hpcs
        usable: true
        shell: ''
        workdir: /home/ishikura/Nagara/projects
        init_file: /etc/profile.local
        ssh:
            address: '133.66.117.139'
            username: ishikura
            password: '*********' 
            port: 22
            # jms = ['Single', 'MPI', 'LSF'], #Local
        envs:
            HOME: /home/ishikura
            NAGARA_TEST: nagara test

        mpi: mpijob mpirun
        jms:
            default: LSF
            Single:
                name: Single
                enable: false
                envs:
                path:
            MPI:
                name: MPI
                enable: false
                envs:
                path:
            LSF:
                name: LSF
                enable: true
                envs:
                path:
                # script:
        commands:
            amber:
                name: amber
                # envs = dict(AMBERHOME = '/home/hpc/opt/amber10.eth'),
                # path = '/home/hpcs/opt/amber10.eth/exe/sander.MPI',
                envs:
                    AMBERHOME: /home/ishikura/opt/amber10.eth
                path: /home/ishikura/opt/amber10.eth/exe/sander.MPI
                enable: true
            marvin:
                name: marvin
                envs:
                # path = '/home/hpcs/Nagara/app/bin/marvin',
                path:  /home/ishikura/Nagara/app/bin/marvin
                enable: true
            paics:
                name: paics
                # envs = dict(PAICS_HOME='/home/ishi/paics/paics-20081214'),
                # path = '/home/ishi/paics/paics-20081214/main.exe',
                envs:
                    PAICS_HOME: /home/ishi/paics/paics-20081214
                path: /home/ishi/paics/paics-20081214/main.exe
                enable: true
#        vlsn:
#            name: vlsn
#            enable: true
#        rccs:

per task:
    symbolic: True or Fase


"""

# classes ======================================================================
class Config(Singleton):

    """
    The class to treat global configs for each project.
    """

    def __init__(self, project=None):
        self.__save_format = 'pickle' # ini or yaml
        
        if not project:
            class Project(object): pass
            self.__project = Project()
            import random
            self.__project.id = random.randint(1,10)

        # start up configuration
        try: # if nagara is runnning, do nothing
            getattr(self, 'running')
        except AttributeError: # when nagara start up
            self.running = True
            # if config file exists
            if os.path.exists(config_filename):
                self.load()
            else: # nagara's first start up
                self.setup(self.__project)

    def setup(self, project):
        init_config = yaml.load(init_config_yaml)
        # common
        self.__common_config =  init_config
        # projects
        self.__project_config_dict = {}
        self.__current_project = project.id
        self.__project_config_dict[project.id] = init_config
        # cache
        self.__cache_config = {}
        self.__cache_config['common'] = copy.deepcopy(self.__common_config)
        self.__cache_config['project_dict'] = copy.deepcopy(
            self.__project_config_dict)

    def load(self, filename=None):
        if self.__save_format == 'pickle':
            try:
                with open(config_filename, 'r') as f:
                    configs = pickle.load(f)
            except pickle.PickleError:
                raise ConfigLoadException()

        elif self.__save_format == 'ini':
            try:
                pass
            except:
                pass

        elif self.__save_format == 'yaml':
            try:
                with open(filename, 'r') as f:
                    configs = yaml.load(f.read())
            except yaml.YAMLError:
                raise ConfigLoadException()

        # meta
        meta = configs['meta']
        self.__current_project = meta['current']
        # comman
        self.__common_config = configs['common']
        # project
        self.__project_config_dict = configs['projects']
        # cache
        self.__cache_config = configs['cache']

    def dump(self):

        configs = {}
        configs['meta'] = {}
        configs['meta']['current'] = self.__current_project
        # common
        configs['common'] = self.__common_config
        # project
        configs['projects'] = self.__project_config_dict
        # cache
        configs['cache'] = self.__cache_config

        if self.__save_format == 'pickle':
            with open(config_filename, 'w') as f:
                pickle.dump(configs, f)
        elif self.__save_format == 'ini':
            pass
        elif self.__save_format == 'yaml':
            with open(config_filename, 'w') as f:
                yaml.dump(f, configs)
        else:
            raise ConfigFormatException()

    def set_current_project(self, project):
        self.__current = project.id
        self.__config = self.__config_list[self.__current]

    def get_current_project(self):
        return self.__current

    def copy(self, dest_project):
        pass

    def set_format(self, format):
        if format in ['pickle', 'ini', 'yaml']:
            self.__save_format = format

        else:
            raise ConfigFormatException()

    def get_common(self):
        return self.__common_config

    def get_project(self):
        return self.__project_config_dict[self.__current_project]

    def get_user_plugin(self):
        return self.get_common()['nagara']['user plugin']


if __name__ == '__main__':
    class Project(object): pass
    p =  Project()
    p.id = 5
    c = Config()
    c.setup(p)
    print 'c', c.get_common()['location']['local']['workdir']
    c.get_common()['location']['local']['workdir'] = 'hogehoge'

    cc = Config()
    print 'cc', cc.get_common()['location']['local']['workdir']
    print cc.get_project()
    print cc.get_common()['location']['hpcs']['init_file']
    #  cc.dump()

