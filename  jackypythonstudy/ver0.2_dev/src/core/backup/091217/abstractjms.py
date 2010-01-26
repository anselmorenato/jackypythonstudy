#! /opt/python2.6/bin/python
# _*_ encoding: utf-8 _*_
# Copyright (C)  2008 - 2009/11/22 Takakazu Ishikura

# standard modules
import os, sys
from optparse import OptionParser, OptionValueError
from abc import abstractmethod, abstractproperty, ABCMeta
import time
import wx

# nagara modules
from exception import NagaraException
import connection
from log import Log
if __name__ == '__main__':
    sys.path.append('../utils')
from event   import NagaraEvent
from pattern import Null
from deco    import threaded

CHECK_TIME=0.01
# CHECK_RUN_TIME=60
CHECK_RUN_TIME=0.01
CHECK_DONE_TIME=300

# JMS: Job Management System


# JMS exceptions ===============================================================
class JMSException(NagaraException): pass

class JMSError(JMSException):      pass
class JMSSubmittedError(JMSError): pass
class JMSRunningError(JMSError):   pass
class JMSProgramError(JMSError):   pass

class ProgramError(JMSException):     pass
class InitilizedError(ProgramError):  pass
class CalculationError(ProgramError): pass

# Abstract class ===============================================================
class IJobManagerSystem(wx.EvtHandler):

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_job_info(self): pass

    @abstractmethod
    def get_submit_command(self): pass

    # @abstractmethod
    # def get_id(self): pass

    # request to jms
    @abstractmethod
    def do_submit(self): pass

    @abstractmethod
    def do_rerun(self): pass

    @abstractmethod
    def do_stop(self): pass

    @abstractmethod
    def do_cancel(self): pass

    # check state
    @abstractmethod
    def is_pending(self): pass

    @abstractmethod
    def is_running(self): pass

    @abstractmethod
    def is_stopping(self): pass

    @abstractmethod
    def is_done(self): pass

    @abstractmethod
    def is_canceled(self): pass

    def initialize(self):
        wx.EvtHandler.__init__(self)
        self.initialize_event()
        self.initialize_other()

    def initialize_other(self):
        self._error = None
        self._fail  = None
        self._state = JMSState(self)

    def initialize_event(self):
        self._pend_event   = NagaraEvent(self)
        self._stop_event   = NagaraEvent(self)
        self._run_event    = NagaraEvent(self)
        self._done_event   = NagaraEvent(self)
        self._cancel_event = NagaraEvent(self)
        self._error_event  = NagaraEvent(self)
        self._fail_event   = NagaraEvent(self)

    # properties
    @property
    def job(self): return self._job

    @property
    def state(self): return  self._state

    @property
    def error_exc(self): return self._error

    @property
    def fail_exc(self): return self._fail

    # property: events
    @property
    def pend_event(self): return self._pend_event

    @property
    def stop_event(self): return self._stop_event

    @property
    def run_event(self): return self._run_event

    @property
    def done_event(self): return self._done_event

    @property
    def cancel_event(self): return self._cancel_event

    @property
    def error_event(self): return self._error_event

    @property
    def fail_event(self): return self._fail_event

    # background check
    @threaded
    def check_submit(self):
        self.do_submit()
        while True:
            try:
                if self.is_pending():
                    self.pend_event.fire()
                    break
                if self.is_running():
                    self.run_event.fire()
                    break
            except JMSError as e:
                self._error = e
                self.error_event.fire()
                break
            time.sleep(CHECK_TIME)

    @threaded
    def check_stop(self):
        self.do_stop()
        while True:
            try:
                if self.is_stopping():
                    self.stop_event.fire()
                    break
            except JMSError as e:
                self._error = e
                self.error_event.fire()
                break
            time.sleep(CHECK_TIME)

    @threaded
    def check_cancel(self):
        self.do_cancel()
        while True:
            try:
                if self.is_canceled():
                    self.cancel_event.fire()
                    break
            except JMSError as e:
                self._error = e
                self.error_event.fire()
                break
            time.sleep(CHECK_TIME)

    @threaded # when pending
    def check_run(self):
        while True:
            try:
                if self.is_running():
                    self.run_event.fire()
                    break
            except JMSError as e:
                self._error = e
                self.error_event.fire()
                break
            time.sleep(CHECK_RUN_TIME)

    @threaded
    def check_rerun(self):
        while True:
            try:
                if self.is_running():
                    self.run_event.fire()
                    break
            except JMSError as e:
                self._error = e
                self.error_event.fire()
                break
            time.sleep(CHECK_TIME)

    @threaded
    def check_done(self):
        while True:
            try:
                if self.is_done():
                    self.done_event.fire()
                    break
            except JMSError as e:
                self._error = e
                self.error_event.fire()
            except ProgramError as e:
                self._fail = e
                self.fail_event.fire()
                break
            time.sleep(CHECK_DONE_TIME)

    def set_resources(self, nproc=1, nnode=1, node_list=[]):
        self._nproc = nproc
        self._nnode = nnode
        self._node_list = node_list

