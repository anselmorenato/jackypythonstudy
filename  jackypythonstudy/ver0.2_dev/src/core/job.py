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

# pypi modules
# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from exception import NagaraException
from config     import Config
from log       import Log
from utils.pattern   import Null
from utils.event     import NagaraEvent


# Exceptions ===================================================================
class JobException(NagaraException): pass
class JobStateException(JobException): pass


# Base state ===================================================================


class Job(object):

    """
    The class to define Job.
    """

    def __init__(self, task):
        self.__task = task
        self.__nproc = 1
        self.__node_distribution = ('intensive', 'not essential')

        # other objects
        self.__name = None
        self.__jms = None

        # setup configuration
        self.__config = Config().get_common()['location']

        # generate event
        self.__state_changed_event = NagaraEvent()

        # create job state
        self.__state = JobState(self)

        # auto setting
        self.__use_auto = False

    # properties
    @property
    def task(self):
        return self.__task

    @property
    def state(self):
        return self.__state
        
    # property: host
    def get_host(self):
        return self.__host
    def set_host(self, host):
        self.__host = host
        self.__task.remote.host = host
    host = property(get_host, set_host)

    def get_available_hosts(self):
        return self.__configs['common']['remote']

    # property: nproc
    def get_nproc(self):
        return self.__nproc
    def set_nproc(self, nproc):
        self.__nproc = __nproc
    nproc = property(get_nproc, set_nproc)

    # property: nnode
    def get_nnode(self):
        return self.__nnode
    def set_nnode(self, nnode):
        self.__nnode = __nnode
    nnode = property(get_nnode, set_nnode)

    # property: expected time
    def get_expected_time(self):
        return self.__expected_time
    def set_expected_time(self, etime):
        self.__expected_time = etime
    expected_time = property(get_expected_time, set_expected_time)

    # property: start time
    def get_start_time(self):
        return self.__start_time
    def set_start_time(self, stime):
        self.__start_time = stime
    start_time = property(get_start_time, set_start_time)

    # property: end time
    def get_end_time(self):
        return self.__end_time
    def set_end_time(self, etime):
        self.__end_time = __end_time
    end_time = property(get_end_time, set_end_time)

    def get_jms_list(self):
        jms_list = self.__config[self.__host]['jms'].keys()
        return set(jms_list) ^ set(['default'])

    # property: jms string
    def get_jms(self):
        return self.__jms_str
    def set_jms(self, jms_str):
        if jms_str not in self.get_jms_list():
            raise JobJMSException()
        self.__jms_str = jms_str
    jms_str = property(get_jms, set_jms)

    def create_jms(self):
        jms_config = self.__config['common']['location'][self.__host]['jms']
        jms_str = jms_config[jms_str]
        self.__jms = jms.get_jms(jms)

    def setup_jms(self):
        self.__jms.set_resources(
            nproc=self.__nproc, nnode=self.__nnode, node_list=self.__node_list,
        )
        self.jms.set_intensive( self.is_intensive() )

    def get_distribution(self):
        d = self.__node_distribution
        if   d == ('intensive', 'essential'): return 0
        elif d == ('intensive', 'not essential'): return 1
        elif d == ('dispersion', 'essential'): return 2
        elif d == ('dispersion', 'not essential'): return 3
        else: raise JobError()

    def set_distribution(self, i):
        if   i == 0: d == ('intensive', 'essential')
        elif i == 1: d == ('intensive', 'not essential')
        elif i == 2: d == ('dispersion', 'essential')
        elif i == 3: d == ('dispersion', 'not essential')
        else: raise JobError()
        self.__node_distribution = d

    def is_intensive(self):
        if self.__node_distribution[0] == 'intensive':
            ret = True
        else:
            ret = False
        return  ret

    def is_auto(self):
        return self.__use_auto

    def setup(self):
        self.__job_path = self.__task.remote.path
        self.__channel  = self.__task.remote.get_channel()
        self.__host = self.__task.remote.get_host()


