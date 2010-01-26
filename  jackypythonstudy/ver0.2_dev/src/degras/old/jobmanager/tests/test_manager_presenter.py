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
import os, sys

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from utils.test_helper import *
set_bodypath(__file__)

# append the path for the target module

import wx
app = wx.App()

from  manager_presenter  import ManagerPresenter
from  manager_model      import ManagerModel
from  manager_view       import ManagerView


class TestManagerPresenter:

    def setup(self):
        self.app = wx.App(redirect=False)
        frame = wx.Frame(None, -1)
        self.model  = ManagerModel()
        self.view   = ManagerView(frame)
        self.presen = ManagerPresenter(self.model, self.view)

    def teardown(self):
        wx.CallAfter(self.app.Exit)
        self.app.MainLoop()
        self.model   = None
        self.view    = None
        self.present = None

    def test_init(self):
        assert isinstance(self.model.init_event, NagaraEvent)
    
    def test_append_job(self):
        assert isinstance(self.model.created_event, NagaraEvent)
        assert_method(self.model, 'get_newjob')
        assert_method(self.view, 'append')

        ##assert_method(self.model, 'get_newjob', ret=jobview)
        ##assert_method(self.view, 'append', args=[job])

    def test_delete_job(self):
        assert isinstance(self.model.delete_event, NagaraEvent)

    def test_update_view(self):
        assert isinstance(self.model.update_event, NagaraEvent)

        assert_method(self.model, 'get_job_dict')
        assert_method(self.view, 'update_all')

    def test_request_for_selected_job_in_view(self):
        request_list = [ 'submit', 'convert', 'send', 'run',
                        'stop', 'rerun', 'cancel', 'receive', 'sync', ]
        for req in request_list:
            event = req + '_event'
            assert isinstance(getattr(self.view, event), NagaraEvent)

        assert_method(self.view, 'get_selected_jobid_list')

    def test_rename_job(self):
        assert isinstance(self.view.rename_event, NagaraEvent)
        assert_method(self.view, 'get_jobname')

    def test_select_on_view(self):
        assert isinstance(self.view.select_event, NagaraEvent)
        assert_method(self.view, 'get_selected_jobid_list')
        assert_method(self.model, 'set_selected_jobid_list')

    def test_enable_auto(self):
        assert isinstance(self.view.set_auto_event, NagaraEvent)
        assert_method(self.view, 'is_auto')
        assert_method(self.view, 'enable_auto')

    def test_popup_on_job(self):
        assert isinstance(self.view.operate_event, NagaraEvent)
        assert_method(self.view, 'popup_jobmenu')

    def test_delete_job(self):
        assert isinstance(self.view.delete_event, NagaraEvent)
        assert_method(self.model, 'delete_job')

    def test_update_from_view(self):
        assert isinstance(self.view.update_event, NagaraEvent)

