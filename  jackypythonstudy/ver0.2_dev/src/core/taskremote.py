#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura
#
# $Date$
# $Rev$
# $Author$
#

# standard modules
import os, sys
from abc import ABCMeta, abstractmethod, abstractproperty

# nagara modules
from exception  import NagaraException
from connection import Connection, ConnectionException

# if __name__ == '__main__':
#     sys.path.append('../')

nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )

from log       import Log
from config    import Config

if __name__ == '__main__':
    sys.path.append('../utils')
from utils.deco    import threaded
from utils.pattern import Null
from utils.event   import NagaraEvent, EventBindManager


CHECK_TIME=1
SYNC_TIME_LIMIT=1000

################################################################################
# Task Remote 
################################################################################

# Task Remote Exceptions =======================================================
class TaskRemoteException(NagaraException): pass
class TaskRemoteReceivingError(TaskRemoteException): pass

# Task Remote Class ============================================================
class TaskRemote(object):

    """
    The class to perform the remote operations for task.
    """
    state_fn = '.nagara'

    def __init__(self, task, use_network=True):
        """Constructor."""
        self.__task = task
        self.initialize_event()
        self.__configs = Config().get_common()['location']

        self.__state = RemoteState(self)

    def initialize_event(self):
        self.__received_event  = NagaraEvent()

    # property: events
    @property
    def received_event(self):
        return self.__received_event

    # property: path
    @property
    def path(self):
        """Return the remote absolute path."""
        return self.__path

    def get_channel(self):
        return self.__channel

    # property: host
    def get_host(self):
        return self.__host
    def set_host(self, host):
        self.__host = host
        dirname = self.__task.local.dirname
        self.__nagara_root = self.__configs[self.__host]['workdir']
        self.__path = self.__nagara_root + '/' + self.__task.local.dirname
    host = property(get_host, set_host)
    

    def connect(self):
        """Connect to remote host by config."""
        if self.__channel:
            if ( socket.gethostbyname(self.__host) != 
                self.__channel.get_host_by_ip() ):
                if self.__channel.is_communicating():
                    raise connection.ConnectionException()
                else:
                    self.__channel.close()
                    try:
                        host_config = self.__configs[self.__host]['ssh']
                    except:
                        message = 'Not found host configuration.'
                        raise TaskRemoteException(message)

                    self.__channel = Connection(
                        host     = host_config['address'],
                        username = host_config['username'],
                        password = host_config['password'],
                    ) 
            else:
                pass

        else:
            if self.__host:
                try:
                    host_config = self.__configs[self.__host]['ssh']
                except:
                    message = 'Not found host configuration.'
                    raise TaskRemoteException(message)

                self.__channel = Connection(
                    host     = host_config['address'],
                    username = host_config['username'],
                    password = host_config['password'],
                ) 

            else:
                self.__host = self.__configs['default']
                try:
                    host_config = self.__configs[self.__host]['ssh']
                except:
                    message = 'Not found host configuration.'
                    raise TaskRemoteException(message)

                self.__channel = Connection(
                    host     = host_config['address'],
                    username = host_config['username'],
                    password = host_config['password'],
                ) 

    def create(self):
        """Create the remote task directory."""
        configs = self.__task.get_configs()
        host = self.__task.host
        remote_root = configs[host]['rootdir']
        chan = self.__task.get_channel()

        if not chan.exists(remote_root):
            chan.mkdir(remote_root)

        if not chan.exists(self.__path):
            chan.mkdir(self.__path)

    # def setConnection(self, conn):
    #     """Set the connection to remote host."""
    #     self.__conn = conn

    # def getConnection(self):
    #     """Get the connection to remote host."""
    #     return self.__conn

    def receive_all(self, force=False):
        """Put the local task to a directory on the remote project dir."""
        try:
            local_dir_
            local_dir_path = self.__task.local.path
            self.__channel.putdir(local_dir_path, self.__path)
            self.received_event.fire()
        except:
            raise TaskRemoteReceivingError()

    def receive_file(self, fn):
        try:
            local_dir_path = self.__task.local.path
            local_fn = os.path.join(local_dir_path, fn)
            remote_fn = self.__path + '/' + fn
            self.__channel.put(local_fn, remote_fn)
        except:
            raise TaskRemoteReceivingError()

    def send_all(self):
        self.__task.getdir
        output_file_list = self.__task.get_all_out_files()
        other_file_list  = self.__task.get_all_con_files()
        try:
            local_dir_path = self.__task.local.path
            self.__channel.getdir(rdir, ldir)
            
            rdir = self.__path
            conn = self.__task.getConnection()
            conn.getDir(rdir, ldir)
        except:
            pass

    def send_file(self, remote_fn):
        pass
        #self.__channel
        # return conn.get(remote_fn, self.__task.local.getPath())

    @threaded
    def tail(self, remote_fn, output):
        conn = self.__task.getConnection()
        rfile = conn.open(remote_fn, mode='r', pipeline=True)
        while True:
            where = rfile.tell()
            line = rfile.readline()
            if not line:
                time.sleep(10)
                rfile.seek(where)
            else:
                output.write(line), # already has newline
                # or + generator + external method

    def is_local(self):
        return False

    def do_excecutable(self):
        conn.execute('chmod u+x '+ run_script)

    @threaded
    def check_files(self):
        # task_remote.receive_all_files()
        time_sum = 0
        while True:
            if self.is_received_all_files(): break
            time.sleep(CHECK_TIME)
            time_sum += CHECK_TIME
            if time_sum >= SYNC_TIME_LIMIT:
                raise ReceivingRemoteStateException()

        self.__state.change_to_runnable()

    def define_host(self):
        pass

    def delete(self):
        """Delete the remote directory."""
        if not self.isNone():
            self.__task.getConnection().execute('rm -rf '+self.__path)
            self.setNone()


