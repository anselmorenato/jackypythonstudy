#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura
#
# $Date$
# $Rev$
# $Author$
#

# standard modules
import os, sys

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from core.exception import NagaraException

# nagara modules

import plugin
from config      import Config
from utils.event import NagaraEvent
from utils.utils import nproperty, include, Null
from core.model  import *

from log           import Log
from dataconverter import DataConverter
from tasklocal     import TaskLocal
from taskremote    import TaskRemote
from job           import Job
from data          import Data

#=== module variables ==========================================================
CHECK_TIME      = 1
SYNC_TIME_LIMIT = 1000

#=== Interface =================================================================
class ITask(Interface):
    """
    Task model interface
    """

    project_name    = Attribute("project name")
    id              = Attribute("indentify")
    name            = Attribute("task name")
    description     = Attribute("description")
    path            = Attribute("path string")
    taskobject_name = Attribute("Task object name")
    taskobject_help = Attribute("Task object help")
    command_name    = Attribute("Command name")
    setting         = Attribute("setting along object name")
    config          = Attribute("task behaviour configuration")
    config_view     = Attribute("task behaviour configuration for view")
    state_name      = Attribute("task state name")
    # local          = Attribute("hoge")
    # remote         = Attribute("hoge")
	# {'input socket name': {'enable':flag, 'data':Data}
    inputs         = Attribute('input socket dictionary') 
	# {'output socket name': {'enable':flag, 'data':Data}
    outputs        = Attribute('output socket dictionary')

    def getAvailableCommands():
        """Return available command list."""

    def getAvailableRequests():
        """Return available request generator."""

    def save():
        """Save this task properties and state to project file."""

    def load():
        """Load this task properties and state from project file."""

    def copy(name):
        """Create a task from this taks by by the given name."""

    def delete(delete_data=False):
        """Delete this task together with/without the output datas."""

    def tail(data_name):
        """Show the given data of data like 'tail -f' command."""

    def defineTaskObject(taskobject_name):
        """Define task object to use this task by task object name.
        State-changing method.
        """
    def changeSocket(inputs={}, outputs={}, concom={}):
        """Change the socket definitions by arguments. State-chaning method."""

    def linkData(data, socket_name):
        """Link the data to the socket. State-changing method."""

    def unlinkData(socket_name):
        """Unlink the dato from the given socket. State-changing method."""

    def invokeConvert():
		"""Invoke convert the data in this task. State-changing method."""

    def invokeSend():
        """Invoke send the local data in the task. State-chaning method."""

    def invokeSubmit():
        """Invoke submit this task. State-changing method."""

    def invokeStop():
		"""Invoke stop small job of this task. State-changing method.
        """
    def invokeAbort():
		"""Invoke stop small job of this task by force. State-changing method.
        """
    def invokeReceive():
        """Invoke receive the location data in the data. State-changing method.
        """


