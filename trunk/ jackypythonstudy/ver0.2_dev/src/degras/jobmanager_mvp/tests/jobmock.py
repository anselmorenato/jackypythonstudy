#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura

# standard modules
import os, sys

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from utils.event import NagaraEvent
from core.exception import NagaraException
from utils.deco import threaded
        
class JobMock(object):

    def __init__(self, id):

        # events
        self.__update_event = NagaraEvent()
        self.__state_event  = NagaraEvent()

        # property
        self.__state         = 'Running'
        self.__expected_time = '3:00'
        self.__start_time    = '15:30'
        self.__finish_time   = '18:30'
        self.__elasped_time  = '1:30'
        self.__id            = id
        self.__location      = 'hpcs'
        self.__project       = 'Project X'
        self.__name          = 'job name'
        self.__jms           = 'LSF'

        self.__use_auto      = False

        # requests
        self.__request_list = [
            'request_submit'  , 
            'request_convert' , 
            'request_send'    , 
            'request_run'     , 
            'request_stop'    , 
            'request_cancel'  , 
            'request_rerun'   , 
            'request_receive' , 
            'request_sync'    , 
            'request_delete'  , 
        ]

        self.__available_request_list = [
            'request_submit'  , 
            'request_convert' , 
            'request_delete'  , 
        ]

    # events
    @property
    def update_event(self):
        return self.__update_event

    @property
    def state_changed_event(self):
        return self.__state_event

    # property: state
    def get_state(self):
        return self.__state
    def set_state(self, state):
        self.__state = state
        self.state_event.fire()
    state = property(get_state, set_state)
    
    # property: expected_time
    def get_expected_time(self):
        return self.__expected_time
    def set_expected_time(self, expected_time):
        self.__expected_time = expected_time
        self.update_event.fire('expected_time')
    expected_time = property(get_expected_time, set_expected_time)

    # property: start
    def get_start_time(self):
        return self.__start_time
    def set_start_time(self, start_time):
        self.__start_time = start_time
        self.update_event.fire('start_time')
    start_time = property(get_start_time, set_start_time)

    # property: finish_time
    def get_finish_time(self):
        return self.__finish_time
    def set_finish_time(self, finish_time):
        self.__finish_time = finish_time
        self.update_event.fire('finish_time')
    finish_time = property(get_finish_time, set_finish_time)

    # property: elasped_time
    def get_elasped_time(self):
        return self.__elasped_time
    def set_elasped_time(self, elasped_time):
        self.__elasped_time = elasped_time
        self.update_event.fire('elasped_time')
    elasped_time = property(get_elasped_time, set_elasped_time)
    
    # property: id
    @property
    def id(self):
        return self.__id
    
    # property: jms
    def get_jms(self):
        return self.__jms
    def set_jms(self, jms):
        self.__jms = jms
        self.update_event.fire('jms')
    jms = property(get_jms, set_jms)
    
    # property: location
    def get_location(self):
        return self.__location
    def set_location(self, location):
        self.__location = location
        self.update_event.fire('location')
    location = property(get_location, set_location)
    
    # property: name
    def get_name(self):
        return self.__name
    def set_name(self, name):
        self.__name = name
        self.update_event.fire('name')
    name = property(get_name, set_name)
    
    # property: project
    @property
    def project(self):
        return self.__project

    def is_auto(self):
        return True if self.__use_auto else False

    def enable_auto(self, enable):
        self.__use_auto = enable

    def get_available_request(self):
        return self.__available_request_list

    def get_all_request(self):
        return self.__request_list

    # below methods is for mock
    def switch_state(self):
        self.__available_request_list = [
            'request_stop'  , 
            'request_cancel' , 
            'request_delete'  , 
        ]
        self.state = 'Stopping'

    def __getattr__(self, reqname):
        if not reqname.startswith('request_'):
            raise AttributeError()

        def request_any():
            pass

        return request_any