# Remote State Class ===========================================================
class RemoteStateException(TaskRemoteException): pass
class RemoteState(object):

    __state_fn = '.nagara'
    binder = EventBindManager()

    def __init__(self, taskremote):
        self.__taskremote = taskremote
        self.__generate_all_states()
        self.binder.bind_all(self)
        self.change_to_none()

    def __generate_all_states(self):
        self.__NONE_STATE      = NoneRemoteState(self.__taskremote)
        self.__INIT_STATE      = InitRemoteState(self.__taskremote)
        self.__RECEIVING_STATE = ReceivingRemoteState(self.__taskremote)
        self.__RUNNABLE_STATE  = RunnableRemoteState(self.__taskremote)
        self.__RUNNING_STATE   = RunningRemoteState(self.__taskremote)
        self.__DONE_STATE      = DoneRemoteState(self.__taskremote)
        self.__SENDING_STATE   = SendingRemoteState(self.__taskremote)
        self.__ERROR_STATE     = ErrorRemoteState(self.__taskremote)

    def get_available_request(self):
        """Return available request in this state."""
        for med in self.__state.__class__.__dict__:
            if med.startswith('request_'): yield med

    def log(self):
        name = self.__state.__class__.__name__
        message = 'RemoteState: ' + 'was set to ' + name
        Log(message)

    def __getattr__(self, attrname):
        try:
            return getattr(self.__state, attrname)
        except AttributeError:
            return Null()

    @property
    def previous(self):
        return self.__previous

    def entry(self):
        self.log()
        self.write_state()
        try:
            self.__state.entry()
        except AttributeError:
            pass

    def change_to_none(self):
        self.__previous = None
        self.__state = self.__NONE_STATE
        self.log()
        try:
            getattr(self.__state, 'entry')
            self.__state.entry()
        except AttributeError:
            pass

    def change_to_init(self):
        self.__previous = self.__state
        self.__state = self.__INIT_STATE
        self.entry()

    def change_to_receiving(self):
        self.__previous = self.__state
        self.__state = self.__RECEIVING_STATE
        self.entry()

    def change_to_runnable(self):
        self.__previous = self.__state
        self.__state = self.__RUNNABLE_STATE
        self.entry()

    def change_to_running(self):
        self.__previous = self.__state
        self.__state = self.__RUNNING_STATE
        self.entry()

    def change_to_done(self):
        self.__previous = self.__state
        self.__state = self.__DONE_STATE
        self.entry()

    def change_to_sending(self):
        self.__previous = self.__state
        self.__state = self.__SENDING_STATE
        self.entry()

    def change_to_error(self):
        self.__previous = self.__state
        self.__state = self.__ERROR_STATE
        self.entry()

    # event handlers
    @binder('__taskremote.received_event')
    def __received_on_taskremote(self, msg):
        self.__log_recieve('__received_on_taskremote')
        try:
            self.__state.receive_received_event()
        except AttributeError:
            pass

    def write_state(self):
        chan = self.__taskremote.get_channel()
        if self.__taskremote.is_local():
            state_path = os.path.join(self.__taskremote.path, self.__state_fn)
        else:
            state_path = self.__taskremote.path + '/' + self.__state_fn
        file = chan.open(state_path, 'wb')
        file.write(state.__class__.__name__)
        file.close()

    def read_state(self):
        chan = self.__taskremote.get_channel()
        if chan.exists(self.__path):
            if self.__taskremote.is_local():
                state_path = os.path.join(
                    self.__taskremote.path, self.__state_fn)
            else:
                state_path = self.__taskremote.path + '/' + self.__state_fn
            rfile = open(state_path, 'rb')
            state = rfile.read()
            rfile.close()
            return state
        else:
            return 'NoneRemoteState'

    def __log_recieve(self, listener_name):
        info_list = self.binder.get_info(listener_name)
        for info in info_list:
            obj = info['object_name']
            evt = info['event_name']
            cls = info['class_name']
            mes = 'Recieved {0} of {1}:{2} at {3}'
            Log( mes.format(evt, obj, cls, listener_name) )


