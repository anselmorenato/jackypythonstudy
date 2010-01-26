#! /opt/python2.6/bin/python
#  -*- encoding: utf-8 -*-
# Copyright (C)  2009 Takakazu Ishikura
import os, sys
from optparse import OptionParser, OptionValueError
import yaml

python_path = '/opt/python2.6/bin/python'

def main():
    # imodel = InterfaceGenerater()
    # imodel.read_config('./gen_config.py')
    # imodel.pp()
    # mock = MockGenerater()
    # mock.read_config('./gen_config.py')
    # mock.pp()

    opts, args = parseOptions()

    if opts.is_interface:
        for arg in args:
            interface = InterfaceGenerater(is_override=opts.is_override)
            interface.read_config(arg)
            interface.write()

    if opts.is_mock:
        for arg in args:
            mock = MockGenerater(is_override=opts.is_override)
            mock.read_config(arg)
            mock.write()

    if opts.is_presenter:
        presenter = PresenterGenerater(is_override=opts.is_override)
        for arg in args:
            presenter.read_config(arg)
        presenter.write()

    if opts.is_presenter_test:
        print 'this version is not implemented.!'
        quit()


def parseOptions():
    """Parse options."""

    usage = ('usage: %prog [options] <input_file>\n'
             'example:\n'
             '    %prog -O -P config_file')
    parser = OptionParser(usage)

    # add options
    parser.add_option(
        "-i", "--generate-interface",
        dest="is_interface",
        default=False,
        action="store_true",
        metavar="INTERFACE",
        help="if this is specified, the interface file will be generated.",
    )
    parser.add_option(
        "-m", "--generate-mockobject",
        dest="is_mock",
        default=False,
        action="store_true",
        metavar="MOCK_OBJECT",
        help="if this is specified, the mock file will be generated.",
    )
    parser.add_option(
        "-O", "--override",
        dest="is_override",
        default=False,
        action="store_true",
        metavar="OVERRIDE",
        help="if this is specified, the output file will be overrided.",
    )
    parser.add_option(
        "-p", "--generate-presenter",
        dest="is_presenter",
        default=False,
        action="store_true",
        metavar="PRESENTER",
        help="if this is specified, the presenter file will be created.",
    )
    parser.add_option(
        "-T", "--generate-presenter-test",
        dest="is_presenter_test",
        default=False,
        action="store_true",
        metavar="PRESENTER_TEST",
        help="if this is specified, the presenter test file will be created.",
    )

    # parse command line arguments and store options and other arguments
    (opts, args) = parser.parse_args()

    # check the arguments
    if len(args) <= 0:
        parser.error("The number of argument is invalid.")

    for arg in args:
        if not os.path.exists(arg):
            parser.error("The specified file not found.")

    return opts, args

# =============================================================================