class TaskException(NagaraException): pass
class NotSetTaskObjectError(TaskException): pass
class Task(object):
    implements(ITask)

    def __init__(self, project):
        self.__model = TaskModel(project)
        self.__state = TaskState(self.__model)
        self.__config_view = None
        verifyObject(ITask, self)

    @nproperty
    def name():
        def get(self):
            return self.__model.name
        def set(self, name):
            self.__model.name = name
        return locals()

    @nproperty
    def description():
    
        def get(self):
            return self.__model.desc
    
        def set(self, description):
            self.__model.desc
    
        return locals()
    

    @property
    def project_name(self):
        return self.__model.project.name

    @property
    def taskobject_name(self):
        if self.__model.taskobject:
            return self.__model.taskobject.name
        else:
            return 'None'

    @property
    def taskobject_help(self):
        if self.__model.taskobject:
            return self.__model.taskobject.help
        else:
            return 'None'

    @property
    def id(self):
        return self.__model.id

    @nproperty
    def description():
        def get(self):
            return self.__model.desc
        def set(self, desc):
            self.__model.desc = desc
        return locals()

    @property
    def path(self):
        return 'path'

    @property
    def state_name(self):
        return self.__state.name

    @property
    def inputs(self):
        return self.__model.inputs

    @property
    def outputs(self):
        return self.__model.outputs

    @nproperty
    def setting():
        def get(self):
            return self.__model.setting
        def set(self, setting):
            self.__model.setting = setting
        return locals()

    @nproperty
    def command_name():
        def get(self):
            return self.__model.command
        def set(self, cmd_str):
            self.__model.command = cmd_str
        return locals()

    @property
    def config(self):
        return self.__model.config

    @property
    def config_view(self):
        return self.__config_view

    # state-independent methods
    # Todo
    def save(self):
        pass

    def load(self):
        pass

    def copy(self, name):
        pass

    def delete(self, delete_data=False):
        pass

    def tail(self, data_name):
        pass

    def getAvailableCommands(self):
        return ['Amber_md', 'paics']

    def getAvailableRequests(self):
        return self.__state.getAvailableRequests()

    # state-changing methods
    def defineTaskObject(self, taskobject_name):
        self.__state.requestSetTaskObject(taskobject_name)

    def changeSocket(self, inputs={}, outputs={}, concom={}):
        self.__state.requestChangeSocket()

    def linkData(self, data, socket_name):
        self.__state.requestLinkInputData

    def unlinkData(self, socket_name):
        self.__state.requestUnlinkInputData(socket_name)

    def invokeConvert(self):
        self.__state.requestConvert()

    def invokeSend(self):
        self.__state.requestSend()

    def invokeSubmit(self):
        self.__state.requestSubmit()

    def invokeStop(self):
        self.__state.requestStop()

    def invokeAbort(self):
        self.__state.requestAbort()

    def invokeReceive(self):
        self.__state.requestReceive()

    # the method used by unit test
    def getEvent(self, event_name):
        return self.__state.getEvent(event_name)

################################################################################
# Task
################################################################################
class TaskObjectException(TaskException): pass
class InvalidSocketError(TaskException): pass
class DataAlreadyExistsError(TaskException): pass
class NoDataSocketError(TaskException): pass

# for is_prepared
class CheckPreparedException(TaskException): pass
class InvalidSettingException(CheckPreparedException): pass
class SocketDataEmptyException(CheckPreparedException): pass

# Task Class ===================================================================

class TaskModel(object):

    """
    Class to define tasks that perform each calculation.
    """

    def __init__(self, project, config=None, taskobject=None, name=None):

        self.__project = project
        # configs
        self.__config = config

        self._taskobject = taskobject

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
            self.__name = 'task ' + str(self.__id)

        # description
        self.__desc = ''

        # generate event
        self.__state_changed_event = NagaraEvent()

        # datas (input, output, setting, concomitance)
        self.__inputs       = {}
        self.__outputs      = {}
        self.__concomitance = {}
        self.__calclog      = {}
        self.__setting      = None
        self.__command      = None
        # self.__inputs = {'system': SystemData, 'data':Data}
        # self.__outputs = {naem1: SystemData, name2: Data, name3: Data}

        # mix-in
        include(self, TaskObjectOperatable ) 
        include(self, SocketOperatable     ) 
        include(self, DataOperatable       ) 
        include(self, SettingOperatable    ) 
        include(self, CommandOperatable    ) 

    @nproperty
    def config():
        def get(self):
            return self.__config
        def set(self, config):
            self.__config = config
        return locals()

    @nproperty
    def name():
        def get(self):
            return self.__name
        def set(self, name):
            self.__name = name
        return locals()

    @nproperty
    def path():
        def get(self):
            return self.__path
        def set(self, path):
            self.__path = path
        return locals()

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

    # property: command
    @nproperty
    def command():

        def get(self):
            return self.__command

        def set(self, cmd_str):
            if cmd_str in self.avalable_commands():
                cmd_class = command.command_dict.get(cmd_str)
                # cmd_class = plugin.loadCommand(cmd_str)
                if cmd_class:
                    self.__command = cmd_class()
                else:
                    raise CommandNotFound()
            else:
                raise CommandInvalid()

        return locals()
    
    @nproperty
    def desc():
        def get(self):
            return self.__desc
        def set(self, desc):
            self.__desc = desc
        return locals()
    
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
        # self._taskobject.input_types
        # self._taskobject.output_types
        # self._taskobject.comcomitances
        # self._taskobject.setting_type

        # command
        # self.__command = None
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
        if self._taskobject:
            self._taskobject.outputs

    def setup_convert(self):
        pass

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

    def getAvailableCommands(self):
        """Get available command list for setting."""
        avalable_commands = []
        for cmd_str in self._taskobject.commands:
            cmd_class = command.command_dict.get(cmd_str)
            if cmd_class:
                if cmd_class.isAvailable(settings):
                    avalable_commands.append(cmd_str)
            else:
                raise CommandNotFound()
        return available_commands

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


    def isPrepared(self):
        """Return true if the task is calculatable."""
        try:
            ret = (
                self.isPreparedAllInputSocket() and
                self.isPreparedSetting()
            )
        except CheckPreparedException as e:
            ret = False
            e.log()
            # raise
        return ret

    # for request_any_operations in PreparedTaskState
    def isReady(self):
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

    # event
    @property
    def state_changed_event(self):
        return self.__state_changed_event

    # def copy(self, dst):
    #     return shutil.copytree(src, dst)

