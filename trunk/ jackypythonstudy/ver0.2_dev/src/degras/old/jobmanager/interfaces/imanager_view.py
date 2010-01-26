#! /opt/python2.6/bin/python
#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura
# Last Change: .

# standard modules
import os, sys
from abc import ABCMeta, abstractmethod, abstractproperty

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from utils.event import NagaraEvent


class IManagerView():
    __metaclass__ =  ABCMeta

    # events
    @abstractproperty
    def cancel_event(self): pass

    @abstractproperty
    def convert_event(self): pass

    @abstractproperty
    def delete_event(self): pass

    @abstractproperty
    def receive_event(self): pass

    @abstractproperty
    def rename_event(self): pass

    @abstractproperty
    def operate_event(self): pass

    @abstractproperty
    def rerun_event(self): pass

    @abstractproperty
    def run_event(self): pass

    @abstractproperty
    def select_event(self): pass

    @abstractproperty
    def send_event(self): pass

    @abstractproperty
    def set_auto_event(self): pass

    @abstractproperty
    def stop_event(self): pass

    @abstractproperty
    def submit_event(self): pass

    @abstractproperty
    def sync_event(self): pass

    @abstractproperty
    def update_event(self): pass

    # enables
    @abstractmethod
    def is_auto(self): pass
    @abstractmethod
    def enable_auto(self, enable=True): pass

    # methods
    @abstractmethod
    def append(self): pass

    @abstractmethod
    def get_jobname(self): pass

    @abstractmethod
    def get_selected_jobid_list(self): pass

    @abstractmethod
    def on_popup_jobmenu(self): pass

    @abstractmethod
    def update_all(self): pass

