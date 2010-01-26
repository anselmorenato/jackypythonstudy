#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura
#
# $Date: 2010-01-20 14:50:42 +0900 (水, 20 1 2010) $
# $Rev: 60 $
# $Author: ishikura $
#
import os, sys

from manager_view      import ManagerView
from manager_presenter import ManagerPresenter

class JobManager(object):

    def __init__(self, parent, model):

        # setup view
        try:
            parent_view = parent.get_view()
        except AttributeError:
            parent_view = parent
        self.__view = ManagerView( parent_view )

        self.__model = model
        self.__presen = ManagerPresenter( self.__model, self.__view )
        # from manager_view import ManagerInteractor
        # inter = ManagerInteractor( self.__view, self__presen )

    def get_view(self):
        return self.__view

    def append_job(self, job):
        return self.__model.append_job(job)

if __name__ == '__main__':

    import wx
    app = wx.App(redirect=False)
    frame = wx.Frame(None, -1, 'Job ListCtrl')

    from manager_model     import ManagerModel
    model = ManagerModel()

    jm = JobManager(frame, model)

    # create Job
    from tests.jobmock import JobMock
    job = JobMock(1)
    
    jm.append_job(job)
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
        jm.append_job(job)
        time.sleep(interval)
        jm.append_job(job)

    import threading
    import multiprocessing 
    
    t = threading.Thread(name=None, target=append_job, args=[3, job])
    # t = multiprocessing.Process(name=None, target=append_job, args=[3, job])
    t.start()
    # t.join()

    app.MainLoop()

