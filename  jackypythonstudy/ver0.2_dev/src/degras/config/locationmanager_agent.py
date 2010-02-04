#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura
#
# $Date: 2010-02-03 17:29:52 +0900 (水, 03 2 2010) $
# $Rev: 80 $
# $Author: ishikura $
#
# standard modules
import os, sys

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from  utils.event import  EventBindManager
from  core.log    import  Log


from locationmanager_view      import LocationManagerView
from locationmanager_presenter import LocationManagerPresenter
class LocationManager(object):

    def __init__(self, view, model=None):

        self.__view   = LocationManagerView(view)
        self.__presen = LocationManagerPresenter(view=self.__view)

    def getView(self):
        return self.__view

    def init(self):
        self.__presen.init()

if __name__ == '__main__':

    import wx

    app = wx.App(redirect=False)
    frame = wx.Frame(None, -1, 'Location Manager Agent')
    lm = LocationManager(frame)
    frame.Show()

        # menubar

    app.MainLoop()