# JMS State Class ==============================================================
class JMSStateException(JMSException): pass
class JMSState(object):

    def __init__(self, jms):
        self.__jms = jms
        self.__generate_all_states()
        self.__bind_all_events()
        self.change_to_entry()

    def __generate_all_states(self):
        # standard states
        self.__ENTRY_STATE    = EntryJMSState(self.__jms)
        self.__QUERYING_STATE = QueryingJMSState(self.__jms)
        self.__PENDING_STATE  = PendingJMSState(self.__jms)
        self.__RUNNING_STATE  = RunningJMSState(self.__jms)
        self.__STOPPING_STATE = StoppingJMSState(self.__jms)
        self.__DONE_STATE     = DoneJMSState(self.__jms)

        # error states
        self.__ERROR_STATE    = ErrorJMSState(self.__jms)   # occured from JMS
        self.__FAILED_STATE   = FailedJMSState(self.__jms)  # occured from calculation

    def __bind_all_events(self):
        self.__jms.pend_event.bind(  self.__pend_on_jms  )
        self.__jms.stop_event.bind(  self.__stop_on_jms  )
        self.__jms.run_event.bind(   self.__run_on_jms   )
        self.__jms.done_event.bind(  self.__done_on_jms  )
        self.__jms.cancel_event.bind(self.__cancel_on_jms)
        self.__jms.error_event.bind( self.__error_on_jms )
        self.__jms.fail_event.bind(  self.__fail_on_jms  )

    def get_available_request(self):
        """Return available request in this state."""
        for med in self.__state.__class__.__dict__:
            if med.startswith('request_'): yield med

    @property
    def previous(self):
        return self.__previous

    def entry(self):
        self.log()
        try:
            self.__state.entry()
        except AttributeError:
            pass

    # change to state
    def change_to_entry(self):
        self.__previous = None
        self.__state = self.__ENTRY_STATE
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

    def change_to_error(self):
        self.__previous = self.__state
        self.__state = self.__ERROR_STATE
        self.entry()

    def change_to_failed(self):
        self.__previous = self.__state
        self.__state = self.__FAILED_STATE
        self.entry()

    def log(self):
        name = self.__state.__class__.__name__
        message = 'JMSState: ' + 'was set to ' + name
        Log(message)

    def __getattr__(self, attrname):
        try:
            return getattr(self.__state, attrname)
        except AttributeError:
            return Null()

    # event handlers
    def __pend_on_jms(self, event):
        Log('pend_on_jms')
        try:
            self.__state.receive_pend_event()
        except AttributeError:
            pass

    def __stop_on_jms(self, event):
        Log('stop_on_jms')
        try:
            self.__state.receive_stop_event()
        except AttributeError:
            pass

    def __run_on_jms(self, event):
        Log('run_on_jms')
        try:
            self.__state.receive_run_event()
        except AttributeError:
            pass

    def __done_on_jms(self, event):
        Log('done_on_jms')
        try:
            self.__state.receive_done_event()
        except AttributeError:
            pass

    def __cancel_on_jms(self, event):
        Log('cancel_on_jms')
        try:
            self.__state.receive_cancel_event()
        except AttributeError:
            pass

    def __error_on_jms(self, event):
        Log('error_on_jms')
        try:
            self.__state.receive_error_event()
        except AttributeError:
            pass

    def __fail_on_jms(self, event):
        Log('fail_on_jms')
        try:
            self.__state.receive_fail_event()
        except AttributeError:
            pass


# Concrete JMS States ==========================================================

class EntryJMSState(object):

    def __init__(self, jms):
        self.__jms = jms

    def request_submit(self):
        self.__jms.state.change_to_querying()
        self.__jms.check_submit()


class PendingJMSState(object):

    def __init__(self, jms):
        self.__jms = jms

    def entry(self):
        self.__jms.job.state.change_to_pending()
        self.__jms.check_run()

    def receive_run_event(self):
        self.__jms.state.change_to_running()

    def receive_error_event(self):
        self.__jms.state.change_to_error()


class RunningJMSState(object):

    def __init__(self, jms):
        self.__jms = jms

    def entry(self):
        self.__jms.job.state.change_to_running()
        self.__jms.check_done()

    def request_cancel(self):
        self.__jms.state.change_to_querying()
        self.__jms.check_cancel()

    def request_stop(self):
        self.__jms.state.change_to_querying()
        self.__jms.check_stop()

    def receive_done_event(self):
        self.__jms.state.change_to_done()

    def receive_fail_event(self):
        self.__jms.state.change_to_failed()

    def receive_error_event(self):
        self.__jms.state.change_to_error()


class StoppingJMSState(object):

    def __init__(self, jms):
        self.__jms = jms

    def entry(self):
        self.__jms.job.state.change_to_stopping()

    def request_run(self):
        self.__jms.state.change_to_querying()
        self.__jms.check_rerun()

    def request_cancel(self):
        self.__jms.state.change_to_querying()
        self.__jms.check_cancel()

    def receive_error_event(self):
        self.__jms.state.change_to_error()


class QueryingJMSState(object):

    def __init__(self, jms):
        self.__jms = jms

    def receive_pend_event(self):
        self.__jms.state.change_to_pending()

    def receive_stop_event(self):
        self.__jms.state.change_to_stopping()

    def receive_cancel_event(self):
        self.__jms.state.change_to_entry()

    def receive_run_event(self):
        self.__jms.state.change_to_running()

    def receive_error_event(self):
        self.__jms.state.change_to_error()


class DoneJMSState(object):

    def __init__(self, jms):
        self.__jms = jms

    def entry(self):
        self.__jms.job.state.change_to_done()


class ErrorJMSState(object):

    def __init__(self, jms):
        self.__jms = jms

    def entry(self):
        self.__jms.job.state.change_to_error()


class FailedJMSState(object):

    def __init__(self, jms):
        self.__jms = jms

    def entry(self):
        self.__jms.job.state.change_to_failed()