#-------------------------------------------------------------------------------


# Task State Class =============================================================
from utils.event import NagaraEvent
class TaskStateException(TaskException): pass
class NotFoundEventError(TaskStateException): pass
class NotFoundStateError(TaskStateException): pass
class TaskState(object):

    def __init__(self, task):
        self.__generateAllStates(task)
        self.__state = None 
        self.changeState('none_object')

    def __generateAllStates(self, task):
        # standard states
        self.__state_dict = dict(
            none_object   = NoneObjectTaskState(   self , task )  ,
            init          = InitTaskState(         self , task )  ,
            preparing     = PreparingTaskState(    self , task )  ,
            prepared      = PreparedTaskState(     self , task )  ,
            ready         = ReadyTaskState(        self , task )  ,
            working       = WorkingTaskState(      self , task )  ,
            converting    = ConvertingTaskState(   self , task )  ,
            converted     = ConvertedTaskState(    self , task )  ,
            sending       = SendingTaskState(      self , task )  ,
            runnable      = RunnableTaskState(     self , task )  ,
            pending       = PendingTaskState(      self , task )  ,
            running       = RunningTaskState(      self , task )  ,
            stopping      = StoppingTaskState(     self , task )  ,
            aborting      = AbortingTaskState(     self , task )  ,
            done          = DoneTaskState(         self , task )  ,
            receiving     = ReceivingTaskState(    self , task )  ,
            complete      = CompleteTaskState(     self , task )  ,
            ready_error   = ReadyErrorTaskState(   self , task )  ,
            working_error = WorkingErrorTaskState( self , task )  ,
            running_error = RunningErrorTaskState( self , task )  ,
        )

        self.__event_dict = dict(
            none_object   = NagaraEvent() , 
            init          = NagaraEvent() , 
            preparing     = NagaraEvent() , 
            prepared      = NagaraEvent() , 
            ready         = NagaraEvent() , 
            working       = NagaraEvent() , 
            converting    = NagaraEvent() , 
            converted     = NagaraEvent() , 
            sending       = NagaraEvent() , 
            runnable      = NagaraEvent() , 
            pending       = NagaraEvent() , 
            running       = NagaraEvent() , 
            stopping      = NagaraEvent() , 
            aborting      = NagaraEvent() , 
            done          = NagaraEvent() , 
            receiving     = NagaraEvent() , 
            complete      = NagaraEvent() , 
            ready_error   = NagaraEvent() , 
            working_error = NagaraEvent() , 
            running_error = NagaraEvent() , 
        )

    @property
    def name(self):
        return self.__state.__class__.__name__.replace('TaskState', '')

    @property
    def previous(self):
        return self.__previous

    def getAvailableRequests(self):
        """Return available request generator in this state."""
        for med in self.__state.__class__.__dict__:
            if med.startswith('request'): yield med

    def entry(self):
        self.log()
        try:
            self.__state.entry()
        except AttributeError:
            pass

    def getEvent(self, event_name):
        ename = event_name.lower()
        if ename not in self.__event_dict:
            raise NotFoundEventError(event_name)
        return self.__event_dict[ename]

    def changeState(self, state_name):
        sname = state_name.lower()
        if sname not in self.__state_dict:
            raise NotFoundStateError(state_name)
        self.__previous = self.__state
        self.__state = self.__state_dict[sname]
        self.entry()

    def log(self):
        name = self.__state.__class__.__name__
        message = 'TaskState: ' + 'was set to ' + name
        Log(message)

    def __getattr__(self, attrname):
        if attrname.endswith('_event'):
            attrname = attrname.replace('_event', '')
            return self.getEvent(attrname)
        elif attrname.startswith('request'):
            try:
                return getattr(self.__state, attrname)
            except:
                return Null()

        else:
            raise AttributeError(attrname)


