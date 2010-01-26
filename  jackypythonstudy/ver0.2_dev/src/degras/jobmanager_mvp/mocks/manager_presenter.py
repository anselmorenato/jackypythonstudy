#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura

# standard modules
import os, sys

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from  utils.event import  EventBindManager
from  core.log    import  Log

class ManagerPresenter(object):

    
    binder = EventBindManager()    
    def __init__(self, model, view):
        self.model = model
        self.view = view
    
        self.binder.bind_all(self)

    @binder("model.created_event")
    def created_on_model(self, msg):
        self.__log_receive('created_on_model')

    @binder("model.delete_event")
    def delete_on_model(self, msg):
        self.__log_receive('delete_on_model')

    @binder("view.submit_event")
    def submit_on_view(self, msg):
        self.__log_receive('submit_on_view')

    @binder("view.convert_event")
    def convert_on_view(self, msg):
        self.__log_receive('convert_on_view')

    @binder("view.send_event")
    def send_on_view(self, msg):
        self.__log_receive('send_on_view')

    @binder("view.run_event")
    def run_on_view(self, msg):
        self.__log_receive('run_on_view')

    @binder("view.stop_event")
    def stop_on_view(self, msg):
        self.__log_receive('stop_on_view')

    @binder("view.rerun_event")
    def rerun_on_view(self, msg):
        self.__log_receive('rerun_on_view')

    @binder("view.cancel_event")
    def cancel_on_view(self, msg):
        self.__log_receive('cancel_on_view')

    @binder("view.receive_event")
    def receive_on_view(self, msg):
        self.__log_receive('receive_on_view')

    @binder("view.sync_event")
    def sync_on_view(self, msg):
        self.__log_receive('sync_on_view')

    @binder("view.rename_event")
    def rename_on_view(self, msg):
        self.__log_receive('rename_on_view')

    @binder("view.select_event")
    def select_on_view(self, msg):
        self.__log_receive('select_on_view')

    @binder("view.set_auto_event")
    def set_auto_on_view(self, msg):
        self.__log_receive('set_auto_on_view')

    @binder("view.delete_event")
    def delete_on_view(self, msg):
        self.__log_receive('delete_on_view')

    def __log_receive(self, listener_name):
        info_list = self.binder.get_info(listener_name)
        for info in info_list:
            obj = info['object_name']
            evt = info['event_name']
            cls = info['class_name']
            mes = 'Recieved {0} of {1}:{2} at {3}'
            Log( mes.format(evt, obj, cls, listener_name) )

