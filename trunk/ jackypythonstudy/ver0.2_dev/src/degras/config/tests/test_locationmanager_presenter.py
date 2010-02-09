#  -*- encoding: utf-8 -*-
import os, sys

import wx
from nose.tools import *

nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from utils.test_helper import *
#sys.path.append( '../interfaces' )
sys.path.append( '../' )


class TestLocationManagerPresenterWithNoLocation:

    def setUp(self):
        self.app = wx.App()
        frame = wx.Frame(None)

        import locationmanager_presenter as p
        import locationmanager_view      as v

        self.view   = v.LocationManagerView(frame)
        self.presen = p.LocationManagerPresenter(self.view)

        # frame.Show()

    def tearDown(self):
        wx.CallAfter(self.app.Exit)
        self.app.MainLoop()
        self.p = None
        self.view = None

    def testInit(self):
        assert_equal(self.view.isEnabled('ID_new_button'), True)
        assert_equal(self.view.isEnabled('ID_edit_button'), False)
        assert_equal(self.view.isEnabled('ID_copy_button'), False)
        assert_equal(self.view.isEnabled('ID_del_button'), False)
    
        # ec = EventCatcher(self.model.init_event)
        # assert ec.is_event()
        # assert hasattr(self.view, 'init')

    def testSelect(self):
        assert_equal(self.presen.select(), False)

    def testPopup(self):
        assert_equal(self.presen.popup(), False)

    # def testCreate(self):
    #     assert_equal(self.presen.create(), True)



    # def test_update_in_view(self):
    #     ec = EventCatcher(self.model.update_event)
    #     assert ec.is_event()
    #     assert hasattr(self.model, 'get_location_list')
    #     assert hasattr(self.view,  'set_location_list')

#     def testEdit(self):
#         print( 'edit!' )

#     def testCopy(self):
#         pass

#     def testDelete(self):
#         pass

#     def testSetDefault(self):
#         pass

#     def testClose(self):
#         pass


# class LocationManagerPresenterWithOneLocation:
#     pass


# class LocationManagerPresenterWithManyLocation:
#     pass
