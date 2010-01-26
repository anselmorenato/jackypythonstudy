#! /opt/python2.6/bin/python
#  -*- encoding: utf-8 -*-
# Copyright (C)  2009 Takakazu Ishikura

# standard modules
import os, sys, datetime
from abc import ABCMeta, abstractmethod, abstractproperty
import wx

# nagara modules
from exception import NagaraException
# if __name__ == '__main__':
#     sys.path.append('../')
from log             import Log

# sys.path.append('..')
if __name__ == '__main__':
    sys.path.append('../utils')
from deco    import threaded
from pattern import Null
from event   import NagaraEvent


CHECK_TIME=1
SYNC_TIME_LIMIT=1000

################################################################################
# Task Local
################################################################################

# Task Local Class =============================================================
class TaskLocalException(NagaraException): pass
class TaskLocal(wx.EvtHandler):

    """
    The class to perform the local operations for task.
    """

    state_fn = '.nagara'

    def __init__(self, task):
        """Constructor."""
        self.__task = task
        self.initialize_event()

        # set the local path
        local_root = self.__task.project.rootpath
        date = datetime.datetime.today().strftime('%Y%m%d-%H%M%S')
        self.__dirname = '{0}.{1}'.format(date, self.__task.id)
        self.__path = os.path.join(local_root, self.__dirname)
        
        # set local state
        self.__state = LocalState(self)

    def initialize_event(self):
        wx.EvtHandler.__init__(self)
        self.__converted_event = NagaraEvent(self)
        self.__received_event  = NagaraEvent(self)

    # property: events
    @property
    def converted_event(self): return self.__converted_event

    @property
    def received_event(self): return self.__received_event

    # property: path
    @property
    def path(self):
        return self.__path

    # property: state
    def get_state(self):
        return self.__state
    def set_state(self, state):
        self.__state = __state
    state = property(get_state, set_state)

    # property: dirname
    def get_dirname(self):
        return self.__dirname
    def set_dirname(self, dirname):
        self.__dirname = __dirname
    dirname = property(get_dirname, set_dirname)

    def get_task(self):
        return self.__task

    # operations
    def create(self):
        """Make a local directory for task."""
        self.state.request_create(self)

    def convert(self):
        """Convert the datas for the input socket."""
        # convert statememt
        self.state.request_convert(self)

    def prepare(self):
        # generate all data and script 
        self.state.request_prepare(self)

    def transmit(self):
        # transmit all data of this task.
        self.state.request_transmit(self)

    def run(self):
        self.state.request_run(self)

    def stop(self):
        self.state.request.stop(self)

    def copy(self, dst_path):
        self.state.request_copy(self, dst_path)

    def move(self, dst_path):
        """Move the local directory to dst_path."""
        self.state.request_move(self, dst_path)

    def delete(self):
        """Delete the local directory."""
        self.state.request_delete(self)

    def show(self):
        pass

    def tail(self):
        pass

    # other methods
    def putFile(self, src_path, dst_fn):
        """Copy the external file to the task directory with dst_fn."""
        ldir = self.__path
        dst_base = os.path.basename(dst_fn)
        dst_path = os.path.join(ldir, dst_base)

        src_file = open(src_path, 'rb')
        dst_file = open(dst_path, 'wb')
        dst_file.write(src_file.read())
        src_file.close()
        dst_file.close()
        pass

    def save_data(self):
        pass

    def restore(self):
        pass

    def getFiles(self):
        pass

    def request_move(self, dst_abspath):
        if not os.path.exists(dst_abspath):
            os.rename(local_task.path, dst_path)
        else:
            raise CreatedLocalStateException()

    def request_clear(self):
        shutil.rmtree(task_local.path)
        task_local.state.change_to_init()

    # request_operations
    def is_converted(self):
        filenames = self.__task.get_all_in_files
        fn_exist_dict = {}
        for fn in filenames:
            abs_fn = os.path.join(self.__path, fn)
            fn_exist_dict[abs_fn] = True if os.path.exists(abs_fn) else False

        fn_set = set(fn_exist_dict.values())
        if len( fn_set ) == 1:
            ret = True if fn_set[0] else False
        else:
            ret = False
        return ret

    def is_received_calculated_files(self):
        filenames = self.__task.get_all_out_files
        fn_exist_dict = {}
        for fn in filenames:
            abs_fn = os.path.join(self.__path, fn)
            fn_exist_dict[abs_fn] = True if os.path.exists(abs_fn) else False

        fn_set = set(fn_exist_dict.values())
        if len( fn_set ) == 1:
            ret = True if fn_set[0] else False
        else:
            ret = False
        return ret

    def is_received(self, data):
        return True if not data.is_empty() else False

    @threaded
    def check_files(self):
        while True:
            if self.is_converted():
                self.converted_event.fire()
                break
            time.sleep(CHECK_TIME)

    @threaded
    def check_calculated_files(self):
        while True:
            if self.is_received_calculated_files():
                self.received_event.fire()
                break
            time.sleep(CHECK_TIME)

    def create(self):
        if not os.path.exists(self.__path):
            os.mkdir(self.__path)
        else:
            message = 'Local task directory already exists.'
            raise TaskLocalException(message)


