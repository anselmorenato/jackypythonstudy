#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura
#
# $Date: 2010-01-20 13:52:45 +0900 (水, 20 1 2010) $
# $Rev: 54 $
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
from job_view  import JobView
class TestJobViewWithState:
    
    def setup(self):
        self.app = wx.App()

        # self.job   = JobMock()
        self.view = JobView()

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

    def teardown(self):
        wx.CallAfter(self.app.Exit)
        self.app.MainLoop()
        self.view   = None

    def test_init(self):

        # test properties
        for prop, val in self.init_prop_dict.items():
            exp_val = val
            ret_val = getattr(self.view, prop)
            assert_equal( ret_val, exp_val )

        # test init state
        state, image = self.view.get_state()
        assert_equal(state, 'Runnable')

        # test init request

    def test_request_menu(self):
        menu = self.view.get_menu()
        for menuitem in menu.GetMenuItems():
            itemname = menuitem.GetLabel()
            enable   = menuitem.IsEnabled()
            reqname  = 'request_' + itemname
            ret_enable = self.init_request_dict[reqname]

            assert reqname in self.init_request_dict.keys(), reqname
            assert_equal(ret_enable, enable)

    def test_state_and_image(self):
        import degras.image as im

        for state in im.JOBSTATE_PATH_DICT.keys():
            image = im.get_jobstate_image(state)
            # set state
            self.view.set_state( state )
            ret_state, ret_image = self.view.get_state()
            assert_equal(ret_state, state)
            assert_equal(ret_image, image)

    def test_update_properties(self):
        prop_dict = dict(
            id            = 5           , 
            expected_time = '5:00'      , 
            start_time    = '18:00'     , 
            elasped_time  = '5:00'      , 
            finish_time   = '23:00'     , 
            location      = 'vlsn'      , 
            jms           = 'NQS'       , 
            name          = 'test job 2', 
            project       = 'project Y' , 
        )
        for prop, val in prop_dict.items():
            set_prop = 'set_'+prop
            get_prop = 'get_'+prop
            getattr(self.view, set_prop)( val )

        for prop, val in prop_dict.items():
            exp_val = val
            ret_val = getattr(self.view, prop)
            assert_equal( ret_val, exp_val )

    def test_update_state(self):
        self.view.set_state( 'Running' )
        import degras.image as im
        expected_image = im.get_jobstate_image('Running')

        ret_state, ret_image = self.view.get_state()
        assert_equal(ret_state, 'Running')
        assert_equal(ret_image, expected_image)

    def test_update_requests(self):
        request_dict = dict(
            request_submit  = False , 
            request_convert = False , 
            request_send    = False , 
            request_run     = False , 
            request_stop    = True  , 
            request_cancel  = True  , 
            request_rerun   = False , 
            request_receive = False , 
            request_sync    = False , 
        )
        self.view.set_request_dict( request_dict )

        menu = self.view.get_menu()
        for menuitem in menu.GetMenuItems():
            itemname = menuitem.GetLabel()
            enable   = menuitem.IsEnabled()
            reqname  = 'request_' + itemname
            ret_enable = request_dict[reqname]

            assert reqname in request_dict.keys(), reqname
            assert_equal(ret_enable, enable)

    # Todo
    def test_on_select(self):
        pass

    def test_on_enable_auto(self):
        pass
