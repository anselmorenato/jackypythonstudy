#! /opt/python2.6/bin/python
#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura
#
# $Date$
# $Rev$
# $Author$
#
# standard modules
import os, sys

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from  utils.event import  EventBindManager
from  core.log    import  Log


class JobPresenter(object):
    
    binder = EventBindManager()    

    def __init__(self, model, view):
        self.model = model
        self.view = view
    
        self.binder.bind_all(self)

    @binder("model.init_event")
    def init(self, msg):
        self.__log_receive('init')
        self.change_state(msg=None)

    @binder("model.state_changed_event")
    def change_state(self, msg):
        self.__log_receive('change_state')
        # set state
        self.view.set_state( self.model.get_state() )
        # set request
        req_dict = self.model.get_available_request_dict()
        self.view.set_request_dict( req_dict )

    @binder("model.update_event")
    def update_view(self, msg):
        self.__log_receive('update_view')
        prop = msg
        set_prop = 'set_' + msg
        get_prop = 'get_' + msg
        ret_val = getattr(self.model, prop)
        getattr(self.view, set_prop)( ret_val )

    @binder("model.delete_event")
    def delete_in_model(self, msg):
        """Delete request will be performed in JobManager."""
        self.__log_receive('request_delete')

    @binder("view.submit_event")
    def request_submit(self, msg):
        self.__log_receive('request_submit')
        self.model.request_submit()

    @binder("view.convert_event")
    def request_convert(self, msg):
        self.__log_receive('request_convert')
        self.model.request_convert()

    @binder("view.send_event")
    def request_send(self, msg):
        self.__log_receive('request_send')
        self.model.request_send()

    @binder("view.run_event")
    def request_run(self, msg):
        self.__log_receive('request_run')
        self.model.request_run()

    @binder("view.stop_event")
    def request_stop(self, msg):
        self.__log_receive('request_stop')
        self.model.request_stop()

    @binder("view.rerun_event")
    def request_rerun(self, msg):
        self.__log_receive('request_rerun')
        self.model.request_rerun()

    @binder("view.cancel_event")
    def request_cancel(self, msg):
        sllf.__log_receive('request_cancel')
        self.model.request_cancel()

    @binder("view.set_auto_event")
    def request_set_auto(self, msg):
        self.__log_receive('request_set_auto')
        self.model.set_auto()

    @binder("view.delete_event")
    def request_delete(self, msg):
        self.__log_receive('request_delete')
        self.model.request_delete()

    @binder("view.receive_event")
    def request_receive(self, msg):
        self.__log_receive('request_receive')
        self.model.request_receive()

    @binder("view.sync_event")
    def request_sync(self, msg):
        self.__log_receive('request_sync')
        self.model.request_sync()

    def __log_receive(self, listener_name):
        info_list = self.binder.get_info(listener_name)
        for info in info_list:
            obj = info['object_name']
            evt = info['event_name']
            cls = info['class_name']
            mes = 'Recieved {0} of {1}:{2} at {3}'
            Log( mes.format(evt, obj, cls, listener_name) )

