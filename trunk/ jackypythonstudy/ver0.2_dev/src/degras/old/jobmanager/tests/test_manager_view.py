#! /opt/python2.6/bin/python
#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura
#
# $Date: 2010-01-20 14:48:22 +0900 (水, 20 1 2010) $
# $Rev: 57 $
# $Author: ishikura $
#

# standard modules
import os, sys
from nose.tools import *
import wx

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from utils.test_helper import *
from utils.event import NagaraEvent, EventBindManager


set_bodypath(__file__)
from manager_view  import ManagerView
class TestManagerViewWithNoJob:
    
    def setup(self):
        self.app = wx.App()
        frame = wx.Frame(None)

        # self.job   = JobMock()
        self.view = ManagerView(frame)

#        self.view.update_all()
        frame.Show()

    def teardown(self):
        wx.CallAfter(self.app.Exit)
        self.app.MainLoop()
        self.view   = None

    def test_init(self):
        pass

#    def test_append(self):
        #from job_view import JobView
        #jobview = JobView()
        #prop_dict = dict(
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

        #for prop, val in prop_dict.items():
            #set_prop = 'set_'+prop
            #get_prop = 'get_'+prop
            #getattr(jobview, set_prop)( val )

        ## set state
        #jobview.set_state( 'Runnable' )

        ## set popup menu
        #request_dict = dict(
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
        #jobview.set_request_dict( request_dict )
        #self.view.append( jobview )

    def test_delete(self):
        ec = EventCatcher(self.view.delete_event)
        ec.trigger()
        assert_catch_event(ec)

#    def test_update(self):
#        pass
#
#    def test_popup_on_job(self):
#        pass
#
#    def test_requests(self):
#        pass
#
#    def test_rename(self):

#        jobid = msg
#        jobview = self.model.get_jobview( jobid )
#        jobname = self.view.get_jobname( jobid )
#        jobview.name = jobname
#        pass
#    
#    def test_enable_auto(self):
#        pass
#
#    def test_update_in_view(self):
#        pass



class TestManagerViewWithOneJob:

    def setup(self):

        self.app = wx.App()

        # create JobView
        from job_view import JobView
        job = JobView()
        # set properties
        self.init_prop_dict = dict(
            id            = 5           , 
            expected_time = '3:00'      , 
            start_time    = '15:00'     , 
            elasped_time  = '1:00'      , 
            finish_time   = ''          , 
            location      = 'hpcs'      , 
            jms           = 'LSF'       , 
            name          = 'test job'  , 
            project       = 'project X' , 
        )

        for prop, val in self.init_prop_dict.items():
            set_prop = 'set_'+prop
            get_prop = 'get_'+prop
            getattr(self.view, set_prop)( val )

        # set state
        self.view.set_state( 'Runnable' )

        # set popup menu
        self.init_request_dict = dict(
            request_submit  = False , 
            request_convert = False , 
            request_send    = False , 
            request_run     = True  , 
            request_stop    = True  , 
            request_cancel  = True  , 
            request_rerun   = False , 
            request_receive = False , 
            request_sync    = False , 
        )
        self.view.set_request_dict( self.init_request_dict )

        # self.job   = JobMock()
        self.view = ManagerView()

        self.view.update_all( [job] )
    
    def setup_selected(self):
        pass

    def teardown_selected(self):
        pass

    def setup_no_selected(self):
        pass

    def teardown_no_selected(self):
        pass

class TestManagerViewWithMoreThanThreeJob:
    """
    Test class for ManagerView with more than three jobs.
    """

    def setup_no_selected(self):
        pass

    def teardown_no_selected(self):
        pass

    def setup_one_selected(self):
        pass

    def teardown_one_selected(self):
        pass

    def setup_two_selected(self):
        pass

    def teardown_two_selected(self):
        pass

    def setup_all_selected(self):
        pass

    def teardown_all_selected(self):
        pass
