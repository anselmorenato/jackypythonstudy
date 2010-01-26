#  -*- encoding: utf-8 -*-
# Copyright (C)  2009 Takakazu Ishikura

# standard modules
import os, sys
from abc import ABCMeta, abstractmethod, abstractproperty

# nagara modules
from exception import NagaraException
if __name__ == '__main__':
    sys.path.append('../utils')
from dataconverter   import DataConverter
from log             import Log

from tasklocal  import TaskLocal
from taskremote import TaskRemote
from job        import Job
from data       import Data

import plugin
from config     import Config
from pattern    import Null
from event      import NagaraEvent


CHECK_TIME=1
SYNC_TIME_LIMIT=1000

################################################################################
# Task
################################################################################
class TaskException(NagaraException): pass
class TaskObjectException(TaskException): pass
class InvalidSocketError(TaskException): pass
class DataAlreadyExistsError(TaskException): pass
class NoDataSocketError(TaskException): pass

# for is_prepared
class CheckPreparedException(TaskException): pass
class NoSocketDataException(CheckPreparedException): pass
class InvalidSettingException(CheckPreparedException): pass
class SocketDataEmptyException(CheckPreparedException): pass

# Task Class ===================================================================
# operations
# prepare
# run
# stop
# delete
class Task(object):

    """
    Class to define tasks that perform each calculation.
    """

    def __init__(self, project, configs=None, name=None,
                 taskobject=None, description=''):

        self.__project = project
        # self.__log = Log
        # configs
        self.__configs = configs

        # task's configs
        # self.__configs = configs['nagara']

        self.__local = None
        self.__remote = None
        self.__job = None

        self.__id = self.__project.get_hightest_id()

        # task name
        if name:
            self.__name = name
        else:
            self.__name = 'task' + ' ' + str(self.__id)

        # description
        self.__description = description

        # generate event
        self.__state_changed_event = NagaraEvent()

        # generate state
        self.__state = TaskState(self)

        # datas (input, output, setting, concomitance)
        self.__inputs       = {}
        self.__outputs      = {}
        self.__concomitance = {}
        self.__calclog      = {}
        self.__setting      = None
        # self.__inputs = {'system': SystemData, 'data':Data}
        # self.__outputs = {naem1: SystemData, name2: Data, name3: Data}

    # property: task_object
    def get_taskobject(self):
        return self.__taskobject

    def set_taskobject(self, taskobject_name):
        user_plugin_path = Config().get_common()['nagara']['user plugin']
        user_plugin_abspath = os.path.expanduser(user_plugin_path)
        taskobject = plugin.load_taskobject_module(user_plugin_abspath)

        for key, cls in taskobject.taskobject_dict.items():
            if key.lower() == taskobject_name.lower():
                self.__taskobject = cls
                break
        else:
            raise TaskObjectException(self)

    # property: default_configs
    def get_default_configs(self):
        return self.__configs
    def set_default_configs(self, configs):
        self.__configs = configs
    default_configs = property(get_default_configs, set_default_configs)

    # property: name
    def get_name(self):
        return self.__name
    def set_name(self, name):
        self.__name = name
    name = property(get_name, set_name)

    # property: path
    def get_path(self):
        return self.__path
    def set_path(self, path):
        self.__path = path
    path = property(get_path, set_path)

    @property
    def id(self):
        return self.__id

    @property
    def inputs(self):
        return self.__inputs

    @property
    def outputs(self):
        return self.__outputs

    def log(self):
        return self.__calclog

    @property
    def concomitance(self):
        return self.__concomitance

    @property
    def setting(self):
        return self.__setting

    def create_outputs(self):
        self.object

    # property: command
    def get_command(self):
        return self.__command or None
    def set_command(self, cmd_str):
        if cmd_str in self.avalable_commands():
            cmd_class = command.command_dict.get(cmd_str)
            if cmc_class:
                self.__command = cmd_class()
            else:
                raise CommandNotFound()
        else:
            raise CommandInvalid()
    command = property(get_command, set_command)
    
    # state
    def get_state(self):
        return self.__state
    def set_state(self, state):
        self.__state = state
    state = property(get_state, set_state)

    # property: description
    def get_desc(self):
        return self.__description
    def set_desc(self, desc):
        self.__description = desc
    description = property(get_desc, set_desc)
    
    @property
    def project(self):
        return self.__project

    @property
    def setting(self):
        return self.__setting

    # ok version method
    def initialize(self):
        self.__local  = TaskLocal(self)
        self.__remote = TaskRemote(self)
        self.__job    = Job(self)

        # templates
        # self.__taskobject.input_types
        # self.__taskobject.output_types
        # self.__taskobject.comcomitances
        # self.__taskobject.setting_type

        # command
        self.__command = None
        # self.__command.input_formats
        # self.__command.output_formats

    @property
    def local(self):
        return self.__local

    @property
    def remote(self):
        return self.__remote

    @property
    def job(self):
        return self.__job

    def setup(self):
        pass

    def prepare_input(self):
        if self.__taskobject:
            self.__taskobject.outputs

    def setup_convert(self):
        pass

    def prepare_setting(self):
        setting_class = settingdata.setting_dict[self.__taskobject.setting]
        datas = self.__setting['datas']
        for option, value in datas.items():
            if value:
                if self.__taskobject.inputs.get(option):
                    self.__taskobject.inputs[option] = value
                if self.__taskobject.outputs.get(option):
                    self.__taskobject.outputs[option] = value

    def change_data_settings(self):
        self.prepare_data_settings()
        self.prepare_output()

    def write(self, message):
        """Write the message."""
        if self.__log: self.__log.write(message)

    def tail_log(self, output):
        log = self.__concomitance['log']
        for line in log.tail():
            output.write(line)

    def get_available_commands(self):
        avalable_commands = []
        for cmd_str in self.__taskobject.commands:
            cmd_class = command.command_dict.get(cmd_str)
            if cmd_class:
                if cmd_class.is_available(settings):
                    avalable_commands.append(cmd_str)
            else:
                raise CommandNotFound()
        return available_commands
    

    def prepare_setting(self):
        if not self.__setting:
            format = self.__taskobject.setting
            self.__setting = SettingData(format)
    
    def check_settings(self, setting_data):
        if setting_data.type == self.__taskobject.setting:
            return True
        else:
            return False

    def convert_input_data(self):
        # {system: Data, restraint
        self.state.preparing
        for socket_name, data in self.inputs.items():
            formats = self.__command.type_format_table.get(data.type)
            if formats:
                dc = DataConverter(data, formats, user_command=False)
                dc.set_filename
                dc.convert()
                datas = dc.get_datas()

        rev_formats = dict([ (format, key) for key, format
                            in self.__command.input_formats.items() ])
        for data in datas:
             key = rev_formats.get(data.format)
             if key:
                 filename = self.__command.default_options[key]
                 file_abspath = os.path.join(self.path, filename)
                 data.dump(file_abspath)
             else:
                 raise DataException()

    def check_input_data(self):
        for key, fmt in self.__command.input_formats.items():
            formats = [ data.type for data in datas ]
            if fmt in formats:
                pass
            else:
                raise DataException()
                
    def convert_setting(self):
        pass

    def check_setting(self):
        pass

    def delete(self):
        self.remote.delete()
        # self.local.delete()
        self.log('delete the task: '+ str(self) + '\n')

    def move(self):
        pass

    def copy(self):
        pass

    def deepcopy(self):
        pass

    def save_file(self):
        pass

    def __setCmd_cmd(self, cmd):
        """Set a command to this task."""
        cmd_configs = self.__configs[self.__host]['commands']
        c = cmd_configs[cmd.getName()]
        cmd.setPath(c['path'])
        cmd.setEnvs(c['envs'])
        self.__cmd = cmd

        self.__task.set_input_data(data, socket)

    # for entry in InitTaskState
    def generate_input_data(self):
        """Generate the input data from taskobject."""
        for socket_name, c in self.__taskobject.inputs.items():
            if c['optional']:
                self.__inputs[socket_name] = {'data': None, 'enable': False}
            else:
                self.__inputs[socket_name] = {'data': None, 'enable': True}

    def generate_output_data(self):
        """Generate the output data from taskobject."""
        for socket_name, c in self.__taskobject.outputs.items():
            data = Data(self.__project, type=c['type'])
            if c['optional']:
                data.enable(False)
                self.__outputs[socket_name] = {'data': data, 'enable': False}
            else:
                data.enable(True)
                self.__outputs[socket_name] = {'data': data, 'enable': True}

    # for request_connect_input and request_connect_output in PreparingTaskState
    def check_input_socketname(self, socket_name):
        """Check whether the socket name for input is valid or invalid."""
        socket = self.__inputs.get(socket_name)
        if not socket: raise InvalidSocketError('input: '+str(socket_name))

    def check_output_socketname(self, socket_name):
        """Check whether the socket name for output is valid or invalid."""
        socket = self.__outputs.get(socket_name)
        if not socket: raise InvalidSocketError('output: '+str(socket_name))

    def set_input_data(self, data, socket_name):
        """Set the data to input socket."""
        self.check_input_socketname(socket_name)
        if self.is_empty_input_socket(socket_name):
            self.__inputs[socket_name]['data'] = data
        else:
            raise DataAlreadyExistsError()

    def unset_input_data(self, socket_name):
        """Unset the data of input socket."""
        self.check_input_socketname(socket_name)
        if self.is_empty_input_socket(socket_name):
            raise NoDataSocketError()
        else:
            self.__inputs[socket_name]['data'] = None

    def is_empty_input_socket(self, socket_name):
        """Return true if the input socket is empty."""
        self.check_input_socketname(socket_name)
        return False if self.__inputs[socket_name]['data'] else True

    # for request_change_socket_setting in PreparingTaskState
    def set_socket_setting(self, inputs={}, outputs={}, concom={}):
        if inputs:
            self.set_input_socket_by(inputs)
        if outputs:
            self.set_output_socket_by(outputs)
        if concom:
            self.set_concom_by(concom)

    def set_input_socket_by(self, socket_name_dict):
        """Set whether the input socket is enable or not."""
        default_enable_socket_list = []
        for socket_name, c in self.__taskobject.inputs.items():
            if not c['optional']:
                default_enable_socket_list.append( socket_name )

        sdesl = set(default_enable_socket_list)
        ssndk = set(socket_name_dict.keys())
        enable_socket_set = ssndk - sdesl

        for socket_name in enable_socket_set:
            self.check_input_socketname(socket_name)

            enable = socket_name_dict[socket_name]
            socket = self.__inputs[socket_name] 
            if enable:
                socket['enable'] = True
                if socket['data']:
                    socket['data'].enable(True)
            else:
                socket['enable'] = False
                if socket['data']:
                    socket['data'].enable(False)

    def set_output_socket_by(self, socket_name_dict):
        """Set whether the output socket is enable or not."""

        default_enable_socket_list = []
        for socket_name, c in self.__taskobject.outputs.items():
            if not c['optional']:
                default_enable_socket_list.append( socket_name )

        sdesl = set(default_enable_socket_list)
        ssndk = set(socket_name_dict.keys())
        enable_socket_set = sdesl ^ ssndk

        for socket_name in enable_socket_set:
            self.check_output_socketname(socket_name)

            enable = socket_name_dict[socket_name]
            socket = self.__outputs[socket_name]
            if enable:
                socket['enable'] = True
                socket['data'].enable(True)
            else:
                socket['enable'] = False
                socket['data'].enable(False)

    def set_concom_by(self, name_dict):
        pass

    def is_prepared(self):
        """Return true if the task is calculatable."""
        try:
            ret = (
                self.is_prepared_for_input_socket() and
                self.is_prepared_for_setting() and
                self.is_prepared_for_hoge()
            )
        except CheckPreparedException as e:
            ret = False
            e.log()
            # raise
        return ret

    def is_prepared_for_input_socket(self):
        for socket_name, c in self.__inputs.items():
            if c['enable']:
                if not c['data']: raise NoSocketDataException(socket_name)
        return True

    def is_prepared_for_setting(self):
        from validator import StandardSettiingValidator as SettingValidator
        sv = SettingValidator(self.__setting)
        if not sv.is_valid():
            raise InvalidSettingException()
        return True

    def is_prepared_for_hoge(self):
        return True

    # for request_any_operations in PreparedTaskState
    def is_ready(self):
        print 'is_ready'
        for socket_name, c in self.__inputs.items():
            print socket_name, c
            if c['enable']:
                if c['data'].is_empty():
                    raise SocketDataEmptyException(socket_name)
                else:
                    pass
        return True





    # for RunnnableTaskState
    def setup_output_data(self):
        chan = self.remote.get_channel()



    # for DoneTaskState
    def set_complete_data(self):
        pass


    # operations in the states
    def any_operations(self):
        self.state.request_any_operations()




    def define_input_sockets(self):
        for socket_name, c in self.__taskobject.inputs.items():
            if not c['optional']:
                self.__inputs[socket_name] = {'data':None, 'enable':True}
            else:
                self.__inputs[socket_name] = {'data':None, 'enable':False}

    def redefine_input_sockets(self, enable_sockets=[]):
        for socket_name in enable_sockets:
            self.__inputs[socket_name]['enable'] = True

    def check_input_sockets(self):
        for name in self.__taskobject.input_types:
            data = self.__inputs.get(name)
            if data:
                if data.is_empty(): 
                    return False
            else:
                return False
        return True

    # event
    @property
    def state_changed_event(self):
        return self.__state_changed_event


    # def copy(self, dst):
    #     return shutil.copytree(src, dst)

