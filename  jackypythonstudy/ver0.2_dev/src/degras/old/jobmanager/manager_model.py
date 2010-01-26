#! /opt/python2.6/bin/python
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


class JobNotFoundError(NagaraException): pass

from interfaces.imanager_model import IManagerModel
class ManagerModel(IManagerModel):
    def __init__(self):

        # define properties
        self.__job_dict = {}

        # generate events
        self.__created_event = NagaraEvent()
        self.__delete_event  = NagaraEvent()
        self.__init_event    = NagaraEvent()
        self.__update_event  = NagaraEvent()

        self.__interval = 0
        self.__update_per_time()

    # events
    @property
    def created_event(self):
        return self.__created_event

    @property
    def delete_event(self):
        return self.__delete_event

    @property
    def init_event(self):
        return self.__init_event

    @property
    def update_event(self):
        return self.__update_event

    # methods
    def init(self):
        self.init_event.fire()

    def get_newjob(self):
        self.__check_job()
        new_id = max(self.__job_dict.keys())
        return self.__job_dict[new_id]

    def get_job_dict(self):
        return self.__job_dict

    def set_selected_jobid_list(self, jobid_list):
        self.__check_job()
        # for self
        job_dict = self.get_job_dict()
        jobid_set = set(job_dict.keys())
        # for argument
        jobid_argset = set(jobid_list)
        if not jobid_argset <= jobid_set:
            raise JobNotFoundError()
        self.__selected_jobid_list = jobid_list

    def append_job(self, job):
        from job_view      import JobView
        from job_model     import JobModel
        from job_presenter import JobPresenter
        id = job.id
        jobmodel  = JobModel(job)
        jobview   = JobView()
        jobpresen = JobPresenter(jobmodel, jobview)
        jobmodel.init()
        self.__job_dict[id] = (jobmodel, jobview, jobpresen)
        self.created_event.fire()

    def delete_job(self, jobid):
        self.__check_job()
        job = self.__job_dict.get(jobid)
        if not job:
            raise JobNotFoundError()
        del self.__job_dict[jobid]
        self.update_event.fire()

    @threaded
    def __update_per_time(self):
        import time
        while True:
            if self.__interval==0: break
            self.update_event.fire()
            time.sleep(interval)

    def __check_job(self):
        if not self.__job_dict:
            raise JobNotFoundError()

    def set_interval(self, interval):
        self.__interval = 0
        self.__interval = interval
        self.__update_per_time()

if __name__ == '__main__':
    mmodel = ManagerModel()
    #mport time
    #ime.sleep(3.5)
    #model.set_interval(1)
    #model.set_interval(0)
    ##time.sleep(3.5)
    #mmodel.enable_auto(False)
