#  -*- encoding: utf-8 -*-
# from __future__ import absolute_import

# __all__ = [load_taskobject_module, ]

# standard modules
import os, sys
import imp
import yaml

# nagara modules
if __name__ == '__main__':
    sys.path.append('../')
from exception import NagaraException
from taskobject import TaskObject
from iconverter import IParser, IFormatter, IConverterCommand

# plugin: plugin directories
# plugin_module
# module
# attribute: module.attribute_dict

# Exception ####################################################################
class PluginException(NagaraException): pass

# variables ####################################################################
__src_dir = os.path.join(os.path.dirname( os.path.abspath(__file__) ), '..')

# Public functions #############################################################

def load_taskobject_module(user_plugin_abspath):
    t = TaskObjectModuleGenerater(__src_dir, user_plugin_abspath)
    return t.get_module()

def load_command_module(user_plugin_abspath):
    c = ModuleGenerator('command', __src_dir, user_plugin_abspath)
    return c.get_module()

def load_setting_module(user_plugin_abspath):
    c = ModuleGenerator('setting', __src_dir, user_plugin_abspath)
    return c.get_module()
    # return __load_plugin_module('setting', user_plugin_abspath,)

def load_converter_module(user_plugin_abspath):
    c = ConverterModuleGenerater(__src_dir, user_plugin_abspath)
    return c.get_module()
    
    # return __load_plugin_module_converter(user_plugin_abspath,)

def load_log_module(user_plugin_abspath):
    # return __load_plugin_module('log', user_plugin_abspath,)
    c = ModuleGenerator('log', __src_dir, user_plugin_abspath)
    return c.get_module()

def load_output_module(user_plugin_abspath):
    # return __load_plugin_module('output', user_plugin_abspath,)
    c = ModuleGenerator('output', __src_dir, user_plugin_abspath)
    return c.get_module()



# Private functions ###########################################################

__src_dir = os.path.join(os.path.dirname( os.path.abspath(__file__) ), '..')

# Command module

class ModuleGenerator(object):

    """
    Class to create the command module.
    """

    def __init__(self, module_name, src_dir, user_plugin_abspath):
        self.__src_dir = src_dir
        self.__user_plugin_abspath = user_plugin_abspath
        self.__name = module_name

    def __load_module(self, module_name, base_path):
        """Load and Return the module."""
        # print module_name, base_path
        f, n, d = imp.find_module(module_name, [base_path])
        return imp.load_module(module_name, f, n, d)

    def __get_file_list(self, path):
        file_list = []
        for file in os.listdir(path):
            if file == '__init__.py': continue
            if os.path.isdir(file): continue
            file_list.append( file )
        return file_list

    def __create_plugin_module(self):
        """Create module with module name."""
        # create new module and regist plugin dictionary.
        plugin_module = imp.new_module(self.__name)
        plugin_dict = self.__name + '_dict'
        plugin_module.__dict__[plugin_dict] = {}
        return plugin_module

    def __load_module_dict(self, base_path):
        """Load module files and return module list."""
        # make the module file
        module_file_list = self.__get_file_list(base_path)

        # load modules from module_file_list, which must be an absolute path
        module_dict = {}
        for mf in module_file_list:
            try:
                if os.path.isdir(mf): print '555'
                module_name = mf.replace('.py', '')
                module = self.__load_module(module_name, base_path)
                module_dict[module_name] = module
            except ImportError:
                pass
                # raise PluginImportException()
        return module_dict

    def __get_setup_yaml(self, plugin_dir):
        """Read the setup yaml file and load the yaml configuration."""
        yaml_file = os.path.join(plugin_dir, 'setup.yaml')
        # print 'aaaaa'
        # print yaml_file, os.path.exists(yaml_file)
        if os.path.exists(yaml_file):
            with open(yaml_file, 'r') as file:
                yaml_str = file.read()
            plugin_configs = yaml.load(yaml_str)
        else:
            plugin_configs = {}
            
        return plugin_configs

    def __register_plugin(self, module, plugin_abspath):
        """Register all modules of all plugins along config file."""
        plugin_module_abspath = os.path.join(plugin_abspath, module.__name__)
        configs = self.__get_setup_yaml(
            os.path.join(plugin_module_abspath, '..') )
        attr_dict = configs.get(module.__name__)
        if attr_dict: 
            if os.path.isdir(plugin_module_abspath):
                self.__register_attribute(
                    module, plugin_module_abspath, attr_dict)

    def __register_all_plugins(self, module, plugin_abspath):
        """Register all modules of all plugins along config file."""
        for dir in os.listdir(plugin_abspath):
            each_plugin_abspath = os.path.join( plugin_abspath, dir)
            self.__register_plugin(module, each_plugin_abspath)

    def __register_attribute(self, module, plugin_dir, config):
        """Register modules of plugin_dir to plugin module alogn config."""
        plugin_module_dict = self.__load_module_dict(plugin_dir)
        attr_dict = module.__name__ + '_dict'

        for name, attr_name in config.items():
            # print name, attr_name
            # print plugin_module_dict
            for pm in plugin_module_dict.values():
                if hasattr(pm, attr_name):
                    attr = getattr(pm, attr_name)
                    module.__dict__[attr_dict][name] = attr

    def get_module(self):

        # create plugin module
        module = self.__create_plugin_module()

        # core plugin
        core_plugin_abspath = os.path.join(self.__src_dir, 'core_plugin')
        self.__register_plugin(module, core_plugin_abspath)

        # default plugin
        default_plugin_abspath = os.path.join(self.__src_dir, 'plugin')
        self.__register_all_plugins(module, default_plugin_abspath)

        # user plugin
        if os.path.exists(self.__user_plugin_abspath):
            user_plugin_abspath = os.path.abspath(self.__user_plugin_abspath)
            self.__register_all_plugins(module, self.__user_plugin_abspath)
        else:
            pass

        return module