#-------------------------------------------------------------------------------


# Task State Class =============================================================
class TaskStateException(TaskException): pass
class TaskState(object):

    def __init__(self, task):
        self.__task = task
        self.__generate_all_states()
        self.change_to_none_object()

    def __generate_all_states(self):
        # standard states
        self.__NONE_OBJECT_STATE = NoneObjectTaskState(self.__task)
        self.__INIT_STATE        = InitTaskState(self.__task)
        self.__PREPARING_STATE   = PreparingTaskState(self.__task)
        self.__PREPARED_STATE    = PreparedTaskState(self.__task)
        self.__READY_STATE       = ReadyTaskState(self.__task)
        self.__WORKING_STATE     = WorkingTaskState(self.__task)
        self.__CONVERTING_STATE  = ConvertingTaskState(self.__task)
        self.__CONVERTED_STATE   = ConvertedTaskState(self.__task)
        self.__SENDING_STATE     = SendingTaskState(self.__task)
        self.__RUNNABLE_STATE    = RunnableTaskState(self.__task)
        self.__PENDING_STATE     = PendingTaskState(self.__task)
        self.__RUNNING_STATE     = RunningTaskState(self.__task)
        self.__STOPPING_STATE    = StoppingTaskState(self.__task)
        self.__ABORTING_STATE    = AbortingTaskState(self.__task)
        self.__DONE_STATE        = DoneTaskState(self.__task)
        self.__RECEIVING_STATE   = ReceivingTaskState(self.__task)
        self.__COMPLETE_STATE    = CompleteTaskState(self.__task)
        
        # error states
        self.__READY_ERROR_STATE   = ReadyErrorTaskState(self.__task)
        self.__WORKING_ERROR_STATE = WorkingErrorTaskState(self.__task)
        self.__RUNNING_ERROR_STATE = RunningErrorTaskState(self.__task)

    @property
    def name(self):
        return self.__state.__class__.__name__

    def get_available_request(self):
        """Return available request in this state."""
        for med in self.__state.__class__.__dict__:
            if med.startswith('request_'): yield med

    def entry(self):
        self.log()
        try:
            self.__state.entry()
        except AttributeError:
            pass

    @property
    def previous(self):
        return self.__previous

    def change_to_none_object(self):
        self.__previous = None
        self.__state = self.__NONE_OBJECT_STATE
        self.entry()

    def change_to_init(self):
        self.__previous = self.__state
        self.__state = self.__INIT_STATE
        self.entry()

    def change_to_preparing(self):
        self.__previous = self.__state
        self.__state = self.__PREPARING_STATE
        self.entry()

    def change_to_prepared(self):
        self.__previous = self.__state
        self.__state = self.__PREPARED_STATE
        self.entry()

    def change_to_ready(self):
        self.__previous = self.__state
        self.__state = self.__READY_STATE
        self.entry()

    def change_to_working(self):
        self.__previous = self.__state
        self.__state = self.__WORKING_STATE
        self.entry()

    def change_to_converting(self):
        self.__previous = self.__state
        self.__state = self.__CONVERTING_STATE
        self.entry()

    def change_to_converted(self):
        self.__previous = self.__state
        self.__state = self.__CONVERTED_STATE
        self.entry()

    def change_to_sending(self):
        self.__previous = self.__state
        self.__state = self.__SENDING_STATE
        self.entry()

    def change_to_runnable(self):
        self.__previous = self.__state
        self.__state = self.__RUNNABLE_STATE
        self.entry()

    def change_to_pending(self):
        self.__previous = self.__state
        self.__state = self.__PENDING_STATE
        self.entry()

    def change_to_running(self):
        self.__previous = self.__state
        self.__state = self.__RUNNING_STATE
        self.entry()

    def change_to_stopping(self):
        self.__previous = self.__state
        self.__state = self.__STOPPING_STATE
        self.entry()

    def change_to_aborting(self):
        self.__previous = self.__state
        self.__state = self.__ABORTING_STATE
        self.entry()

    def change_to_done(self):
        self.__previous = self.__state
        self.__state = self.__DONE_STATE
        self.entry()

    def change_to_receiving(self):
        self.__previous = self.__state
        self.__state = self.__RECEIVING_STATE
        self.entry()

    def change_to_complete(self):
        self.__previous = self.__state
        self.__state = self.__COMPLETE_STATE
        self.entry()
        
    def change_to_ready_error(self):
        self.__previous = self.__state
        self.__state = self.__READY_ERROR_STATE
        self.entry()

    def change_to_working_error(self):
        self.__previous = self.__state
        self.__state = self.__WORKING_ERROR_STATE
        self.entry()

    def change_to_running_error(self):
        self.__previous = self.__state
        self.__state = self.__RUNNING_ERROR_STATE
        self.entry()

    def log(self):
        name = self.__state.__class__.__name__
        message = 'TaskState: ' + 'was set to ' + name
        Log(message)

    def request_rename(self, name):
        self.__task.name = name

    def __getattr__(self, attrname):
        try:
            return getattr(self.__state, attrname)
        except AttributeError:
            return Null()