#===========================
    # checker
    def check_ncore(self):
        x, y, free_cores = jms.get_core_info()
        if ncore > free_cores:
            raise JobCoreException()

    def check_channel(self):
        """Check a remote connection."""
        if not self.__channel:
            raise JobChannelException()
        if not self.__channel.available():
            raise JobChannelException()

    def __setup_jobpath(self):
        # remote_path format : username@host:path
        ssh = self.__configs['location'][self.__host]['ssh']
        ssh['address']
        ssh['password']
        ssh['username']
        pass

    def getRemoteInfo(self):
        """Return remote info: user name, host and working path."""
        rpath = self.remote.getPath()
        if rpath.find('@') >= 0:
            username, tmp = rpath.split('@')
        else:
            username = None
            tmp = rpath

        if tmp.find(':') >=0:
            host, path = tmp.split(':')
        else:
            host = None
            path = tmp
        return username, host, path

#===========================




    # public operations
    def get_available_request(self):
        return list(self.state.get_available_request())

    def change_auto(self, b=False):
        self.state.request_change_auto(self, b)

    def set_node_list(self, node_list=[]):
        self.__node_list = node_list

    def submit(self):
        self.state.request_submit(self)

    def stop(self):
        self.state.request_stop(self)

    def cancel(self):
        self.state.request_cancel(self)

    def convert(self):
        self.state.request_convert(self)

    def send(self):
        self.state.request_send(self)

    def run(self):
        self.state.request_run(self)

    def select_host(self, host=None):
        self.state.request_select_host(self, host)

    def force_cancel(self):
        self.state.request_force_cancel(self)

    def show_error(self):
        self.state.request_show_error(self)

    def delete(self):
        pass

    # checker
    def is_host_selected(self):
        if self.host:
            ret = True
        else:
            ret = False
        return ret

    # event
    @property
    def state_changed_event(self):
        return self.__state_changed_event


# Job State Class =============================================================
class JobStateException(JobException): pass
class JobState(object):

    def __init__(self, job):
        self.__job = job
        self.__generate_all_states()
        self.change_to_preparing()

    def __generate_all_states(self):
        # standard states
        self.__PREPARING_STATE  = PreparingJobState(self.__job)
        self.__PREPARED_STATE   = PreparedJobState(self.__job)
        self.__READY_STATE      = ReadyJobState(self.__job)
        self.__CONVERTING_STATE = ConvertingJobState(self.__job)
        self.__CONVERTED_STATE  = ConvertedJobState(self.__job)
        self.__SENDING_STATE    = SendingJobState(self.__job)
        self.__RUNNABLE_STATE   = RunnableJobState(self.__job)
        self.__QUERYING_STATE   = QueryingJobState(self.__job)
        self.__PENDING_STATE    = PendingJobState(self.__job)
        self.__RUNNING_STATE    = RunningJobState(self.__job)
        self.__STOPPING_STATE   = StoppingJobState(self.__job)
        self.__DONE_STATE       = DoneJobState(self.__job)

        # error states
        self.__RUNNING_ERROR    = RunningErrorJobState(self.__job)

    def get_available_request(self):
        """Return available request in this state."""
        for med in self.__state.__class__.__dict__:
            if med.startswith('request_'): yield med

    @property
    def previous(self):
        return self.__previous

    def entry(self):
        self.log()
        self.__job.state_changed_event.fire()
        try:
            self.__state.entry()
        except AttributeError:
            pass

    # change to state
    def change_to_preparing(self):
        self.__previous = None
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

    def change_to_querying(self):
        self.__previous = self.__state
        self.__state = self.__QUERYING_STATE
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

    def change_to_done(self):
        self.__previous = self.__state
        self.__state = self.__DONE_STATE
        self.entry()

    def change_to_running_error(self):
        self.__previous = self.__state
        self.__state = self.__RUNNING_ERROR_STATE
        self.entry()

    def log(self):
        name = self.__state.__class__.__name__
        message = 'JobState: ' + 'was set to ' + name
        Log(message)

    def __getattr__(self, attrname):
        try:
            return getattr(self.__state, attrname)
        except AttributeError:
            return Null()

    # common request
    def request_change_auto(self, b=True):
        self.__use_auto = b