# functions to be used in converter ###########################################

class ConverterModuleGenerater(object):
    """
    Class to create the converter module.
    """

    def __init__(self, src_dir, user_plugin_abspath):
        self.__src_dir = src_dir
        self.__user_plugin_abspath = user_plugin_abspath
        self.__name = 'converter'

    def __load_module(self, module_name, base_path):
        """Load and Return the module."""
        # print module_name, base_path
        f, n, d = imp.find_module(module_name, [base_path])
        return imp.load_module(module_name, f, n, d)

    def __get_file_list(self, path):
        file_list = []
        for file in os.listdir(path):
            if file == '__init__.py': continue
            if os.path.isdir(file): continue
            file_list.append( file )
        return file_list

    def __create_plugin_module(self):
        """Create module with module name."""
        # create new module and regist plugin dictionary.
        plugin_module = imp.new_module(self.__name)
        plugin_module.__dict__['converter_dict'] = {}
        return plugin_module


    def __load_module_dict(self, base_path):
        """Load module files and return module list."""
        # make the module file
        module_file_list = self.__get_file_list(base_path)

        # load modules from module_file_list, which must be an absolute path
        module_dict = {}
        for mf in module_file_list:
            try:
                if os.path.isdir(mf): print '555'
                module_name = mf.replace('.py', '')
                module = self.__load_module(module_name, base_path)
                module_dict[self.__name] = module
            except ImportError:
                pass
                # raise PluginImportException()
        return module_dict

    def __get_setup_yaml(self, plugin_dir):
        """Read the setup yaml file and load the yaml configuration."""
        yaml_file = os.path.join(plugin_dir, 'setup.yaml')
        # print 'aaaaa'
        # print yaml_file, os.path.exists(yaml_file)
        if os.path.exists(yaml_file):
            with open(yaml_file, 'r') as file:
                yaml_str = file.read()
            plugin_configs = yaml.load(yaml_str)
        else:
            plugin_configs = {}
            
        return plugin_configs

    def __register_plugin(self, module, plugin_abspath):
        """Register all modules of all plugins along config file."""
        plugin_module_abspath = os.path.join(plugin_abspath, module.__name__)
        configs = self.__get_setup_yaml(
            os.path.join(plugin_module_abspath, '..') )
        attr_dict = configs.get(module.__name__)
        if attr_dict: 
            if os.path.isdir(plugin_module_abspath):
                self.__register_attribute(
                    module, plugin_module_abspath, attr_dict)

    def __register_all_plugins(self, module, plugin_abspath):
        """Register all modules of all plugins along config file."""
        for dir in os.listdir(plugin_abspath):
            each_plugin_abspath = os.path.join( plugin_abspath, dir)
            self.__register_plugin(module, each_plugin_abspath)

    def __register_attribute(self, module, plugin_dir, config):
        """Register modules of plugin_dir to plugin module alogn config."""
        plugin_module_dict = self.__load_module_dict(plugin_dir)
        conv_dict = module.__dict__['converter_dict']
        

        if 'parser' in config:
            parser_list = config['parser']
            for parser in parser_list:
                pformat  = parser.get('format')
                ptype    = parser.get('type')
                pclsname = parser.get('class')

                # make key
                if isinstance(pformat, list):
                    key = tuple(pformat),  ('NagaraData',)
                else:
                    key = tuple([pformat]), ('NagaraData',)

                for pm in plugin_module_dict.values():
                    if not hasattr(pm, pclsname):
                        continue
                    pclass = getattr(pm, pclsname)
                    # if not issubclass(pclass, IParser):
                    #     continue
                    conv_dict[key] = pclass

        if 'formatter' in config:
            formatter_list = config['formatter']
            for formatter in formatter_list:
                fformat  = formatter.get('format')
                ftype    = formatter.get('type')
                fclsname = formatter.get('class')

                # make key
                if isinstance(fformat, list):
                    key = ('NagaraData',), tuple(fformat)
                else:
                    key = ('NagaraData',), tuple([fformat])

                for pm in plugin_module_dict.values():
                    if not hasattr(pm, fclsname):
                        continue
                    fclass = getattr(pm, fclsname)
                    #if not issubclass(fclass, IFormatter):
                    #    continue
                    conv_dict[key] = fclass

        if 'command' in config:
            command_list = config['command']
            for com1 in command_list:
                c1_format  = com1.get('format')
                c1_type    = com1.get('type')
                c1_clsname = com1.get('class')

                if isinstance(c1_format, list):
                    key1 = tuple(c1_format)
                else:
                    key1 = tuple([c1_format])

                for com2 in command_list:
                    c2_format  = com2.get('format')
                    c2_type    = com2.get('type')
                    c2_clsname = com2.get('class')

                    if not (c1_type == c2_type and c1_clsname == c2_clsname):
                        continue
                    if c1_format == c2_format: continue

                    if isinstance(c2_format, list):
                        key2 = tuple(c2_format)
                    else:
                        key2 = tuple([c2_format])

                    key = key1, key2
                    for pm in plugin_module_dict.values():
                        if not hasattr(pm, c1_clsname):
                            continue
                        com_class = getattr(pm, c1_clsname)
                        # if not issubclass(com_class, IConverterCommand):
                        #     continue
                        conv_dict[key] = com_class

        deny_list = config.get('deny')
        if deny_list:
            for d in deny_list:
                inp_fmt_list, out_fmt_list = d
                
                if isinstance(inp_fmt_list, list):
                    inp_fmt_set = set(inp_fmt_list)
                else:
                    inp_fmt_set = set([inp_fmt_list])

                if isinstance(out_fmt_list, list):
                    out_fmt_set = set(out_fmt_list)
                else:
                    out_fmt_set = set([out_fmt_list])

                for conv_key in conv_dict.keys():
                    inp_key_tup, out_key_tup = conv_key
                    inp_key_set, out_key_set = set(inp_key_tup),set(out_key_tup)

                    if (inp_fmt_set == inp_key_set and
                        out_fmt_set == out_key_set):
                        del conv_dict[conv_key]

        allow_list = config.get('allow')
        if allow_list:
            pass
        else:
            pass
            # raise PluginImportException()


    def get_module(self):

        # create plugin module
        module = self.__create_plugin_module()

        # core plugin
        core_plugin_abspath = os.path.join(self.__src_dir, 'core_plugin')
        self.__register_plugin(module, core_plugin_abspath)

        # default plugin
        default_plugin_abspath = os.path.join(self.__src_dir, 'plugin')
        self.__register_all_plugins(module, default_plugin_abspath)

        # user plugin
        if os.path.exists(self.__user_plugin_abspath):
            user_plugin_abspath = os.path.abspath(self.__user_plugin_abspath)
            self.__register_all_plugins(module, self.__user_plugin_abspath)
        else:
            pass

        # if 'parser' in config:
        #     parser_items = config['parser'].items()
        #     for names, attr_name in parser_items:
        #         name_list = names.split()
        #         name_list.sort()
        #         name_tuple = tuple(name_list)
        #         # print plugin_module_dict
        #         for pm in plugin_module_dict.values():
        #             if hasattr(pm, attr_name):
        #                 attr = getattr(pm, attr_name)
        #                 module.__dict__['parser_dict'][name_tuple] = attr

        # if 'formatter' in config:
        #     formatter_items = config['formatter'].items()
        #     for name, attr_name in formatter_items:
        #         name_list = names.split()
        #         name_list.sort()
        #         name_tuple = tuple(name_list)
        #         # print name, attr_name
        #         # print plugin_module_dict
        #         for pm in plugin_module_dict.values():
        #             if hasattr(pm, attr_name):
        #                 attr = getattr(pm, attr_name)
        #                 module.__dict__['formatter_dict'][name_tuple] = attr


        return module