# operations
# create, convert, prepare, transmit, run, stop, move, delete, copy, 
# show, tail

# Task Local State Class =======================================================
class LocalStateException(TaskLocalException): pass
class LocalState(object):

    __state_fn = '.nagara'

    def __init__(self, tasklocal):
        self.__tasklocal = tasklocal
        self.__generate_all_states()
        self.__bind_all_events()
        self.change_to_init()

    def __generate_all_states(self):
        self.__INIT_STATE      = InitLocalState(self.__tasklocal)
        self.__PREPARING_STATE = PreparingLocalState(self.__tasklocal)
        self.__READY_STATE     = ReadyLocalState(self.__tasklocal)
        self.__RECEIVING_STATE = ReceivingLocalState(self.__tasklocal)
        self.__COMPLETE_STATE  = CompleteLocalState(self.__tasklocal)
        self.__ERROR_STATE     = ErrorLocalState(self.__tasklocal)

    def __bind_all_events(self):
        self.__tasklocal.converted_event.bind( self.__converted_on_tasklocal )
        self.__tasklocal.received_event.bind(  self.__received_on_tasklocal  )

    def get_available_request(self):
        """Return available request in this state."""
        for med in self.__state.__class__.__dict__:
            if med.startswith('request_'): yield med

    def entry(self):
        self.log()
        self.write_state()
        try:
            self.__state.entry()
        except AttributeError:
            pass

    @property
    def previous(self):
        return self.__previous

    def change_to_init(self):
        self.__previous = None
        self.__state = self.__INIT_STATE
        self.log()
        try:
            getattr(self.__state, 'entry')
            self.__state.entry()
        except AttributeError:
            pass

    def change_to_preparing(self):
        self.__previous = self.__state
        self.__state = self.__PREPARING_STATE
        self.entry()

    def change_to_ready(self):
        self.__previous = self.__state
        self.__state = self.__READY_STATE
        self.entry()

    def change_to_receiving(self):
        self.__previous = self.__state
        self.__state = self.__RECEIVING_STATE
        self.entry()

    def change_to_complete(self):
        self.__previous = self.__state
        self.__state = self.__COMPLETE_STATE
        self.entry()

    def change_to_error(self):
        self.__previous = self.__state
        self.__state = self.__ERROR_STATE
        self.entry()

    # event handlers
    def __converted_on_tasklocal(self, event):
        Log('converted_on_tasklocal')
        try:
            self.__state.receive_converted_event()
        except AttributeError:
            pass

    def __received_on_tasklocal(self, event):
        Log('received_on_tasklocal')
        try:
            self.__state.receive_received_event()
        except AttributeError:
            pass

    def log(self):
        name = self.__state.__class__.__name__
        message = 'LocalState: ' + 'was set to ' + name
        Log(message)

    def __getattr__(self, attrname):
        try:
            return getattr(self.__state, attrname)
        except AttributeError:
            return Null()

    def write_state(self):
        state = self.__state
        state_path = os.path.join(self.__tasklocal.path, self.__state_fn)
        with open(state_path, 'wb') as f:
            f.write(state.__class__.__name__)

    def read_state(self):
        if os.path.exists(self.__tasklocal.path):
            state_path = os.path.join(self.__tasklocal.path, self.__state_fn)
            with open(state_path, 'rb') as f:
                state = f.read()
            return state
        else:
            return 'NoneLocalState'


# Concrete Local States ========================================================
class InitLocalState(object):

    def __init__(self, tasklocal):
        self.__tasklocal = tasklocal

    def entry(self):
        self.__tasklocal.create()


class PreparingLocalState(object):

    def __init__(self, tasklocal):
        self.__tasklocal = tasklocal

    def receive_converted_event(self):
        self.__tasklocal.state.change_to_ready()


class ReadyLocalState(object):

    def __init__(self, tasklocal):
        self.__tasklocal = tasklocal

    def entry(self):
        self.__tasklocal.get_task().state.change_to_converted()


class ReceivingLocalState(object):

    def __init__(self, tasklocal):
        self.__tasklocal = tasklocal

    def receive_received_event(self):
        self.__tasklocal.state.change_to_complete()


class CompleteLocalState(object):

    def __init__(self, tasklocal):
        self.__tasklocal = tasklocal

    def entry(self):
        self.__tasklocal.get_task().state.change_to_complete()


class ErrorLocalStateException(LocalStateException): pass
class ErrorLocalState(object):

    def __init__(self, tasklocal):
        self.__tasklocal = tasklocal


if __name__ == '__main__':
    import task, project
    p = project.Project()
    t = task.Task(p)

    t.state.request_set_taskobject('energy')
    t.state.request_any_operations()

