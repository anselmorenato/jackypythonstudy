#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura

# standard modules
import os, sys

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from  utils.event import  EventBindManager
from  core.log    import  Log

class LocationPresenter(object):


    binder = EventBindManager()    

    def __init__(self, model, view):
        self.model = model
        self.view = view
    
        self.binder.bind_all(self)

    @binder("model.init_event")
    def init(self, msg):
        self.__log_receive('init')
        prop_list = [
            'name', 'workdir', 'shell', 'init_file', 'environ_dict', 'mpi',
            'ssh_address', 'ssh_username', 'ssh_password', 'ssh_port',
            'command_dict', 'jms_dict', 'jms_default',
        ]

        for prop in prop_list:
            get_prop = 'get_' + prop
            set_prop = 'set_' + prop
            val = getattr(self.model, prop)
            getattr(self.view, set_prop)( val )
        
        self.view.show()

    @binder("model.update_event")
    def update_in_view(self, msg):
        self.__log_receive('update_in_view')
        prop = msg
        get_prop = 'get_' + prop
        set_prop = 'set_' + prop
        val = getattr(self.model, prop)
        getattr(self.view, set_prop)( val )

    @binder("view.close_event", 'view.ok_event')
    def close_shower(self, msg):
        self.__log_receive('close_shower')

        prop_list = [
           'name', 'workdir', 'shell', 'init_file', 'environ_dict', 'mpi',
           'ssh_address', 'ssh_username', 'ssh_password', 'ssh_port',
           'command_dict', 'jms_dict', 'jms_default',
        ]

        for prop in prop_list:
           get_prop = 'get_' + prop
           set_prop = 'set_' + prop
           val = getattr(self.view, prop)
           getattr(self.model, set_prop)( val )

        self.view.close()

    @binder("view.cancel_event")
    def ok_on_view(self, msg):
       self.__log_receive('ok_on_view')

    @binder("view.update_event")
    def update_model(self, msg):
        self.__log_receive('update_model')
        prop = msg
        get_prop = 'get_' + prop
        set_prop = 'set_' + prop
        val = getattr(self.view, prop)
        getattr(self.model, set_prop)( val )

    def __log_receive(self, listener_name):
        info_list = self.binder.get_info(listener_name)
        for info in info_list:
            obj = info['object_name']
            evt = info['event_name']
            cls = info['class_name']
            mes = 'Recieved {0} of {1}:{2} at {3}'
            Log( mes.format(evt, obj, cls, listener_name) )