# Concrete Task State Class ====================================================
class NoneObjectTaskStateException(TaskStateException): pass
class NoneObjectTaskState(object):

    def __init__(self, state, task):
        self.__task   = task
        self.__state = state

    def requestSetTaskObject(self, taskobject_name):
        self.__task.defineTaskObjectByName( taskobject_name )
        self.__state.changeState('init')


class InitTaskStateException(TaskStateException): pass
class InitTaskState(object):

    def __init__(self, state, task):
        self.__task  = task
        self.__state = state

    def entry(self):
        self.__task.initialize()
        self.__task.createInputSockets()
        self.__task.createOutputSockets()
        self.__state.none_object_event.fire()
        self.requestAnyOperations()

    def requestAnyOperations(self):
        self.__state.changeState('preparing')


class PreparingTaskStateException(TaskStateException): pass
class PreparingTaskState(object):

    def __init__(self, state, task):
        self.__task  = task
        self.__state = state

    def entry(self):
        self.__state.preparing_event.fire()
        # self.__task.createOutputData()

    def requestChangeSocket(self, inputs={}, outputs={}, concom={}):
        self.__task.changeSocket(
            inputs=inputs, outputs=outputs, concom=concom )
        self.requestAnyOperations()

    def requestConnectInput(self, data, socket):
        self.__task.linkInputData(data, socket)
        self.requestAnyOperations()

    def requestDisconnectInput(self, socket):
        self.__task.uninkInputData(socket)
        self.requestAnyOperations()

    def requestAnyOperations(self):
        if self.__task.is_prepared():
            self.__state.changeState('prepared')


class PreparedTaskStateException(TaskStateException): pass
class PreparedTaskState(object):

    def __init__(self, state, task):
        self.__task  = task
        self.__state = state

    def entry(self):
        self.__state.prepared_event.fire()

    def requestChangeSocket(self, inputs={}, outputs={}, concom={}):
        self.__task.changeSocket(
            inputs=inputs, outputs=outputs, concom=concom )
        self.requestAnyOperations()

    def requestDisconnectInput(self, socket):
        self.__task.unlinInputData(socket)
        self.requestAnyOperations()

    def requestAnyOperations(self):
        if not self.__task.is_prepared(): 
            self.__state.changeState('preparing')
        elif self.__task.is_ready():
            self.__state.changeState('ready')
        else:
            pass


class ReadyTaskStateException(TaskStateException): pass
class ReadyTaskState(object):

    def __init__(self, state, task):
        self.__task  = task
        self.__state = state

    def requestSetup(self):
        # from job_state, too
        self.__state.changeState('working')
    

class WorkingTaskStateException(TaskStateException): pass
class WorkingTaskState(object):

    def __init__(self, state, task):
        self.__task  = task
        self.__state = state

    def entry(self):
        self.__task.job.state.change_to_converting()
        self.requestConvert()

        while True:
            if self.__task.local.has_all_files(): # and event
                self.__task.local.state.change_to_ready()
                break

        self.__task.remote.state.change_to_init()
        self.__task.job.state.change_to_sending()
        self.__task.remote.state.change_to_receiving()

    def requestConvert(self):
        self.__task.convert_data()
        self.__task.convert_setting()
        self.__task.generate_script()

    def requestAbort(self):
        self.__state.change('aborting')


class ConvertingTaskState(object):

    def __init__(self, state, task):
        self.__task  = task
        self.__state = state

    def entry(self):
        self.__state.converting_event.fire()
        self.requestConvert()

    def requestConvert(self, task):
        self.__task.convert_data()
        self.__task.convert_setting()
        self.__task.generate_script()

    def requestAbort(self):
        self.__state.changeState('aborting')


class ConvertedTaskState(object):

    def __init__(self, state, task):
        self.__task  = task
        self.__state = state

    def entry(self):
        self.__state.converted_event.fire()

    def requestSend(self):
        self.__state.changeState('sending')


class SendingTaskState(object):

    def __init__(self, state, task):
        self.__task  = task
        self.__state = state

    def entry(self):
        self.__state.sending_event.fire()

