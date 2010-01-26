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


class JobInteractor(object):

    def __init__(self, view, presenter):
        menu = view.get_menu()
        menu.Bind( wx.EVT_MENU , self.on_submit  , id=view.ID_SUBMIT  ) 
        menu.Bind( wx.EVT_MENU , self.on_convert , id=view.ID_CONVERT ) 
        menu.Bind( wx.EVT_MENU , self.on_send    , id=view.ID_SEND    ) 
        menu.Bind( wx.EVT_MENU , self.on_run     , id=view.ID_RUN     ) 
        menu.Bind( wx.EVT_MENU , self.on_stop    , id=view.ID_STOP    ) 
        menu.Bind( wx.EVT_MENU , self.on_cancel  , id=view.ID_CANCEL  ) 
        menu.Bind( wx.EVT_MENU , self.on_rerun   , id=view.ID_RERUN   ) 
        menu.Bind( wx.EVT_MENU , self.on_receive , id=view.ID_RECEIVE ) 
        menu.Bind( wx.EVT_MENU , self.on_sync    , id=view.ID_SYNC    ) 

    def on_submit(self, event):
        self.presenter.request_submit()

    def on_convert(self, event):
        self.presenter.request_convert()
    
    def on_send(self, event):
        self.presenter.request_send()

    def on_run(self, event):
        self.presenter.request_run()

    def on_stop(self, event):
        self.presenter.request_stop()

    def on_cancel(self, event):
        self.presenter.request_cancel()

    def on_rerun(self, event):
        self.presenter.request_rerun()

    def on_receive(self, event):
        self.presenter.request_receive()

    def on_sync(self, event):
        self.presenter.request_sync()


class NotFoundRequestError(NagaraException): pass

class JobView(object):


    def __init__(self):

        self.init_request_menu()

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

    def init_request_menu(self):
        self.__menu     = wx.Menu()
        self.ID_SUBMIT  = wx.NewId()
        self.ID_CONVERT = wx.NewId()
        self.ID_SEND    = wx.NewId()
        self.ID_RUN     = wx.NewId()
        self.ID_STOP    = wx.NewId()
        self.ID_CANCEL  = wx.NewId()
        self.ID_RERUN   = wx.NewId()
        self.ID_RECEIVE = wx.NewId()
        self.ID_SYNC    = wx.NewId()

        self.__menu.Append( self.ID_SUBMIT  , 'submit'  , 'submit'  ) 
        self.__menu.Append( self.ID_CONVERT , 'convert' , 'convert' ) 
        self.__menu.Append( self.ID_SEND    , 'send'    , 'send'    ) 
        self.__menu.Append( self.ID_RUN     , 'run'     , 'run'     ) 
        self.__menu.Append( self.ID_STOP    , 'stop'    , 'stop'    ) 
        self.__menu.Append( self.ID_CANCEL  , 'cancel'  , 'cancel'  ) 
        self.__menu.Append( self.ID_RERUN   , 'rerun'   , 'rerun'   ) 
        self.__menu.Append( self.ID_RECEIVE , 'receive' , 'receive' ) 
        self.__menu.Append( self.ID_SYNC    , 'sync'    , 'sync'    ) 

    def enable_menuitem(self, id, enable):
        self.__menu.Enable(id, enable)

    def is_enabled_menuitem(self, id):
        return self.__menu.IsEnabled(id)

    def set_state(self, state):
        self.__state = state
        self.__image = im.get_jobstate_image(state)

    def get_state(self):
        return self.__state, self.__image

    def get_menu(self):
        return self.__menu


if __name__ == '__main__':
    app = wx.App()
    j = JobView()
    menu = j.get_menu()
    