# functions to be used in task object #########################################

class TaskObjectModuleGenerater(object):

    """
    Class to create the TaskObject module.
    """

    def __init__(self, src_dir, user_plugin_abspath):
        self.__src_dir = src_dir
        self.__user_plugin_abspath = user_plugin_abspath
        self.__name = 'taskobject'

    def get_module(self):

        # create plugin module
        module = self.__create_plugin_module()

        # core plugin
        core_plugin_abspath = os.path.join(self.__src_dir, 'core_plugin')
        self.__register_plugin(module, core_plugin_abspath)

        # default plugin
        default_plugin_abspath = os.path.join(self.__src_dir, 'plugin')
        self.__register_all_plugins(module, default_plugin_abspath)

        # user plugin
        if os.path.exists(self.__user_plugin_abspath):
            user_plugin_abspath = os.path.abspath(user_plugin_path)
            __register_all_plugins_to_taskobject(module, user_plugin_abspath)
        else:
            pass

        # taskobject vs. command 
        self.__register_plugin_t_vs_c(module, core_plugin_abspath)
        self.__register_all_plugins_t_vs_c(module, default_plugin_abspath)
        if os.path.exists(self.__user_plugin_abspath):
            self.__register_all_plugins_t_vs_c(
                module, self.__user_plugin_abspath)
        else:
            pass

        return module

    def __create_plugin_module(self):
        """Create module with module name."""
        # create new module and regist plugin dictionary.
        plugin_module = imp.new_module(self.__name)
        plugin_dict = self.__name + '_dict'
        plugin_module.__dict__[plugin_dict] = {}
        return plugin_module

    def __get_setup_yaml(self, plugin_dir):
        """Read the setup yaml file and load the yaml configuration."""
        yaml_file = os.path.join(plugin_dir, 'setup.yaml')
        # print 'aaaaa'
        # print yaml_file, os.path.exists(yaml_file)
        if os.path.exists(yaml_file):
            with open(yaml_file, 'r') as file:
                yaml_str = file.read()
            plugin_configs = yaml.load(yaml_str)
        else:
            plugin_configs = {}
            
        return plugin_configs

    def __register_plugin(self, module, plugin_abspath):
        # plugin_path/module_name/
        plugin_module_abspath = os.path.join(plugin_abspath, module.__name__)
        configs = self.__get_setup_yaml( 
            os.path.join(plugin_module_abspath, '..') )
        attr_dict = configs.get(module.__name__)
        if attr_dict: 
            if os.path.isdir(plugin_module_abspath):
                self.__register(module, plugin_module_abspath, attr_dict)

    def __register_all_plugins(self, module, plugin_abspath):
        """Register all modules of all plugins along config file."""
        module_name = module.__name__
        # plugin_path/module_name/
        for dir in os.listdir(plugin_abspath):
            each_plugin_abspath = os.path.join(plugin_abspath, dir)
            self.__register_plugin(module, each_plugin_abspath)

    def __register(self, module, plugin_module_path, config):
        """Register the task objects to taskobject module along config."""
        taskobject_dict = self.__create_taskobject_dict(plugin_module_path)
        attr_dict = module.__name__ + '_dict'

        if not hasattr(module, attr_dict):
            raise PluginException()

        for name, attr_name in config.items():
            # print plugin_module_dict
            taskobject = taskobject_dict.get(name)
            if not taskobject: continue
            if not taskobject.name == attr_name: continue
            getattr(module, attr_dict)[name] = taskobject

    def __create_taskobject_dict(self, plugin_module_path):
        yaml_file_list = [
            f for f in os.listdir(plugin_module_path) if f.endswith('.yaml')
        ]
        # make all task object
        taskobject_dict = {}
        for yaml_file in yaml_file_list:
            object_name = yaml_file.replace('.yaml', '')

            # make class
            with open(os.path.join(plugin_module_path, yaml_file), 'r') as f:
                yaml_string = f.read()
            object_config = yaml.load(yaml_string)
            class_name = object_config['name']
            taskobject_class = type( class_name, (TaskObject,), {} )
            # generate dictionary of name and its task object from class
            taskobject_dict[object_name] = taskobject_class(object_config)
        return taskobject_dict

    def __register_plugin_t_vs_c(self, module, plugin_path):
        """Register commands to the taskobject of module."""
        keyword = 'taskobject command'
        configs = self.__get_setup_yaml(plugin_path)
        toc = configs.get(keyword)
        if toc:
            attr_dict = module.__name__ + '_dict'
            obj_dict = getattr(module, attr_dict)
            for obj_str, cmd_str in toc.items():
                taskobject = obj_dict.get(obj_str)
                if taskobject:
                    taskobject.append_commands([cmd_str])

    def __register_all_plugins_t_vs_c(self, module, plugin_path):
        """Register commands for all plugins to the taskobject of module."""
        for dir in os.listdir(plugin_path):
            each_plugin_path = os.path.join( plugin_path, dir)
            if os.path.isdir(plugin_path):
                self.__register_plugin_t_vs_c(module, each_plugin_path)