# Concrete Task State Class ====================================================
class NoneObjectTaskStateException(TaskStateException): pass
class NoneObjectTaskState(object):

    def __init__(self, task):
        self.__task = task

    def request_set_taskobject(self, taskobject_name):
        self.__task.set_taskobject( taskobject_name )
        self.__task.state.change_to_init()


class InitTaskStateException(TaskStateException): pass
class InitTaskState(object):

    def __init__(self, task):
        self.__task = task

    def entry(self):
        self.__task.initialize()
        self.__task.generate_input_data()
        self.__task.generate_output_data()
        self.request_any_operations()

    def request_any_operations(self):
        self.__task.state.change_to_preparing()


class PreparingTaskStateException(TaskStateException): pass
class PreparingTaskState(object):

    def __init__(self, task):
        self.__task = task

    def entry(self):
        self.__task.local.state.change_to_preparing()
        self.__task.job.state.change_to_preparing()
        self.__task.create_output_data()

    def request_change_socket_setting(self, inputs={}, outputs={}, concom={}):
        self.__task.set_socket_setting(
            inputs=inputs, outputs=outputs, concom=concom )
        self.request_any_operations()

    def request_connect_input(self, data, socket):
        self.__task.set_input_data(data, socket)
        self.request_any_operations()

    def request_disconnect_input(self, socket):
        self.__task.unset_input_data(socket)
        self.request_any_operations()

    def request_any_operations(self):
        if self.__task.is_prepared():
            self.__task.state.change_to_prepared()


