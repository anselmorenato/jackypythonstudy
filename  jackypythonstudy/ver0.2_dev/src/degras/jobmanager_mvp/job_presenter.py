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

    def __init__(self, job, view):
        self.__model = job
        self.__view = view
    
        self.binder.bind_all(self)

    @binder("__model.state_changed_event")
    def change_state(self, msg):
        self.__log_receive('change_state')
        # set state
        self.__view.set_state( self.__model.state )
        # set request
        self.update_reqmenu()

    @binder("__model.update_event")
    def update_view(self, msg):
        self.__log_receive('update_view')
        prop = msg
        set_prop = 'set_' + msg
        get_prop = 'get_' + msg
        ret_val = getattr(self.__model, prop)
        getattr(self.__view, set_prop)( ret_val )

    # @binder("__job.delete_event")
    # def delete_in_model(self, msg):
        # """Delete request will be performed in JobManager."""
        # self.__log_receive('request_delete')

    # delegate request
    def __getattr__(self, reqname):
        if reqname.startswith('request_'):
            try:
                getattr(self.__model, reqname)
            except AttributeError:
                pass

    def update_reqmenu(self):
        request_dict = {}
        ava_req_list = self.__model.get_available_request()
        all_req_list = self.__model.get_all_request()
        for req in all_req_list:
            request_dict[req] = True if req in ava_req_list else False

        for req, enable in request_dict.items():
            reqname = req.split('_')[-1]
            reqid = 'ID_' + reqname.upper()
            if reqid=='ID_DELETE': continue
            self.__view.enable_menuitem(getattr(self.__view, reqid), enable)

    def enable_auto(self, enable):
        self.__model.enable_auto(enable)

    def delete(self):
        # self.model.request_delete()
        pass

    def __log_receive(self, listener_name):
        info_list = self.binder.get_info(listener_name)
        for info in info_list:
            obj = info['object_name']
            evt = info['event_name']
            cls = info['class_name']
            mes = 'Recieved {0} of {1}:{2} at {3}'
            Log( mes.format(evt, obj, cls, listener_name) )


if __name__ == '__main__':
    import wx
    app = wx.App(redirect=False)
    from job_view import JobView, JobInteractor
    from tests.jobmock import JobMock
    jobview = JobView()
    job = JobMock(10)
    print job.state_event

    p = JobPresenter(job, jobview)
    