class RunnableTaskStateException(TaskStateException): pass
class RunnableTaskState(object):

    def __init__(self, state, task):
        self.__task  = task
        self.__state = state

    def entry(self):
        pre = self.__state.previous
        if pre.name == 'Sending':
            self.__task.createOutputData()
        self.__state.runnable_event.fire()


class PendingTaskStateException(TaskStateException): pass
class PendingTaskState(object):

    def __init__(self, state, task):
        self.__task  = task
        self.__state = state

    def requestAbort(self):
        self.__state.changeState('aborting')


class RunningTaskStateException(TaskStateException): pass
class RunningTaskState(object):

    def __init__(self, state, task):
        self.__task  = task
        self.__state = state

    def entry(self):
        self.__state.running_event.fire()

    def requestAbort(self):
        self.__state.changeState('aborting')


class StoppingTaskStateException(TaskStateException): pass
class StoppingTaskState(object):

    def __init__(self, state, task):
        self.__task  = task
        self.__state = state

    def requestRun(self):
        pass


class AbortingTaskStateException(TaskStateException): pass
class AbortingTaskState(object):

    def __init__(self, state, task):
        self.__task  = task
        self.__state = state


class DoneTaskStateException(TaskStateException): pass
class DoneTaskState(object):

    def __init__(self, state, task):
        self.__task  = task
        self.__state = state

    def entry(self, task):
        self.__state.done_event.fire()

    def requestFetch(self, data):
        self.__task.remote.state.change_to_sending()
        self.__task.remote.fetch(data)


class ReceivingTaskStateException(TaskStateException): pass
class ReceivingTaskState(object):

    def __init__(self, state, task):
        self.__task  = task
        self.__state = state


class CompleteTaskStateException(TaskStateException): pass
class CompleteTaskState(object):

    def __init__(self, state, task):
        self.__task  = task
        self.__state = state

       
class ReadyErrorTaskStateException(TaskStateException): pass
class ReadyErrorTaskState(object):

    def __init__(self, state, task):
        self.__task  = task
        self.__state = state


class WorkingErrorTaskStateException(TaskStateException): pass
class WorkingErrorTaskState(object):

    def __init__(self, state, task):
        self.__task  = task
        self.__state = state


class RunningErrorTaskStateException(TaskStateException): pass
class RunningErrorTaskState(object):

    def __init__(self, state, task):
        self.__task  = task
        self.__state = state

#=== StateChanger ==============================================================
from utils.event import EventBindManager
class TaskStateCommunicator:

    binder = EventBindManager()

    def __init__(self, task_state, local, remote, job):
        self.task_state = task_state
        self.local      = local
        self.remote     = remote
        self.job        = job

        self.binder.bindAll(self)

    @binder('task_state.none_object_event')
    def receiveNoneObject(self, msg):
        pass

    @binder('task_state.init_event')
    def receiveInit(self, msg):
        pass

    @binder('task_state.preparing_event')
    def receivePreparing(self, msg):
        self.local.changeState('preparing')
        self.job.changeState('preparing')

    @binder('task_state.prepared_event')
    def receivePrepared(self, msg):
        self.job.changeState('prepred')

    @binder('task_state.ready_event')
    def receiveReady(self, msg):
        pass

    # @binder('task_state.working_event')
    # def receiveWorking(self, msg):
    #     pass
        self.job.changeState('converting')


        self.__task.job.state.change_to_converting()
        self.requestConvert()

        while True:
            if self.__task.local.has_all_files(): # and event
                self.__task.local.state.change_to_ready()
                break

        self.__task.remote.state.change_to_init()
        self.__task.job.state.change_to_sending()
        self.__task.remote.state.change_to_receiving()


    @binder('task_state.converting_event')
    def receiveConverting(self, msg):
        self.job.changeState('converting')

    @binder('task_state.converted_event')
    def receiveConverted(self, msg):
        self.job.changeState('converted')
        self.remote.changeState('init')

    @binder('task_state.sending_event')
    def receiveSending(self, msg):
        self.job.changeState('sending')
        self.remote.changeState('receiving')

    @binder('task_state.runnable_event')
    def receiveRunnable(self, msg):
        pre = self.task_state.previous
        if pre.name == 'Sending':
            self.job.changeState('runnable')
        else:
            self.remote.changeState('runnable')

    @binder('task_state.running_event')
    def receiveRunning(self, msg):
        self.remote.changeState('running')

    @binder('task_state.stopping_event')
    def receiveStopping(self, msg):
        pass

    @binder('task_state.pending_event')
    def receivePending(self, msg):
        pass

    @binder('task_state.done_event')
    def receiveDone(self, msg):
        self.rmeote.changeState('done')

    @binder('task_state.receiving_event')
    def receiveReceive(self, msg):
        pass

    @binder('task_state.complete_event')
    def receiveComplete(self, msg):
        pass

    @binder('task_state.aborting_event')
    def receiveAborting(self, msg):
        pass




