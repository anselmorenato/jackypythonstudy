#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura

# standard modules
import os, sys

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

    def setUp(self):
        from  job_presenter  import JobPresenter
        from  job_model      import JobModel
        from  job_view       import JobView, NotFoundRequestError
        from  jobmock        import JobMock
        job         = JobMock(1)
        self.model  = JobModel(job)
        self.view   = JobView()
        self.presen = JobPresenter(self.model, self.view)

    def tearDown(self):
        self.model = None
        self.view = None
        self.present = None

    def test_init(self):
        # ec = EventCatcher(self.view.delete_event)
        ec = EventCatcher(self.model.delete_event)
        ec.trigger('fuga')
        assert_catch_event(ec,'fuga')
        assert_method(self.view, 'get_name', ret='task name' )
        #assert hasattr(self.presen, 'change_state')
        #assert ec.is_event()

    def test_change_state(self):
        assert_method(self.model, 'get_state', ret='Running')
        assert_method(self.view, 'set_state', args=['Running'])

        assert_method(self.model, 'get_available_request_dict')
        req_dict = self.model.get_available_request_dict()
        assert_method(self.model, 'get_available_request_dict', args=[req_dict])

        assert_method(self.view, 'set_request_dict')
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
        assert_method(self.view, 'set_request_dict', args=[request_dict])

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
        for prop, val in prop_val_dict.items():
            ec.trigger(prop)
            assert_catch_event(ec, prop)

            set_prop = 'set_'+prop
            get_prop = 'get_'+prop

            assert_method(self.model, prop)
            assert_method(self.view , set_prop, args=[val])

    def test_delete_in_model(self):
        pass

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
            assert_method(self.model, reqname)