class PreparedTaskStateException(TaskStateException): pass
class PreparedTaskState(object):

    def __init__(self, task):
        self.__task = task

    def entry(self):
        self.__task.job.state.change_to_prepared()

    def request_change_socket_setting(self, inputs={}, outputs={}, concom={}):
        self.__task.set_socket_setting(
            inputs=inputs, outputs=outputs, concom=concom )
        self.request_any_operations()

    def request_disconnect_input(self, socket):
        self.__task.unset_input_data(socket)
        self.request_any_operations()

    def request_any_operations(self):
        if not self.__task.is_prepared(): 
            self.__task.state.change_to_preparing()
        elif self.__task.is_ready():
            self.__task.state.change_to_ready()
        else:
            pass


class ReadyTaskStateException(TaskStateException): pass
class ReadyTaskState(object):

    def __init__(self, task):
        self.__task = task

    def request_setup(self):
        # from job_state, too
        self.__task.state.change_to_working()
    

class WorkingTaskStateException(TaskStateException): pass
class WorkingTaskState(object):

    def __init__(self, task):
        self.__task = task

    def entry(self):
        self.__task.job.state.change_to_converting()
        self.request_convert()

        while True:
            if self.__task.local.has_all_files(): # and event
                self.__task.local.state.change_to_ready()
                break

        self.__task.remote.state.change_to_init()
        self.__task.job.state.change_to_sending()
        self.__task.remote.state.change_to_receiving()

    def request_convert(self):
        self.__task.convert_data()
        self.__task.convert_setting()
        self.__task.generate_script()

    def request_abort(self):
        self.__task.state.change_to_abort()