class LocalStateCommunicator:

    binder = EventBindManager()

    def __init__(self, local, task_state):
        self.local = local
        self.task_state = task_state


class RemoteStateCommunicator:

    binder = EventBindManager()

    def __init__(self, remote, task_state):
        self.remote = remote
        self.task_state = task_state


class JobStateCommunicator:

    binder = EventBindManager()

    def __init__(self, job, task_state):
        self.job = job
        self.task_state = task_state




#=== Mix-ins ===================================================================
class TaskObjectOperatable:

    @property
    def taskobject(self):
        return self._taskobject
    
    def defineTaskObjectByName(self, taskobject_name):
        user_plugin_path = Config().get_common()['nagara']['user plugin']
        user_plugin_abspath = os.path.expanduser(user_plugin_path)
        taskobject = plugin.load_taskobject_module(user_plugin_abspath)

        for key, cls in taskobject.taskobject_dict.items():
            if key.lower() == taskobject_name.lower():
                self.__taskobject = cls
                break
        else:
            raise TaskObjectException(self)


#===============================================================================
class SocketOperatable:

    def createInputSockets(self):
        """Create input sockets by abstract input attribute of task object."""
        for socket_name, c in self.__taskobject.inputs.items():
            if not c['optional']:
                self.__inputs[socket_name] = {'data':None, 'enable':True}
            else:
                self.__inputs[socket_name] = {'data':None, 'enable':False}

    def createOuptputSockets(self):
        """Create output sockets by abstract outputs attribute of task object.
        """
        for socket_name, c in self.__taskobject.outputs.items():
            if not c['optional']:
                self.__outputs[socket_name] = {'data':None, 'enable':True}
            else:
                self.__outputs[socket_name] = {'data':None, 'enable':False}

    def enableInputSockets(self, **socket_dicts):
        for socket_name, enable in socket_enables.items():
            if socket_name in self.__inputs:
                self.__inputs[socket_name]['enable'] = enable

    def enableOutputSockets(self, **socket_dicts):
        for socket_name, enable in socket_enables.items():
            if socket_name in self.__inputs:
                self.__outputs[socket_name]['enable'] = enable

    def checkInputSocketByName(self, socket_name):
        """Check whether the socket name for input is valid or invalid."""
        if socket_name not in self.__inputs:
            raise InvalidSocketError('input: '+str(socket_name))

    def checkOutputSocketByName(self, socket_name):
        """Check whether the socket name for output is valid or invalid."""
        if socket_name not in self.__outputs:
            raise InvalidSocketError('output: '+str(socket_name))

    def linkInputData(self, data, socket_name):
        """Link the data to the input socket."""
        self.checkInputSocketByName(socket_name)
        if self.isEmptyInputSocket(socket_name):
            self.__inputs[socket_name]['data'] = data
        else:
            raise DataAlreadyExistsError()

    def unlinkInputData(self, socket_name):
        """Remove the data in the input socket."""
        self.checkInputSocketByName(socket_name)
        if self.isEmptyInputSocket(socket_name):
            raise NoDataSocketError(socket_name)
        else:
            self.__inputs[socket_name]['data'] = None

    def isEmptyInputSocket(self, socket_name):
        """Return true if the input socket is empty."""
        self.checkInputSocketByName(socket_name)
        return False if self.__inputs[socket_name]['data'] else True

    def isPreparedAllInputSocket(self):
        """Return true if all of the input socket are not empty."""
        for socket_name in self.__inputs:
            if self.isEmptyInputSocket(socket_name):
                return False
        return True

    def changeSocket(self, inputs={}, outputs={}, concoms={}):
        """Change the definition of socket."""
        if inputs:
            self.__changeInputSocket(inputs)
        if outputs:
            self.__changeOutputSocket(outputs)
        if concom:
            self.__changeConcom(concoms)

    def __changeInputSocket(self, socket_name_dict):
        """Set whether the input socket is enable or not."""
        default_enable_socket_list = []
        for socket_name, c in self.__taskobject.inputs.items():
            if not c['optional']:
                default_enable_socket_list.append( socket_name )

        sdesl = set(default_enable_socket_list)
        ssndk = set(socket_name_dict.keys())
        enable_socket_set = ssndk - sdesl

        for socket_name in enable_socket_set:
            self.checkInputSocketName(socket_name)

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

    def __changeOutputSocket(self, socket_name_dict):
        """Set whether the output socket is enable or not."""

        default_enable_socket_list = []
        for socket_name, c in self.__taskobject.outputs.items():
            if not c['optional']:
                default_enable_socket_list.append( socket_name )

        sdesl = set(default_enable_socket_list)
        ssndk = set(socket_name_dict.keys())
        enable_socket_set = sdesl ^ ssndk

        for socket_name in enable_socket_set:
            self.checkOutputSocketName(socket_name)

            enable = socket_name_dict[socket_name]
            socket = self.__outputs[socket_name]
            if enable:
                socket['enable'] = True
                socket['data'].enable(True)
            else:
                socket['enable'] = False
                socket['data'].enable(False)

    # Todo
    def __changeConcom(self, name_dict):
        pass