class InterfaceGenerater(object):

    def __init__(self, is_override=False):
        self.is_override = is_override

    def read_config(self, config_fn):
        with open(config_fn, 'r') as file:
            self.parse_config(file)

    def read_existing(self): pass

    def parse_config(self, file):

        config_content = file.read()
        config = yaml.load(config_content)
        class_name = config['class_name']

        # define interface file name
        if class_name.endswith('View'):
            cn = class_name.replace('View', '')
            obj_name = 'view'
        elif class_name.endswith('Model'):
            cn = class_name.replace('Model', '')
            obj_name = 'model'
        else:
            cn = class_name
            obj_name = ''

        # self._output_filename = '{0}_i{1}.py'.format(cn.lower(), obj_name)
        self._output_filename = 'i{0}_{1}.py'.format(cn.lower(), obj_name)

        # set python property
        self._class_name = 'I'+class_name
        self._events     = config['events']     if config['events']     else []
        self._properties = config['properties'] if config['properties'] else {}
        self._getsets    = config['getsets']    if config['getsets']    else {}
        self._enables    = config['enables']    if config['enables']    else []
        self._methods    = config['methods']    if config['methods']    else []

    def parse_existing(self): pass

    def generate_code(self):
        codes = []
        codes.append( self.inject_header() )
        codes.append( self.inject_class(self._class_name) )

        if self._events != []:
            codes.append(' '*4 + '# events')
            self._events.sort()
            for e in self._events:
                codes.append( self.inject_event(e) )

        if self._properties != {}:
            codes.append(' '*4 + '# properties')
            prop_keys = sorted(self._properties.keys())
            for p in prop_keys:
                codes.append( self.inject_property(p) )

        if self._getsets != {}:
            codes.append(' '*4 + '# properties with setter')
            getsets_keys = sorted(self._getsets.keys())
            for g in getsets_keys:
                if isinstance(self._getsets[g], bool):
                    codes.append( self.inject_bool(g) )
                else:
                    codes.append( self.inject_getset(g) )
        
        if self._enables != []:
            codes.append(' '*4 + '# enables')
            self._enables.sort()
            for en in self._enables:
                codes.append( self.inject_enable(en) )

        if self._methods != []:
            codes.append(' '*4 + '# methods')
            self._methods.sort()
            for en in self._methods:
                codes.append( self.inject_method(en) )

        return codes

    def inject_header(self):
        template = (
            '{indent}#! {path}\n'
            '{indent}#  -*- encoding: utf-8 -*-\n'
            '{indent}# Copyright (C)  2010 Takakazu Ishikura\n'
            '{indent}# Last Change: .\n'
            '\n'
            '# standard modules\n'
            'import os, sys\n'
            '{indent}from abc '
            'import ABCMeta, abstractmethod, abstractproperty\n'
            '\n'
            '# nagara modules\n'
            "nagara_path = os.environ['NAGARA_PATH']\n"
            "sys.path.append( os.path.join(nagara_path, 'src') )\n"
            'from utils.event import NagaraEvent'
            '\n'
            '\n'
        )
        return template.format(indent='', path=python_path)

    def inject_class(self, key):
        template = (
            '{indent}class {key}():\n'
            '{indent}    __metaclass__ =  ABCMeta\n'
        )
        return template.format(key=key, indent='')

    def inject_event(self, key):
        template = (
            '{indent}@abstractproperty\n'
            '{indent}def {key}_event(self): pass\n'
        )
        return template.format(key=key, indent=' '*4)

    def inject_getset(self, key):
        template = (
            '{indent}@abstractmethod\n'
            '{indent}def get_{key}(self): pass\n'
            '{indent}@abstractmethod\n'
            '{indent}def set_{key}(self, {key}): pass\n'
            '{indent}{key} = abstractproperty(get_{key}, set_{key})\n'
        )
        return template.format(key=key, indent=' '*4)

    def inject_bool(self, key):
        template = (
            '{indent}@abstractmethod\n'
            '{indent}def get_{key}(self): pass\n'
            '{indent}@abstractmethod\n'
            '{indent}def set_{key}(self, {key}): pass\n'
            '{indent}is_{key} = abstractproperty(get_{key}, set_{key})\n'
        )
        return template.format(key=key, indent=' '*4)

    def inject_property(self, key):
        template = (
            '{indent}@abstractproperty\n'
            '{indent}def {key}(self): pass\n'
        )
        return template.format(key=key, indent=' '*4)

    def inject_enable(self, key):
        template = (
            '{indent}@abstractmethod\n'
            '{indent}def is_{key}(self): pass\n'
            '{indent}@abstractmethod\n'
            '{indent}def enable_{key}(self, enable=True): pass\n'
        )
        return template.format(key=key, indent=' '*4)

    def inject_method(self, key):
        template = (
            '{indent}@abstractmethod\n'
            '{indent}def {key}(self): pass\n'
        )
        return template.format(key=key, indent=' '*4)

    def write(self):
        if not self.is_override:
            if os.path.exists(self._output_filename):
                print('output file: {0} already exist.'
                      .format(self._output_filename))
                quit()
        with open(self._output_filename, 'w') as file:
            self.pp(file)

    def pp(self, file=sys.stdout):
        for line in self.generate_code():
            file.write(line+'\n')