class ConvertingTaskState(object):

    def __init__(self, task):
        self.__task = task

    def entry(self):
        self.__task.job.state.change_to_converting()
        self.request_convert()

    def request_convert(self, task):
        self.__task.convert_data()
        self.__task.convert_setting()
        self.__task.generate_script()

    def request_abort(self):
        self.__task.state.change_to_abort()


class ConvertedTaskState(object):

    def __init__(self, task):
        self.__task = task

    def entry(self):
        self.__task.job.state.change_to_converted()
        self.__task.remote.state.change_to_init()

    def request_send(self):
        self.__task.state.change_to_sending()


class SendingTaskState(object):

    def __init__(self, task):
        self.__task = task

    def entry(self):
        self.__task.job.state.change_to_sending()
        self.__task.remote.state.change_to_receiving()


class RunnableTaskStateException(TaskStateException): pass
class RunnableTaskState(object):

    def __init__(self, task):
        self.__task = task

    def entry(self):
        pre = self.__task.state.previous
        if isinstance(pre, SendingTaskState):
            self.__task.setup_output_data()
            self.__task.job.state.change_to_runnable()
        else:
            self.__task.remote.state.change_to_runnable()


class PendingTaskStateException(TaskStateException): pass
class PendingTaskState(object):

    def __init__(self, task):
        self.__task = task

    def request_abort(self):
        self.__task.state.change_to_abort()