#==============================================================================
# yet not implemented
def reload(task_object_dict):
    # get path
    pwd_path = os.path.dirname( os.path.abspath(__file__) )
    # generate yaml file list
    yaml_file_list = [
        f for f in os.listdir(pwd_path) if f.endswith('.yaml')
    ]
    # make all task object
    task_object_dict = {}
    for yaml_file in yaml_file_list:
        object_name = yaml_file.replace('.yaml', '')
        # make class
        with open(yaml_file, 'r') as f:
            yaml_string = f.read()
        object_config = yaml.load(yaml_string)
        class_name = object_config['name']
        each_taskobject_class = type( class_name, (TaskObject,), {} )
        # generate dictionary of name and its task object from class
        task_object_dict[object_name] = each_taskobject_class(object_config)
    return task_object_dict


def __check_setup_validity(configs):
    pass

def __check_taskobject_validity(configs):
    pass



# main function ###############################################################
def main():
    # a = command.A()
    user_plugin_path = 'Dropbox/Office/myNagara/src/plugin_user'
    user_plugin_path = os.path.join(os.environ['HOME'], user_plugin_path )
    command = load_command_module(user_plugin_path)
    setting = load_setting_module(user_plugin_path)
    for k, v in command.command_dict.items():
        print k, v
        # p = command.Amber()

    p = command.command_dict['a']()
    p.write('hihifh')
    # print a.write('gyagyagya')
    print setting.setting_dict

