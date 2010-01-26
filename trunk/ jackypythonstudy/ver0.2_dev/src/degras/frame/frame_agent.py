#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura

# standard modules
import os, sys

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from  utils.event import  EventBindManager
from  core.log    import  Log


class Frame(object):

    def __init__(self):
        from frame_view  import FrameView
        from frame_presenter import FramePresenter

        self.view = FrameView()
        self.presen = FramePresenter(view=self.view)

    def get_view(self):
        return self.view

    def append_pane(self, pane, paneinfo):
        self.presen.append_pane(pane, paneinfo)

    def set_menubar(self, menubar):
        self.view.set_menubar(menubar)

    def show(self):
        self.view.show()

    def init(self):
        self.presen.init()

if __name__ == '__main__':

    import wx

    app = wx.App(redirect=False)
    frame = Frame()
    frame.init()
    panel = wx.Panel(frame.get_view(), -1)
    frame.append_pane(panel, None)
    frame.show()

        # menubar

    app.MainLoop()