class RunningTaskStateException(TaskStateException): pass
class RunningTaskState(object):

    def __init__(self, task):
        self.__task = task

    def entry(self):
        self.__task.remote.state.change_to_running()

    def request_abort(self):
        self.__task.state.change_to_abort()


class StoppingTaskStateException(TaskStateException): pass
class StoppingTaskState(object):

    def __init__(self, task):
        self.__task = task

    def request_run(self):
        pass


class AbortingTaskStateException(TaskStateException): pass
class AbortingTaskState(object):

    def __init__(self, task):
        self.__task = task


class DoneTaskStateException(TaskStateException): pass
class DoneTaskState(object):

    def __init__(self, task):
        self.__task = task

    def entry(self, task):
        self.__task.remote.state.change_to_done()

    def request_fetch(self, data):
        self.__task.remote.state.change_to_sending()
        self.__task.remote.fetch(data)


class ReceivingTaskStateException(TaskStateException): pass
class ReceivingTaskState(object):

    def __init__(self, task):
        self.__task = task


class CompleteTaskStateException(TaskStateException): pass
class CompleteTaskState(object):

    def __init__(self, task):
        self.__task = task

       
class ReadyErrorTaskStateException(TaskStateException): pass
class ReadyErrorTaskState(object):

    def __init__(self, task):
        self.__task = task


