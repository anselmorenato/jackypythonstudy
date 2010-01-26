#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura

# standard modules
import os, sys

from nose.tools import *

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from utils.test_helper import *

# append the path for the target module
current_path = os.path.split( __file__ )[0]
sys.path.append( os.path.join(current_path, '..' ) )

import wx
app = wx.App()

from  job_presenter  import JobPresenter
from  job_model      import JobModel
from  job_view       import JobView, NotFoundRequestError
from  test_job_model import JobMock

class TestJobPresenter:

    def setup(self):
        from  job_presenter  import JobPresenter
        from  job_model      import JobModel
        from  job_view       import JobView, NotFoundRequestError
        from  jobmock        import JobMock
        self.model  = JobMock(1)
        self.view   = JobView()
        self.presen = JobPresenter(self.model, self.view)

    def teardown(self):
        self.model = None
        self.view = None
        self.present = None

    def test_init(self):
        # ec = EventCatcher(self.view.delete_event)
        ec = EventCatcher(self.model.state_changed_event)
        ec.trigger('fuga')
        assert_catch_event(ec,'fuga')
        assert_method(self.view, 'get_name', ret='task name' )
        #assert hasattr(self.presen, 'change_state')
        #assert ec.is_event()

    def test_change_state(self):
        mstate = self.model.get_state()

        # event catch and do method
        ec = EventCatcher(self.model.state_changed_event)
        ec.trigger()
        assert_catch_event(ec)

        state, image = self.view.get_state()
        assert_equal(state, mstate)

    def test_update_reqmenu(self):
        request_dict = {}
        ava_req_list = self.model.get_available_request()
        all_req_list = self.model.get_all_request()
        for req in all_req_list:
            request_dict[req] = True if req in ava_req_list else False

        self.presen.update_reqmenu()

        for req, enable in request_dict.items():
            reqname = req.split('_')[-1]
            reqid = 'ID_' + reqname.upper()
            if reqid=='ID_DELETE': continue
            ret_enable = self.view.is_enabled_menuitem(
                getattr(self.view, reqid))
            assert_equal(ret_enable, enable)

    def test_request(self):
        request_list = [
            'request_submit',
            'request_convert',
            'request_send',
            'request_run',
            'request_stop',
            'request_cancel',
            'request_rerun',
            'request_receive',
            'request_sync',
        ]
        for reqname in request_list:
            assert_method(self.presen, reqname)
            assert_method(self.model, reqname)

    def test_update_view(self):
        ec = EventCatcher(self.model.update_event)

        prop_val_dict = dict(
            expected_time = '2:00'       , 
            start_time    = '18:00'      , 
            finish_time   = '20:00'      , 
            elasped_time  = '1:00'       , 
            jms           = 'NQS'        , 
            location      = 'vlsn'       , 
            name          = 'Job name b' , 
        )

        for prop in prop_val_dict.keys():
            ec.trigger(prop)
            assert_catch_event(ec, prop)

            exp_val = getattr(self.model, prop)
            ret_val = getattr(self.view,  prop)

            assert_equal(ret_val, exp_val)

    def test_enable_auto(self):
        enable = True
        self.presen.enable_auto(enable)
        assert_equal(self.model.is_auto(), enable)

        enable = False
        self.presen.enable_auto(enable)
        assert_equal(self.model.is_auto(), enable)

