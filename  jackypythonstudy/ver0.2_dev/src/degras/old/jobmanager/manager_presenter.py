#! /opt/python2.6/bin/python
#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura
#
# $Date$
# $Rev$
# $Author$
# Last Change: 2010/01/13 16:48.
#

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

    @binder("model.init_event")
    def init(self, msg):
        self.__log_receive('init')
        self.update_view(None)

    @binder("model.created_event")
    def append_job(self, msg):
        self.__log_receive('append_job')
        job = self.model.get_newjob()
        self.view.append( job )

    @binder("model.delete_event")
    def delete_job(self, msg):
        self.__log_receive('delete_job')
        self.update_view()

    @binder("model.update_event")
    def update_view(self, msg):
        self.__log_receive('update_view')
        jobmodel_list = [ m for m, v, p in self.model.get_job_dict() ]
        self.view.update_all( jobmodel_list )

    @binder("view.operate_event")
    def popup_on_job(self, msg):
        self.__log_receive('operate_event')
        jobid = msg # recieve job_id
        m, v, p = self.model.get_job_dict()[ jobid ]
        self.view.popup_jobmenu( v.get_menu() )

    @binder("view.submit_event")
    def submit_for_selected_job(self, msg):
        self.__log_receive('submit_for_selected_job')
        jobid_list = self.view.get_selected_jobid_list()
        for jobid in jobid_list:
            m, v, p = self.model.get_job_dict()[ jobid ]
            v.on_submit()

    @binder("view.convert_event")
    def convert_for_selected_job(self, msg):
        self.__log_receive('convert_for_selected_job')
        jobid_list = self.view.get_selected_jobid_list()
        for jobid in jobid_list:
            m, v, p = self.model.get_job_dict()[ jobid ]
            v.on_convert()

    @binder("view.send_event")
    def send_for_selected_job(self, msg):
        self.__log_receive('send_for_selected_job')
        jobid_list = self.view.get_selected_jobid_list()
        for jobid in jobid_list:
            m, v, p = self.model.get_job_dict()[ jobid ]
            v.on_send()

    @binder("view.run_event")
    def run_for_selected_job(self, msg):
        self.__log_receive('run_for_selected_job')
        jobid_list = self.view.get_selected_jobid_list()
        for jobid in jobid_list:
            m, v, p = self.model.get_job_dict()[ jobid ]
            v.on_run()

    @binder("view.stop_event")
    def stop_for_selected_job(self, msg):
        self.__log_receive('stop_for_selected_job')
        jobid_list = self.view.get_selected_jobid_list()
        for jobid in jobid_list:
            m, v, p = self.model.get_job_dict()[ jobid ]
            v.on_stop()

    @binder("view.rerun_event")
    def rerun_for_selected_job(self, msg):
        self.__log_receive('rerun_for_selected_job')
        jobid_list = self.view.get_selected_jobid_list()
        for jobid in jobid_list:
            m, v, p = self.model.get_job_dict()[ jobid ]
            v.on_rerun()

    @binder("view.cancel_event")
    def cancel_for_selected_job(self, msg):
        self.__log_receive('cancel_for_selected_job')
        jobid_list = self.view.get_selected_jobid_list()
        for jobid in jobid_list:
            m, v, p = self.model.get_job_dict()[ jobid ]
            v.on_cancel()

    @binder("view.receive_event")
    def receive_for_selected_job(self, msg):
        self.__log_receive('receive_for_selected_job')
        jobid_list = self.view.get_selected_jobid_list()
        for jobid in jobid_list:
            m, v, p = self.model.get_job_dict()[ jobid ]
            v.on_receive()

    @binder("view.sync_event")
    def sync_for_selected_job(self, msg):
        self.__log_receive('sync_for_selected_job')
        jobid_list = self.view.get_selected_jobid_list()
        for jobid in jobid_list:
            m, v, p = self.model.get_job_dict()[ jobid ]
            v.on_sync()

    @binder("view.rename_event")
    def rename_job(self, msg):
        self.__log_receive('rename_job')
        jobid = msg
        m, v, p = self.model.get_job_dict()[ jobid ]
        jobname = self.view.get_jobname( jobid )
        m.name = jobname

    @binder("view.select_event")
    def select_on_view(self, msg):
        self.__log_receive('select_on_view')
        job_list = self.view.get_selected_jobid_list()
        self.model.set_selected_jobid_list( job_list )

    @binder("view.set_auto_event")
    def enale_auto(self, msg):
        self.__log_receive('enale_auto')
        jobid, enable = msg
        m, v, p = self.model.get_job_dict()[ jobid ]
        m.enable_auto( enable )

    @binder("view.delete_event")
    def delete_job(self, msg):
        self.__log_receive('delete_job')
        jobid_list = self.view.get_selected_jobid_list()
        for jobid in jobid_list:
            self.model.delete_job( jobid )

    @binder("view.update_event")
    def update_from_view(self, msg):
        self.__log_receive('update_from_view')
        self.model.update_event.fire()

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
    frame = wx.Frame(None, -1, 'Job ListCtrl')

    from manager_model import ManagerModel
    from manager_view  import ManagerView
    model  = ManagerModel()
    view   = ManagerView(frame)
    presen = ManagerPresenter(model, view)

    # create Job
    from tests.jobmock import JobMock
    job = JobMock(1)
    ## set properties
    #init_prop_dict = dict(
        #id            = 5           , 
        #expected_time = '3:00'      , 
        #start_time    = '15:00'     , 
        #elasped_time  = '1:00'      , 
        #finish_time   = ''          , 
        #location      = 'hpcs'      , 
        #jms           = 'LSF'       , 
        #name          = 'test job'  , 
        #project       = 'project X' , 
    #)

    #for prop, val in init_prop_dict.items():
        #set_prop = 'set_'+prop
        #get_prop = 'get_'+prop
        #getattr(jobview, set_prop)( val )

    ## set state
    #jobview.set_state( 'Runnable' )

    ## set popup menu
    #init_request_dict = dict(
        #request_submit  = False , 
        #request_convert = False , 
        #request_send    = False , 
        #request_run     = True  , 
        #request_stop    = True  , 
        #request_cancel  = True  , 
        #request_rerun   = False , 
        #request_receive = False , 
        #request_sync    = False , 
    #)
    #jobview.set_request_dict( init_request_dict )

    model.append_job(job)
    #print model.get_job_dict()
    #managermodel.append(job)
    #managermodel.append(job)
    #managermodel.append(job)
    #managermodel.append(job)
    #managermodel.append(job)

    frame.Show()


    import time
    def append_job(interval, job):
        time.sleep(interval)
        model.append_job(job)
        time.sleep(interval)
        model.append_job(job)

    import threading
    t = threading.Thread(name=None, target=append_job, args=[3, job])
    t.start()

    app.MainLoop()

    #view.update_all( [jobview] )