#===============================================================================
class DataOperatable:

    def convertInputData(self):
        """Convert input data to command-adaptable format data."""
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

    # Todo
    def checkInputData(self):
        for name in self.__taskobject.input_types:
            data = self.__inputs.get(name)
            if data:
                if data.is_empty(): 
                    return False
            else:
                return False
        return True

    # Todo
    def checkInputData(self):
        for key, fmt in self.__command.input_formats.items():
            formats = [ data.type for data in datas ]
            if fmt in formats:
                pass
            else:
                raise DataException()

    # Todo
    def checkOutputData(self):
        """"""

    # Todo
    def createInputData(self):
        """Generate the input data from taskobject."""
        for socket_name, c in self.__taskobject.inputs.items():
            if c['optional']:
                self.__inputs[socket_name] = {'data': None, 'enable': False}
            else:
                self.__inputs[socket_name] = {'data': None, 'enable': True}

    # Todo
    def createOutputData(self):
        """Generate the output data from taskobject."""
        for socket_name, c in self.__taskobject.outputs.items():
            data = Data(self.__project, type=c['type'])
            if c['optional']:
                data.enable(False)
                self.__outputs[socket_name] = {'data': data, 'enable': False}
            else:
                data.enable(True)
                self.__outputs[socket_name] = {'data': data, 'enable': True}



#===============================================================================
class SettingOperatable:

    def prepare_setting(self):
        setting_class = settingdata.setting_dict[self.__taskobject.setting]
        datas = self.__setting['datas']
        for option, value in datas.items():
            if value:
                if self.__taskobject.inputs.get(option):
                    self.__taskobject.inputs[option] = value
                if self.__taskobject.outputs.get(option):
                    self.__taskobject.outputs[option] = value

    def generateSetting(self, to_name):
        pass

    def prepare_setting(self):
        if not self.__setting:
            format = self.__taskobject.setting
            self.__setting = SettingData(format)
    
    def check_settings(self, setting_data):
        if setting_data.type == self.__taskobject.setting:
            return True
        else:
            return False
                
    def convert_setting(self):
        """convert by command converter from task object setting"""
        pass

    def isPreparedSetting(self):
        from validator import StandardSettiingValidator as SettingValidator
        sv = SettingValidator(self.__setting)
        if not sv.is_valid():
            raise InvalidSettingException()
        return True

#===============================================================================
class CommandOperatable:
    def checkCommand(self, cmd_str):
        if cmd_str in self.__config[self.remote.host]['commands']:
            return True
        else:
            return False


    def setCommand(self, cmd_str):
        """Set a command to this task."""
        if not self.checkCommand(cmd_str): pass
        self.__config[self.remote.host]['commands']
        self.__command = plugin.commands.commands_dict['cmt_str']

    def generateScript(self):
        pass


#===============================================================================
class SyncOperatable:
    pass