class WorkingErrorTaskStateException(TaskStateException): pass
class WorkingErrorTaskState(object):

    def __init__(self, task):
        self.__task = task


class RunningErrorTaskStateException(TaskStateException): pass
class RunningErrorTaskState(object):

    def __init__(self, task):
        self.__task = task


if __name__ == '__main__':

    def print_request_and_check(id, task, message, request_name, *args, **kwds):
        pre = task.state.name
        print
        print '='*80
        print str(id) + ': ' + message
        print '     ' + request_name + ' at ' + task.state.name
        print '     with args and kwds :' , args, kwds
        print task.state.name, list(task.state.get_available_request())
        print ' ***** request log ********** '
        getattr(task.state, request_name)(*args, **kwds)
        print ' ***** input sockets ******** '
        for socket_name, d in task.inputs.items():
            print socket_name, d
        print ' ***** output sockets ******* '
        for socket_name, d in task.outputs.items():
            print socket_name, d
        aft = task.state.name
        print 'STATE TRANSITION: ' + pre + ' => ' + aft


    import project
    p = project.Project()
    t = Task(p)
    p.append_task(t)
    print t.name

    print_request_and_check(
        0, t, '', 'request_rename', 'hoge'
    )
    print t.name

    import data
    system_data = Data(p, type='System')
    group_data  = Data(p, type='group')

    i = 0

    try:

        #
        i+=1
        print_request_and_check(
            i, t, '', 'request_test'
        )
        #
        i+=1
        try:
            print_request_and_check(
                i, t, '', 'request_set_taskobject', 'optimize'
            )
        except data.DataTypeError as e:
            e.log()
        #
        i+=1
        socket_name = 'system'
        print_request_and_check(
            i, t, '', 'request_connect_input', system_data, socket_name
        )
        #
        try:
            i+=1
            print_request_and_check(
                i, t, '',
                'request_change_socket_setting', inputs={'restraint': True}
            )
        except CheckPreparedException as e:
            e.log()
        # 
        print 100, group_data.is_enable()
        try:
            socket_name = 'restraint'
            print_request_and_check(
                i, t, '', 'request_connect_input', group_data, socket_name
            )
        except CheckPreparedException as e:
            e.log()
        print 200, group_data.is_enable()
        #
        try:
            i+=1
            print_request_and_check(
                i, t, 'do disable restraint socket',
                'request_change_socket_setting', inputs={'restraint': False}
            )
        except CheckPreparedException as e:
            e.log()
        #
        try:
            i+=1
            print_request_and_check(
                i, t, 'do disable system socket',
                'request_change_socket_setting', inputs={'system': False}
            )
        except CheckPreparedException as e:
            e.log()
        #
        i+=1
        print_request_and_check(
            i, t, 'disconnect the data from the system socket.',
            'request_disconnect_input', 'system'
        )
        #
        i+=1
        print_request_and_check(
            i, t, '', 'request_rename', 'fuga'
        )
        print t.name
    except CheckPreparedException as e:
        e.log()

    i+=1
    socket_name = 'system'
    print_request_and_check(
        i, t, '', 'request_connect_input', system_data, socket_name
    )

    # to ready state
    i+=1
    socket_name = 'system'
    print_request_and_check(
        i, t, '', 'request_connect_input', system_data, socket_name
    )

    # for id, c in t.outputs.items():
    #     od = c['data']
    #     print id, od.name, od.is_enable()

    # to = t.get_taskobject()
    # print 'name = ', to.name
    # print 'inputs = ', to.inputs
    # print 'outputs = ', to.outputs
    # print 'settings = ', to.setting
    # print '*'*70

    # t.define_input_sockets()
    # print t.inputs