# ==============================================================================

class MockGenerater(object): 
    def __init__(self, is_override=False):
        self.is_override = is_override

    def read_config(self, config_fn):
        with open(config_fn, 'r') as file:
            self.parse_config(file)

    def parse_config(self, file):
        config_content = file.read()
        config = yaml.load(config_content)
        class_name = config['class_name']

        # define interface file name
        if class_name.endswith('View'):
            cn = class_name.replace('View', '')
            obj_name = 'view'
        elif class_name.endswith('Model'):
            cn = class_name.replace('Model', '')
            obj_name = 'model'
        else:
            cn = class_name
            obj_name = ''

        self._output_filename = '{0}_{1}.py'.format(cn.lower(), obj_name)

        # set python property
        self._class_name = class_name
        self._events     = config['events']     if config['events']     else []
        self._properties = config['properties'] if config['properties'] else {}
        self._getsets    = config['getsets']    if config['getsets']    else {}
        self._enables    = config['enables']    if config['enables']    else []
        self._methods    = config['methods']    if config['methods']    else []

    def generate_code(self):
        codes = []
        codes.append( self.inject_header() )
        codes.append( self.inject_class() )
        
        if self._properties=={} and self._getsets=={} and self._events==[]:
            pass
        else:
            codes.append(' '*8 + '# define properties')
            prop_keys = sorted(self._properties.keys())
            for k in prop_keys:
                codes.append( self.inject_prop_init(k, self._properties[k]) )
            getset_keys = sorted(self._getsets.keys())
            for k in getset_keys:
                codes.append( self.inject_prop_init(k, self._getsets[k]) )
            self._enables.sort()
            for k in self._enables:
                codes.append( self.inject_enable_init(k) )
            codes.append('')

        if self._events != []:
            codes.append(' '*8 + '# generate events')
            self._events.sort()
            for e in self._events:
                codes.append( self.inject_event_init(e) )
            codes.append('')

        if self._properties != {}:
            codes.append(' '*4 + '# properties')
            prop_keys = sorted(self._properties.keys())
            for p in prop_keys:
                codes.append( self.inject_property(p) )

        if self._events != []:
            codes.append(' '*4 + '# events')
            for e in self._events:
                codes.append( self.inject_event(e) )

        if self._getsets != {}:
            codes.append(' '*4 + '# properties with setter')
            getset_keys = sorted(self._getsets.keys())
            for g in getset_keys:
                if isinstance(self._getsets[g], bool):
                    codes.append( self.inject_bool(g) )
                else:
                    codes.append( self.inject_getset(g) )
        
        if self._enables != []:
            codes.append(' '*4 + '# enables')
            for en in self._enables:
                codes.append( self.inject_enable(en) )

