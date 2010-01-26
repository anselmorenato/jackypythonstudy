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

from jobmock import JobMock
from job_model  import JobModel, NotUsedRequestError
class TestJobModelWithState:
    
    def setUp(self):
        self.job   = JobMock(5)
        self.model = JobModel(self.job)

    def tearDown(self):
        self.model = None
        self.job   = None

    def test_init(self):
        prop_list = [
            'expected_time' , 
            'start_time'    , 
            'finish_time'   , 
            'elasped_time'  ,
            'jms'           , 
            'location'      , 
            'name'          , 
        ]
        assert_equal(self.model.get_state(), self.job.state)
        for prop in prop_list:
            assert_equal(getattr(self.model, prop), getattr(self.model, prop))

        req_set = set( self.model.get_available_request_dict().keys() )
        assert_equal( req_set, set( self.job.get_all_request()) )

    def test_run_request(self):
        for reqname, b in self.model.get_available_request_dict().items():
            print reqname
            if b:
                assert_not_catch_exc(
                    NotUsedRequestError, getattr(self.model, reqname) )
            else:
                assert_catch_exc(
                    NotUsedRequestError, getattr(self.model, reqname) )

        # state changed
        self.job.switch_state()
        for reqname, b in self.model.get_available_request_dict().items():
            print reqname
            if b:
                assert_not_catch_exc(
                    NotUsedRequestError, getattr(self.model, reqname) )
            else:
                assert_catch_exc(
                    NotUsedRequestError, getattr(self.model, reqname) )

    def test_get_available_request_dict(self):
        ava_req_list = [
            req for req, b in self.model.get_available_request_dict().items()
                if b
        ]
        assert_equal( set(ava_req_list), set(self.job.get_available_request()))

        # state changed
        self.job.switch_state()
        ava_req_list = [
            req for req, b in self.model.get_available_request_dict().items()
                if b
        ]
        assert_equal( set(ava_req_list), set(self.job.get_available_request()))

    def test_state_changed(self):
        state_catcher = EventCatcher(self.model.state_changed_event)
        self.job.switch_state()
        # assert_equal(state_catcher.is_catched(), True)
        assert_equal(state_catcher.count, 1)
        assert_equal(self.model.get_state(), self.job.state)

    def test_property_and_model_updated(self):
        update_catcher = EventCatcher(self.model.update_event)
        prop_val_dict = dict(
            expected_time = '2:00'       , 
            start_time    = '18:00'      , 
            finish_time   = '20:00'      , 
            elasped_time  = '1:00'       , 
            jms           = 'NQS'        , 
            location      = 'vlsn'       , 
            name          = 'Job name b' , 
        )

        i = 0
        for prop, value in prop_val_dict.items():
            i += 1
            set_method = 'set_' + prop
            get_method = 'get_' + prop
            getattr(self.job, set_method)(value)
            assert_catch_event( update_catcher )
            assert_equal( getattr(self.model, prop), value )

    def test_set_auto(self):
        enable = self.job.is_auto()
        assert_equal(self.model.is_auto(), enable)

        self.model.enable_auto(not enable)
        assert_equal(self.model.is_auto(), not enable)
        assert_equal(self.model.is_auto(), self.job.is_auto())

    def test_is_selected(self):
        assert_equal( self.model.is_selected(), False )
        self.model.enable_selected(True)
        assert_equal( self.model.is_selected(), True )

#    def test_delete(self):
#        pass

        
