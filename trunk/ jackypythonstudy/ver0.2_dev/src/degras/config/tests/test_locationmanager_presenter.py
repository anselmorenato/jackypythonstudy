#  -*- encoding: utf-8 -*-
import os, sys

nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from utils.test_helper import *
#sys.path.append( '../interfaces' )
sys.path.append( '../' )


class TestLocationManagerPresenterWithNoLocation:

    def setUp(self):
        import locationmanager_presenter as p
        import locationmanager_view      as v

        self.model  = m.LocationManagerModel()
        self.view   = v.LocationManagerView()
        self.presen = p.LocationManagerPresenter(self.model, self.view)

    def tearDown(self):
        self.p = None
        self.model = None
        self.view = None

    def testInit(self):
        ec = EventCatcher(self.model.init_event)
        assert ec.is_event()
        assert hasattr(self.view, 'init')

    def test_update_in_view(self):
        ec = EventCatcher(self.model.update_event)
        assert ec.is_event()
        assert hasattr(self.model, 'get_location_list')
        assert hasattr(self.view,  'set_location_list')

    def testSelect(self):
        self.presen.select()



    def testPopup(self):
        self.view.popupMenu()

    def testCreate(self):
        print 'create!'

    def testEdit(self):
        print( 'edit!' )

    def testCopy(self):
        pass

    def testDelete(self):
        pass

    def testSetDefault(self):
        pass

    def testClose(self):
        pass


class LocationManagerPresenterWithOneLocation:
    pass


class LocationManagerPresenterWithManyLocation:
    pass