# Concrete Remote States =======================================================
class NoneRemoteState(object):

    def __init__(self, taskremote):
        self.__taskremote = taskremote


class InitRemoteState(object):

    def __init__(self, taskremote):
        self.__taskremote = taskremote

    def entry(self):
        self.__taskremote.define_host()
        self.__taskremote.create()


class ReceivingRemoteStateException(RemoteStateException): pass
class ReceivingRemoteState(object):

    def __init__(self, taskremote):
        self.__taskremote = taskremote

    def receive_received_event(self):
        self.__taskremote.state.change_to_runnable()


class RunnableRemoteStateException(RemoteStateException): pass
class RunnableRemoteState(object):
    
    def __init__(self, taskremote):
        self.__taskremote = taskremote

    def entry(self):
        name = self.__taskremote.get_task().name
        Log(name + ': all files sended.')
        self.__taskremote.do_excutable()
        self.__taskremote.get_task().state.change_to_runnable()


class RunningRemoteStateException(RemoteStateException): pass
class RunningRemoteState(object):

    def __init__(self, taskremote):
        self.__taskremote = taskremote


class DoneRemoteStateException(RemoteStateException): pass
class DoneRemoteState(object):

    def __init__(self, taskremote):
        self.__taskremote = taskremote

    def entry(self):
        if isinstance(self.__taskremote.state.previous, SendingLocalState):
            task = self.__taskremote.get_task()
            task.local.state.change_to_complete()
        else:
            pass

    def request_receive(self):
        self.__taskremote.send_all_files()


class SendingRemoteStateException(RemoteStateException): pass
class SendingRemoteState(object):

    def __init__(self, taskremote):
        self.__taskremote = taskremote

    def entry(self):
        task = self.__taskremote.get_task()
        self.__task.state.change_to_receiving()
        self.__taskremote.send_all_files()


class ErrorRemoteStateException(RemoteStateException): pass
class ErrorRemoteState(object):

    def __init__(self, taskremote):
        self.__taskremote = taskremote



if __name__ == '__main__':

    import task, project
    p = project.Project()
    t = task.Task(p)

    t.state.request_set_taskobject('energy')
    t.state.request_any_operations()
    
    tr = t.remote

    from pubsub.utils import printTreeDocs
    printTreeDocs(extra="a")
    print '\nTopic tree listeners:'
    printTreeDocs(extra="L")
