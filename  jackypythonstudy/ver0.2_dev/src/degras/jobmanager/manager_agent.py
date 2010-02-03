#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura
#
# $Date: 2010-02-02 21:51:23 +0900 (火, 02 2 2010) $
# $Rev: 76 $
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
    job1 = JobMock(1)
    job2 = JobMock(2)
    job3 = JobMock(3)

    job1.name = 'Task 1'
    job1.state = 'Running'
    job1.expected_time = '3:00'
    job1.start_time = '15:30'
    job1.finish_time = ''
    job1.elasped_time = '1:11'

    job2.name = 'Task 2'
    job2.state = 'Converting'
    job2.expected_time = ''
    job2.start_time = ''
    job2.finish_time = ''
    job2.elasped_time = ''

    job3.name = 'Task 3'
    job3.state = 'Preparing'
    job3.expected_time = ''
    job3.start_time = ''
    job3.finish_time = ''
    job3.elasped_time = ''

    
    jm.append_job(job1)
    jm.append_job(job2)
    jm.append_job(job3)
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
        jm.append_job(job2)
        time.sleep(interval)
        jm.append_job(job3)

    import threading
    import multiprocessing 
    
    # t = threading.Thread(name=None, target=append_job, args=[3, job])
    # t = multiprocessing.Process(name=None, target=append_job, args=[3, job])
    # t.start()
    # t.join()

    app.MainLoop()