def main_command():
    # a = command.A()
    user_plugin_path = 'Dropbox/Office/myNagara/src/plugin_user'
    user_plugin_path = os.path.join(os.environ['HOME'], user_plugin_path )
    command = load_command_module(user_plugin_path)
    print 50*'='
    for k, v in command.command_dict.items():
        print k, v
        # p = command.Amber()

    # p = command.command_dict['a']()
    # p.write('hihifh')
    # print a.write('gyagyagya')

def main_converter():
    # a = command.A()
    user_plugin_path = 'Dropbox/Office/myNagara/src/plugin_user'
    user_plugin_abspath = os.path.join(os.environ['HOME'], user_plugin_path )
    converter = load_converter_module(user_plugin_abspath)
    for key, cls in converter.converter_dict.items():
        print key, cls


def main_task():
    user_plugin_path = 'Dropbox/Office/myNagara/src/plugin_user'
    user_plugin_path = os.path.join(os.environ['HOME'], user_plugin_path )

    taskobject = load_taskobject_module(user_plugin_path)
    for name, to in taskobject.taskobject_dict.items():
        print 50*'='
        print 'string name: ', name
        print 'class name: ', to.name
        print 'inputs: '
        print  to.inputs
        print 'outputs: '
        print to.outputs
        print 'commands: '
        print to.commands
        print 'log: ', to.log
        print 'setting: ', to.setting



if __name__ == '__main__':
    print '*** task ********************************************************'
    main_task()
    print '*** converter ***************************************************'
    main_converter()
    print '*** command *****************************************************'
    main_command()
    main()