def new_main():
    """
    For Example:

        >>> import project
        >>> p = project.Project()
        >>> t = Task(p)
        >>> p.append_task(t)
        hoge

    request rename

        >>> t.name = 'hoge'
        >>> t.name
        'hoge'

    """

    def print_request_and_check(id, task, message, request_name, *args, **kwds):
        pre = task.state_name
        print
        print '='*80
        print str(id) + ': ' + message

        print request_name, args, kwds, ' at ', task.state_name
        print 'Available Request: ', list(task.getAvailableRequests())
        print ' ***** request log ********** '
        getattr(task, request_name)(*args, **kwds)
        print ' ***** input sockets ******** '
        for socket_name, d in task.inputs.items():
            print ' '*4 + socket_name, d
        print ' ***** output sockets ******* '
        for socket_name, d in task.outputs.items():
            print ' '*4 + socket_name, d
        aft = task.state_name
        print 'STATE TRANSITION: ' + pre + ' => ' + aft


    import project
    p = project.Project()
    t = Task(p)
    p.append_task(t)
    print t.name


    # 0 ############################
    print_request_and_check(
        0, t, '', 'requestRename', 'hoge'
    )
    print t.name

    import data
    system_data = Data(p, type='System')
    # group_data  = Data(p, type='group')

    i = 0
    ################################
    i+=1
    print_request_and_check(
        i, t, '', 'requestTest'
    )
    ################################
    i+=1
    try:
        print_request_and_check(
            i, t, '', 'requestSetTaskObject', 'optimize'
        )
    except data.DataTypeError as e:
        e.log()
    ################################
    i+=1
    socket_name = 'system'
    print_request_and_check(
        i, t, '', 'requestConnectInput', system_data, socket_name
    )
    ################################
    try:
        i+=1
        print_request_and_check(
            i, t, '',
            'requestChangeSocket', inputs={'restraint': True}
        )
    except CheckPreparedException as e:
        e.log()
    ################################
    i+=1
    print_request_and_check(
        i, t, 'do disable restraint socket',
        'requestChangeSocket', inputs={'restraint': False}
    )
    ################################
    i+=1
    print_request_and_check(
        i, t, 'do disable system socket',
        'requestChangeSocket', inputs={'system': False}
    )
    ################################
    i+=1
    print_request_and_check(
        i, t, 'disconnect the data from the system socket.',
        'requestDisconnectInput', 'system'
    )
    ################################
    i+=1
    print_request_and_check(
        i, t, '', 'requestRename', 'fuga'
    )
    print t.name
    ################################
    i+=1
    socket_name = 'system'
    print_request_and_check(
        i, t, '', 'requestConnectInput', system_data, socket_name
    )
    # to ready state
    i+=1
    socket_name = 'system'
    print_request_and_check(
        i, t, '', 'requestConnectInput', system_data, socket_name
    )


if __name__ == '__main__':
    new_main()


class TaskPiecePresenter(object):
    """docstring for TaskPiece"""
    def __init__(self, view, model=None):
        self.view = view
        self.model = model
        self.setting_agent = None

        self.__event_dict = {
            'setting_in_miniframe' : NagaraEvent() , 
            'setting_in_pane'      : NagaraEvent() , 
            'selected'             : NagaraEvent() , 
        }

    def showSettingInDialog(self):
        if self.settinge_agent is None: self.__setupSetting()
        # show dialog
        SettingDialog(self.setting_agent).start()
        # with SettingDialog(self.setting_agent) as dlg: pass

    def showSettingInPane(self):
        if self.settinge_agent is None: self.__setupSetting()
        self.setting_in_pane_event.fire(self.model.id)

    def showSettingInMiniFrame(self):
        if self.settinge_agent is None: self.__setupSetting()
        self.setting_in_miniframe_event.fire(self.model.id)

    def __setupSetting(self):
        # load setting agent class
        to_name = self.model.taskobject_name
        setting_class = plugin.loadSettingComponent(to_name)
        # setting_class = plugin.loadSettingComponent('optimize')

        # create setting_agent
        if self.model.setting is None:
            self.setting_agent = setting_class()
            self.model.setting = self.setting_agent.getModel()
        else:
            self.setting_agent = setting_class(self.model.setting)

    def select(self):
        self.selected_event.fire(self.model.id)

    # event attribute
    def __getattr__(self, attrname):
        if attrname.endswith('_event'):
            aname = attrname.replace('_event', '')
            return self.__event_dict(aname)
        else:
            raise AttributeError(attrname)


class IPane(Interface):
    pass

class IMiniFrame(Interface):
    pass

class IDialog(Interface):
    pass