#        if self._events != []:
#            codes.append(' '*4 + '# send events')
#            for k in self._events:
#                codes.append( self.inject_send_event(k) )

        if self._methods != []:
            codes.append(' '*4 + '# methods')
            for k in self._methods:
                codes.append( self.inject_method(k) )

        return codes

    def inject_header(self):
        template = (
            '{indent}#! {path}\n'
            '{indent}#  -*- encoding: utf-8 -*-\n'
            '{indent}# Copyright (C)  2010 Takakazu Ishikura\n'
            '{indent}# Last Change: .\n'
            '\n'

            '{indent}# standard modules\n'
            '{indent}import os, sys\n'
            '\n'
            '# nagara modules\n'
            "nagara_path = os.environ['NAGARA_PATH']\n"
            "sys.path.append( os.path.join(nagara_path, 'src') )\n"
            'from utils.event import NagaraEvent'
        )
        return template.format(indent='', path=python_path)

    def inject_class(self):
        # define interface file name
        class_name = self._class_name
        if class_name.endswith('View'):
            cn = class_name.replace('View', '')
            obj_name = 'view'
        elif class_name.endswith('Model'):
            cn = class_name.replace('Model', '')
            obj_name = 'model'
        else:
            cn = class_name
            obj_name = ''
        interface_name = 'i{0}_{1}'.format(cn.lower(), obj_name)
        iclass_name = 'I'+class_name

        template = (
            '\n'
            '{indent}from interfaces.{interface_name} import {iclass_name}\n'
            #'{indent}class {key}({interface_name}.{iclass_name}):\n'
            '{indent}class {key}({iclass_name}):\n'
            '{indent}    def __init__(self):\n'
        )
        return template.format(key=class_name, interface_name=interface_name,
                               iclass_name=iclass_name, indent='')

    def inject_prop_init(self, key, val):
        if isinstance(val, str):
            template = (
                "{indent}self.__{key} = '{val}'"
            )
        else:
            template = (
                '{indent}self.__{key} = {val}'
            )
        return template.format(key=key, val=val, indent=' '*8)

    def inject_enable_init(self, key):
        template = (
            '{indent}self.__is_{key} = True'
        )
        return template.format(key=key, indent=' '*8)
        
    def inject_event_init(self, key):
        template = (
            '{indent}self.__{key}_event = NagaraEvent()'
        )
        return template.format(key=key, indent=' '*8)

    def inject_event(self, key):
        template = (
            '{indent}@property\n'
            '{indent}def {key}_event(self):\n'
            '{indent}    return self.__{key}_event\n'
        )
        return template.format(key=key, indent=' '*4)

    def inject_property(self, key):
        template = (
            '{indent}@property\n'
            '{indent}def {key}(self):\n'
            '{indent}    return self.__{key}\n'
        )
        return template.format(key=key, indent=' '*4)

    def inject_getset(self, key):
        template = (
            '{indent}def get_{key}(self):\n'
            '{indent}    return self.__{key}\n'
            '{indent}def set_{key}(self, {key}):\n'
            '{indent}    self.__{key} = {key}\n'
            '{indent}{key} = property(get_{key}, set_{key})\n'
        )
        return template.format(key=key, indent=' '*4)

    def inject_bool(self, key):
        template = (
            '{indent}def get_{key}(self):\n'
            '{indent}    return self._{key}\n'
            '{indent}def set_{key}(self, {key}):\n'
            '{indent}    self._{key} = {key}\n'
            '{indent}is_{key} = property(get_{key}, set_{key})\n'
        )
        return template.format(key=key, indent=' '*4)

    def inject_enable(self, key):
        template = (
            '{indent}def enable_{key}(self, enable=True):\n'
            '{indent}    self.__{key} = enable\n'
            '{indent}def is_{key}(self):\n'
            '{indent}    return self.__is_{key}\n'
        )
        return template.format(key=key, indent=' '*4)

    def inject_method(self, key):
        template = (
            '{indent}def {key}(self):\n'
            '{indent}    pass\n'
        )
        return template.format(key=key, indent=' '*4)

    def write(self):
        if not self.is_override:
            if os.path.exists(self._output_filename):
                print('output file: {0} already exist.'
                      .format(self._output_filename))
                quit()
        with open(self._output_filename, 'w') as file:
            self.pp(file)

    def pp(self, file=sys.stdout):
        for line in self.generate_code():
            file.write(line+'\n')

# ==============================================================================

