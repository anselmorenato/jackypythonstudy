#  -*- encoding: utf-8 -*-
# Copyright (C)  2009 Takakazu Ishikura

# standard modules
import os, sys

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from  utils.event import  EventBindManager
from  core.log    import  Log

class MenubarPresenter(object):

    
    binder = EventBindManager()    
    def __init__(self, model, view):
        self.model = model
        self.view = view
    
        self.binder.bind_all(self)

    @binder("view.test_event")
    def test_on_view(self, msg):
        self._log_recieve('test_on_view')

    @binder("model.update_file_event")
    def update_file_on_model(self, msg):
        self._log_recieve('update_file_on_model')

    @binder("model.update_project_event")
    def update_project_on_model(self, msg):
        self._log_recieve('update_project_on_model')

    @binder("model.update_edit_event")
    def update_edit_on_model(self, msg):
        self._log_recieve('update_edit_on_model')

    @binder("model.update_view_event")
    def update_view_on_model(self, msg):
        self._log_recieve('update_view_on_model')

    @binder("model.update_workflow_event")
    def update_workflow_on_model(self, msg):
        self._log_recieve('update_workflow_on_model')

    @binder("model.update_tool_event")
    def update_tool_on_model(self, msg):
        self._log_recieve('update_tool_on_model')

    @binder("model.update_plugin_event")
    def update_plugin_on_model(self, msg):
        self._log_recieve('update_plugin_on_model')

    def _log_recieve(self, listener_name):
        info_list = self.binder.get_info(listener_name)
        for info in info_list:
            obj = info['object_name']
            evt = info['event_name']
            cls = info['class_name']
            mes = 'Recieved {0} of {1}:{2} at {3}'
            Log( mes.format(evt, obj, cls, listener_name) )

