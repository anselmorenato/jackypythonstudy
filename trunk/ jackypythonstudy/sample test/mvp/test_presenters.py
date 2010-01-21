#----------------------------------------------------------------------------
# Name:         test_presenters.py
# Purpose:      Unittesting for the AlbumPresenter
#
# Author:       Peter Damoc (peter at sigmacore.net)
#               
# Created:      January 2006
# Version:      0.1 
# Licence:      wxWindows license

import unittest
import mock_objects
import models
import presenters

class TestAlbumPresenter(unittest.TestCase):
    '''
    A sample test case to demonstrate the use of mock objects
    '''
    
    def setUp(self):
        self.someAlbums = models.someAlbums

    def testUpdateCausesComposerEnabledToBeRefreshed(self):
        view = mock_objects.MockAlbumWindow();
        model = [models.Album(*data) for data in self.someAlbums]
        interactor = mock_objects.MockAlbumInteractor()
        presenter = presenters.AlbumPresenter(model, view, interactor);
        assert view.isClassical() is False
        assert view.composerIsEnabled is False
        view.setClassical(True)
        presenter.dataFieldUpdated()
        assert view.composerIsEnabled is True
        
    def testApplySavesDataToModel(self):
        view = mock_objects.MockAlbumWindow();
        model = [models.Album(*data) for data in self.someAlbums]
        interactor = mock_objects.MockAlbumInteractor()
        presenter = presenters.AlbumPresenter(model, view, interactor);
        newTitle = "Some Other Title"
        view.title = newTitle
        presenter.updateModel()
        assert view.title == newTitle

    def testCancelRestoresDataFromModel(self):
        view = mock_objects.MockAlbumWindow();
        model = [models.Album(*data) for data in self.someAlbums]
        interactor = mock_objects.MockAlbumInteractor()
        presenter = presenters.AlbumPresenter(model, view, interactor);
        newTitle = "Some Other Title"
        view.title = newTitle
        presenter.loadViewFromModel()
        assert view.title != newTitle

if __name__ == '__main__':
    unittest.main()