class PresenterGenerater(object):
    def __init__(self, is_override):
        self.is_override = is_override
        self._objects = {}

    def set_interface(self): pass
    def get_interface(self): pass

    def generate_code(self):
        codes = []
        codes.append( self.inject_header() )
        codes.append( self.inject_class(self._class_name) )
        codes.append( self.inject_init() )

        # codes.append(' '*8 + '# bind listener')
        # for k, v in self._objects.items():
        #     if k.endswith('Model'):
        #         obj_name = 'model'
        #     elif k.endswith('View'):
        #         obj_name = 'view'
        #     else:
        #         obj_name = 'obj'
        #     for e in v['events']:
        #         codes.append( self.inject_event_bind(e, obj_name) )
        # codes.append('')

        # define listener
        key_list = []
        for k, v in self._objects.items():
            if k.endswith('Model'):
                obj_name = 'model'
            elif k.endswith('View'):
                obj_name = 'view'
            else:
                obj_name = 'obj'
            for e in v['events']:
                codes.append( self.inject_listener(e, obj_name) )

        codes.append( self.inject_log_recieve() )

        # codes.append( self.inject_main(self._objects))

        return codes

    def inject_header(self):
        template = (
            '{indent}#! {path}\n'
            '{indent}#  -*- encoding: utf-8 -*-\n'
            '{indent}# Copyright (C)  2010 Takakazu Ishikura\n'
            '{indent}# Last Change: .\n'
            '\n'
            '# standard modules\n'
            'import os, sys\n'
            '\n'
            '# nagara modules\n'
            "nagara_path = os.environ['NAGARA_PATH']\n"
            "sys.path.append( os.path.join(nagara_path, 'src') )\n"
            'from  utils.event import  EventBindManager\n'
            'from  core.log    import  Log\n'
        )
        return template.format(indent='', path=python_path)

    def read_config(self, config_file):
        with open(config_file, 'r') as file:
            self.parse_config(file)

    def parse_config(self, file):
        config_content = file.read()
        config = yaml.load(config_content)
        class_name = config['class_name']

        properties = dict(
            events = config['events'],
        )
        self._objects[class_name] = properties

        # define interface file name
        cn = []
        for o in self._objects.keys():
            if o.endswith('View'):
                cn.append( o.replace('View', '') )
            elif o.endswith('Model'):
                cn.append( o.replace('Model', '') )
            else:
                cn.append('Undefined')

        if len(set(cn)) == 1:
            class_name = cn[0]
        else:
            class_name = 'Undefined'

        self._class_name = class_name
        self._output_filename = class_name.lower() + '_presenter.py'

    def inject_class(self,key):
        template = (
            '{indent}class {key}Presenter(object):\n'
        )
        return template.format(key=key, indent='')

    def inject_init(self):
        codes = []
        codes.append(' '*4 + '# events')
        template = (
            '{indent}\n'
            '{indent}binder = EventBindManager()'
            '{indent}\n'
            '{indent}def __init__(self, model, view):\n'
            '{indent}    self.model = model\n'
            '{indent}    self.view = view\n'
            '{indent}\n'
            '{indent}    self.binder.bind_all(self)\n'
        )
        return template.format(indent=' '*4)

    # def inject_event_bind(self, key, obj_name):
    #     template = (
    #         '{indent}{obj}.{key}_event.bind(self.{key}_on_{obj})'
    #     )
    #     return template.format(key=key, obj=obj_name, indent=' '*8)

    def inject_listener(self, key, obj_name):
        template = (
            '{indent}@binder("{obj}.{key}_event")\n'
            '{indent}def {key}_on_{obj}(self, msg):\n'
            "{indent}    self.__log_receive('{key}_on_{obj}')\n"
        )
        return template.format(key=key, obj=obj_name, indent=' '*4)

    def inject_log_recieve(self):
        template = (
            '{indent}def __log_receive(self, listener_name):\n'
            "{indent}    info_list = self.binder.get_info(listener_name)\n"
            "{indent}    for info in info_list:\n"
            "{indent}        obj = info['object_name']\n"
            "{indent}        evt = info['event_name']\n"
            "{indent}        cls = info['class_name']\n"
            "{indent}        mes = 'Recieved {{0}} of {{1}}:{{2}} at {{3}}'\n"
            "{indent}        Log( mes.format(evt, obj, cls, listener_name) )\n"
        )
        return template.format(indent=' '*4)

    def write(self):
        if not self.is_override:
            if os.path.exists(self._output_filename):
                print('output file: {0} already exist.'
                      .format(self._output_filename))
                quit()
        with open(self._output_filename, 'w') as file:
            self.pp(file)

    def pp(self, file=sys.stdout):
        for line in self.generate_code():
            file.write(line+'\n')


class PresenterTestGenerator(object):
    def __init__(self): pass

class ModelViewSpecGenerator(object):
    def __init__(self): pass


if __name__ == '__main__':
    main()

