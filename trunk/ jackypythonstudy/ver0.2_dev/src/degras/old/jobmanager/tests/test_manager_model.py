#! /opt/python2.6/bin/python
#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura

# standard modules
import os, sys
from nose.tools import *

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from utils.test_helper import *
from utils.event import NagaraEvent, EventBindManager
from utils.pattern import Null

# append the path for the target module
set_bodypath(__file__)

# test modules
import wx
app = wx.App()
from manager_model import ManagerModel, JobNotFoundError
from job_model     import JobModel
from job_view      import JobView
from job_presenter import JobPresenter
from jobmock       import JobMock
class TestManagerModelWithNoJob:

    def setup(self):
        self.model = ManagerModel()

    def teardown(self):
        self.model = None

    def test_init(self):
        ec = EventCatcher(self.model.init_event)
        self.model.init()
        assert_catch_event(ec)

    def test_get_newjob(self):
        assert_catch_exc(JobNotFoundError, self.model.get_newjob)

    def test_get_job_dict(self):
        job_dict = self.model.get_job_dict()
        assert_equal(0, len(job_dict))

    def test_set_selected_jobid_list(self):
        assert_catch_exc(JobNotFoundError,
                         self.model.set_selected_jobid_list, [])
        assert_catch_exc(JobNotFoundError,
                         self.model.set_selected_jobid_list, [1])

    def test_append_job(self):
        from job_model     import JobModel
        from job_view      import JobView
        from job_presenter import JobPresenter
        job = JobMock(5)
        self.model.append_job(job)
        m, v, p = self.model.get_newjob()
        assert isinstance(m, JobModel     ) 
        assert isinstance(v, JobView      ) 
        assert isinstance(p, JobPresenter ) 

    def test_delete_job(self):
        """Test the method: delete_job."""
        assert_catch_exc(JobNotFoundError, self.model.delete_job, 'job')

    def test_update_per_time(self):
        """Test the method: update_per_time."""
        pass


class TestManagerModelWithOneJob:

    def setup(self):
        self.model = ManagerModel()
        job = JobMock(3)
        self.model.append_job(job)

    def teardown(self):
        self.model = None

    def test_init(self):
        # test init
        ec = EventCatcher(self.model.init_event)
        self.model.init()
        assert_catch_event(ec)

        job_dict = self.model.get_job_dict()
        assert_equal(1, len(job_dict))

    def test_get_newjob(self):
        assert_not_catch_exc(JobNotFoundError, self.model.get_newjob)

        m, v, p = self.model.get_newjob()
        assert isinstance(m, JobModel     ) 
        assert isinstance(v, JobView      ) 
        assert isinstance(p, JobPresenter ) 

    def test_get_job_dict(self):
        assert_not_catch_exc(JobNotFoundError, self.model.get_job_dict)
        job_dict = self.model.get_job_dict()
        assert_equal(1, len(job_dict))

        for id, job in job_dict.items():
            id = id
            job = job

        newjob = self.model.get_newjob()
        assert_equal(job_dict[id], newjob)

    def test_set_selected_jobid_list(self):
        assert_catch_exc(JobNotFoundError,
                         self.model.set_selected_jobid_list, [1,2,3,4,5])
        assert_catch_exc(JobNotFoundError,
                         self.model.set_selected_jobid_list, [5])
        assert_not_catch_exc(JobNotFoundError,
                         self.model.set_selected_jobid_list, [3])

    def test_append_job(self):
        old_job = self.model.get_newjob()
        job = JobMock(8)
        self.model.append_job(job)
        new_job = self.model.get_newjob()

        assert_not_equal(old_job, new_job)

        job_dict = self.model.get_job_dict()
        assert_equal(2, len(job_dict) )

    def test_delete_job(self):
        """Test the method: delete_job."""
        ec = EventCatcher(self.model.update_event)
        assert_catch_exc(JobNotFoundError, self.model.delete_job, 9)

        self.model.delete_job( 3 )
        assert_catch_event(ec)
        assert_equal( 0, len(self.model.get_job_dict()) )

    #def test_update_per_time(self):
        #"""Test the method: update_per_time."""
        #pass


class TestManagerModelWithMoreThanTwoJob:

    def setup(self):
        self.model = ManagerModel()
        job1 = JobMock(3)
        job2 = JobMock(25)
        self.model.append_job(job1)
        self.model.append_job(job2)

    def teardown(self):
        self.model = None

    def test_init(self):
        # test init
        ec = EventCatcher(self.model.init_event)
        self.model.init()
        assert_catch_event(ec)

        job_dict = self.model.get_job_dict()
        assert_equal(2, len(job_dict))

    def test_get_newjob(self):
        assert_not_catch_exc(JobNotFoundError, self.model.get_newjob)

        m, v, p = self.model.get_newjob()
        assert_equal(m.id, 25)

    def test_get_job_dict(self):
        job_dict = self.model.get_job_dict()
        assert_equal(2, len(job_dict))

        job1 = job_dict[3]
        job2 = job_dict[25]
        assert_not_equal(job1, job2)

    def test_set_selected_jobid_list(self):
        assert_catch_exc(
            JobNotFoundError, self.model.set_selected_jobid_list, [1,2,3,4,5])
        assert_not_catch_exc(
            JobNotFoundError, self.model.set_selected_jobid_list, [3])
        assert_not_catch_exc(
            JobNotFoundError, self.model.set_selected_jobid_list, [25])
        assert_not_catch_exc(
            JobNotFoundError, self.model.set_selected_jobid_list, [3,25])

    def test_append_job(self):
        snd_job = self.model.get_newjob()

        job = JobMock(8)
        self.model.append_job(job)
        new_job = self.model.get_newjob()

        assert_equal(snd_job, new_job)

        job_dict = self.model.get_job_dict()
        print job_dict.keys()
        assert_equal(3, len(job_dict) )
        assert_equal( set([3,8,25]), set(job_dict.keys()) )

    def test_delete_job(self):
        """Test the method: delete_job."""
        ec = EventCatcher(self.model.update_event)
        assert_catch_exc(JobNotFoundError, self.model.delete_job, 12)

        self.model.delete_job( 3 )
        assert_catch_event(ec)
        assert_equal( 1, len(self.model.get_job_dict()) )

        self.model.delete_job( 25 )
        assert_catch_event(ec)
        assert_equal( 0, len(self.model.get_job_dict()) )

    ##def test_update_per_time(self):
        ##"""Test the method: update_per_time."""
        ##pass
    
