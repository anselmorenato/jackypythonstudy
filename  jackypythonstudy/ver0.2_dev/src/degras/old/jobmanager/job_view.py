#! /opt/python2.6/bin/python
#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura

# standard modules
import os, sys
import wx

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from utils.event import NagaraEvent
from core.exception import NagaraException
import degras.image as im

class NotFoundRequestError(NagaraException): pass

from interfaces.ijob_view import IJobView
class JobView(IJobView):

    __request_list = [
        'submit', 'convert', 'send', 'run', 'stop',
        'cancel', 'rerun', 'receive', 'sync',
    ]

    def __init__(self):

        self.__menu = wx.Menu()

        # define properties
        self.__elasped_time  = 900
        self.__expected_time = 100
        self.__finish_time   = 100
        self.__id            = 1
        self.__jms           = 'jms'
        self.__location      = 'hpcs'
        self.__name          = 'task name'
        self.__project       = 'project'
        self.__start_time    = 1
        self.__is_selected   = True

        # generate events
        self.__cancel_event   = NagaraEvent()
        self.__convert_event  = NagaraEvent()
        self.__delete_event   = NagaraEvent()
        self.__receive_event  = NagaraEvent()
        self.__rerun_event    = NagaraEvent()
        self.__run_event      = NagaraEvent()
        self.__send_event     = NagaraEvent()
        self.__set_auto_event = NagaraEvent()
        self.__stop_event     = NagaraEvent()
        self.__submit_event   = NagaraEvent()
        self.__sync_event     = NagaraEvent()

    # events
    @property
    def cancel_event(self):
        return self.__cancel_event

    @property
    def convert_event(self):
        return self.__convert_event

    @property
    def delete_event(self):
        return self.__delete_event

    @property
    def receive_event(self):
        return self.__receive_event

    @property
    def rerun_event(self):
        return self.__rerun_event

    @property
    def run_event(self):
        return self.__run_event

    @property
    def send_event(self):
        return self.__send_event

    @property
    def set_auto_event(self):
        return self.__set_auto_event

    @property
    def stop_event(self):
        return self.__stop_event

    @property
    def submit_event(self):
        return self.__submit_event

    @property
    def sync_event(self):
        return self.__sync_event

    # properties with setter
    def get_elasped_time(self):
        return self.__elasped_time
    def set_elasped_time(self, elasped_time):
        self.__elasped_time = elasped_time
    elasped_time = property(get_elasped_time, set_elasped_time)

    def get_expected_time(self):
        return self.__expected_time
    def set_expected_time(self, expected_time):
        self.__expected_time = expected_time
    expected_time = property(get_expected_time, set_expected_time)

    def get_finish_time(self):
        return self.__finish_time
    def set_finish_time(self, finish_time):
        self.__finish_time = finish_time
    finish_time = property(get_finish_time, set_finish_time)

    def get_id(self):
        return self.__id
    def set_id(self, id):
        self.__id = id
    id = property(get_id, set_id)

    def get_jms(self):
        return self.__jms
    def set_jms(self, jms):
        self.__jms = jms
    jms = property(get_jms, set_jms)

    def get_location(self):
        return self.__location
    def set_location(self, location):
        self.__location = location
    location = property(get_location, set_location)

    def get_name(self):
        return self.__name
    def set_name(self, name):
        self.__name = name
    name = property(get_name, set_name)

    def get_project(self):
        return self.__project
    def set_project(self, project):
        self.__project = project
    project = property(get_project, set_project)

    def get_start_time(self):
        return self.__start_time
    def set_start_time(self, start_time):
        self.__start_time = start_time
    start_time = property(get_start_time, set_start_time)

    # enables
    def enable_selected(self, enable=True):
        self.__selected = enable
    def is_selected(self):
        return self.__is_selected

    # methods
    def set_request_dict(self, request_dict):
        if self.__menu.GetMenuItemCount() == 0:
            self.__id_table = {}
            for i, req in enumerate(self.__request_list):
                id = wx.NewId()
                self.__menu.Append(id, req, req)
                self.__menu.Bind(wx.EVT_MENU, self.on_select, id=id)

        for item in self.__menu.GetMenuItems():
            id = item.GetId()
            menuname = item.GetLabel()
            reqname = 'request_'+menuname
            enable = request_dict[reqname]
            self.__menu.Enable(id, enable)

    def set_state(self, state):
        self.__state = state
        self.__image = im.get_jobstate_image(state)

    def get_state(self):
        return self.__state, self.__image

    def get_menu(self):
        return self.__menu

    def on_select(self, event):
        id = event.GetId()
        menuitem = self.__menu.FindItemById(id)
        menuname = menuitem.GetLabel()
        req_event = menuname + '_event'
        if hasattr(self, req_event):
            getattr(self, req_event).fire()
        else:
            raise NotFoundRequestError(menuname)

    def on_delete(self, event):
        pass

    def on_enable_auto(self, event):
        pass

