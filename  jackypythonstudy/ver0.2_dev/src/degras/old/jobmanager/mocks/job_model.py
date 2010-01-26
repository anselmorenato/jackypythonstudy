#! /opt/python2.6/bin/python
#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura
# Last Change: .

# standard modules
import os, sys

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from utils.event import NagaraEvent

from interfaces.ijob_model import IJobModel
class JobModel(IJobModel):
    def __init__(self):

        # define properties
        self.__expected_time = 100
        self.__finish_time = 100
        self.__id = 1
        self.__jms = 'jms'
        self.__location = 'local'
        self.__name = 'task name'
        self.__project = 'project'
        self.__start_time = 1
        self.__is_selected = True

        # generate events
        self.__delete_event = NagaraEvent()
        self.__init_event = NagaraEvent()
        self.__state_changed_event = NagaraEvent()
        self.__update_event = NagaraEvent()

    # properties
    @property
    def expected_time(self):
        return self.__expected_time

    @property
    def finish_time(self):
        return self.__finish_time

    @property
    def id(self):
        return self.__id

    @property
    def jms(self):
        return self.__jms

    @property
    def location(self):
        return self.__location

    @property
    def name(self):
        return self.__name

    @property
    def project(self):
        return self.__project

    @property
    def start_time(self):
        return self.__start_time

    # events
    @property
    def delete_event(self):
        return self.__delete_event

    @property
    def init_event(self):
        return self.__init_event

    @property
    def state_changed_event(self):
        return self.__state_changed_event

    @property
    def update_event(self):
        return self.__update_event

    # enables
    def enable_is_selected(self):
        self._is_selected = True
    def disable_is_selected(self):
        self._is_selected = False
    def is_is_selected_enabled(self):
        return self._is_selected

    # methods
    def get_available_request_dict(self):
        pass

    def get_state(self):
        pass

    def request_submit(self):
        pass

    def request_convert(self):
        pass

    def request_send(self):
        pass

    def request_run(self):
        pass

    def request_stop(self):
        pass

    def request_rerun(self):
        pass

    def request_cancel(self):
        pass

    def request_delete(self):
        pass

    def request_receive(self):
        pass

    def request_sync(self):
        pass

    def set_auto(self):
        pass