# Concrete Job State Class ====================================================
class PreparingJobState(object):

    def __init__(self, job):
        self.__job = job


class PreparedJobState(object):

    def __init__(self, job):
        self.__job = job

#     def request_select_location(self, job):
#         job.state.change_to_ready()


class ReadyJobStateException(JobStateException): pass
class ReadyJobState(object):

    def __init__(self, job):
        self.__job = job

    def entry(self):
        if self.__job.is_auto:
            self.request_convert()

    def request_select_host(self, host=None):
        self.__job.host = host

    def request_convert(self):
        self.__job.task.state.request_convert()


class ConvertingJobState(object):

    def __init__(self, job):
        self.__job = job


class ConvertedJobState(object):

    def __init__(self, job):
        self.__job = job

    def request_select_host(self, host=None):
        self.__job.host = host

    def request_send(self):
        if self.__job.is_host_selected():
            self.__job.task.state.request_send()
        else:
            message = 'Host is not set.'
            raise HostJobError(message)


class SendingJobState(object):

    def __init__(self, job):
        self.__job = job


class RunnableJobState(object):

    def __init__(self, job):
        self.__job = job

    def entry(self):
        self.__job.create_jms()
        self.__job.setup()

        if job.is_auto:
            self.request_submit()

    def request_submit(self):
        self.__job.setup_jms()
        self.__job.state.change_to_querying()
        self.__job.jms.state.request_submit()


class QueryingJobState(object):

    def __init__(self, job):
        self.__job = job

    def request_force_cancel(self):
        pass


class PendingJobStateException(JobStateException): pass
class PendingJobState(object):

    def __init__(self, job):
        self.__job = job

    def entry(self):
        self.__job.task.state.change_to_pending()

    def request_cancel(self):
        self.__job.state.change_to_querying()
        self.__job.jms.state.request_cancel()


class RunningJobStateException(JobStateException): pass
class RunningJobState(object):

    def __init__(self, job):
        self.__job = job

    def entry(self):
        self.__job.task.state.change_to_running()

    def request_stop(self):
        self.__job.state.change_to_querying()
        self.__job.jms.state.request_stop()

    def request_cancel(self):
        self.__job.state.change_to_querying()
        self.__job.jms.state.request_cancel()


class StoppingJobStateException(JobStateException): pass
class StoppingJobState(object):

    def __init__(self, job):
        self.__job = job

    def entry(self):
        self.__job.task.state.change_to_stopping()

    def request_run(self):
        self.__job.state.change_to_querying()
        self.__job.jms.state.request_run()

    def request_cancel(self):
        self.__job.state.change_to_querying()
        self.__job.jms.state.request_cancel()


class DoneJobStateException(JobStateException): pass
class DoneJobState(object):

    def __init__(self, job):
        self.__job = job

    def entry(self):
        self.__job.task.state.change_to_done()


class RunningErrorJobStateException(object): pass
class RunningErrorJobState(object):

    def __init__(self, job):
        self.__job = job

    def entry(self):
        if self.__job.jms.error_exc:
            raise self.__job.jms.error_exc
        elif self.__job.jms.fail_exc:
            raise self.__job.jms.fail_exc
        else:
            raise RunningErrorJobStateException()

    def request_show_error(self):
        if self.__job.jms.error_exc:
            Log( self.__job.jms.error_exc )
        elif self.__job.jms.fail_exc:
            Log( self.__job.jms.fail_exc )
        else:
            raise RunningErrorJobStateException()

def main1():
    import task, project
    p = project.Project()
    t = task.Task(p)

    t.state.request_set_taskobject('energy')
    t.state.request_any_operations()

    j = t.job

def main2():
    from pattern import Null
    Job(Null())


if __name__ == '__main__':
    main2()
    



