#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura

# standard modules
import os, sys
from abc import ABCMeta, abstractmethod, abstractproperty

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from utils.event import NagaraEvent


class IJobView():
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
    def rerun_event(self): pass

    @abstractproperty
    def run_event(self): pass

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

    # properties with setter
    @abstractmethod
    def get_elasped_time(self): pass
    @abstractmethod
    def set_elasped_time(self, elasped_time): pass
    elasped_time = abstractproperty(get_elasped_time, set_elasped_time)

    @abstractmethod
    def get_expected_time(self): pass
    @abstractmethod
    def set_expected_time(self, expected_time): pass
    expected_time = abstractproperty(get_expected_time, set_expected_time)

    @abstractmethod
    def get_finish_time(self): pass
    @abstractmethod
    def set_finish_time(self, finish_time): pass
    finish_time = abstractproperty(get_finish_time, set_finish_time)

    @abstractmethod
    def get_id(self): pass
    @abstractmethod
    def set_id(self, id): pass
    id = abstractproperty(get_id, set_id)

    @abstractmethod
    def get_jms(self): pass
    @abstractmethod
    def set_jms(self, jms): pass
    jms = abstractproperty(get_jms, set_jms)

    @abstractmethod
    def get_location(self): pass
    @abstractmethod
    def set_location(self, location): pass
    location = abstractproperty(get_location, set_location)

    @abstractmethod
    def get_name(self): pass
    @abstractmethod
    def set_name(self, name): pass
    name = abstractproperty(get_name, set_name)

    @abstractmethod
    def get_project(self): pass
    @abstractmethod
    def set_project(self, project): pass
    project = abstractproperty(get_project, set_project)

    @abstractmethod
    def get_start_time(self): pass
    @abstractmethod
    def set_start_time(self, start_time): pass
    start_time = abstractproperty(get_start_time, set_start_time)

    # enables
    @abstractmethod
    def is_selected(self): pass
    @abstractmethod
    def enable_selected(self, enable=True): pass

    # methods
    @abstractmethod
    def get_state(self): pass

    @abstractmethod
    def on_popup(self): pass

    @abstractmethod
    def set_request_dict(self): pass

    @abstractmethod
    def set_state(self): pass

