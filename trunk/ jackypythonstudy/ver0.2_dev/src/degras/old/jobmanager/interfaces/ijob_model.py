#! /opt/python2.6/bin/python
#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura
# Last Change: 2010/01/06 22:00.

# standard modules
import os, sys
from abc import ABCMeta, abstractmethod, abstractproperty

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from utils.event import NagaraEvent


class IJobModel():
    __metaclass__ =  ABCMeta

    # events
    @abstractproperty
    def delete_event(self): pass

    @abstractproperty
    def init_event(self): pass

    @abstractproperty
    def state_changed_event(self): pass

    @abstractproperty
    def update_event(self): pass

    # properties
    @abstractproperty
    def expected_time(self): pass

    @abstractproperty
    def finish_time(self): pass

    @abstractproperty
    def id(self): pass

    @abstractproperty
    def jms(self): pass

    @abstractproperty
    def location(self): pass

    @abstractproperty
    def name(self): pass

    @abstractproperty
    def project(self): pass

    @abstractproperty
    def start_time(self): pass

    @abstractproperty
    def elasped_time(self): pass

    # enables
    @abstractmethod
    def enable_selected(self): pass
    @abstractmethod
    def is_selected(self): pass

    # methods
    @abstractmethod
    def get_available_request_dict(self): pass

    @abstractmethod
    def get_state(self): pass

    @abstractmethod
    def request_cancel(self): pass

    @abstractmethod
    def request_convert(self): pass

    @abstractmethod
    def request_delete(self): pass

    @abstractmethod
    def request_receive(self): pass

    @abstractmethod
    def request_rerun(self): pass

    @abstractmethod
    def request_run(self): pass

    @abstractmethod
    def request_send(self): pass

    @abstractmethod
    def request_stop(self): pass

    @abstractmethod
    def request_submit(self): pass

    @abstractmethod
    def request_sync(self): pass

    @abstractmethod
    def enable_auto(self): pass

