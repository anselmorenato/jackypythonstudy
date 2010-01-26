#! /opt/python2.6/bin/python
#  -*- encoding: utf-8 -*-
# Copyright (C)  2009 Takakazu Ishikura

# standard modules
import os, sys
from abc import ABCMeta, abstractmethod, abstractproperty
import wx
import wx.aui

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from utils.event import NagaraEvent


class IFrameView():
    __metaclass__ =  ABCMeta

    # events
    @abstractproperty
    def close_event(self): pass

    # properties with setter
    @abstractmethod
    def get_title(self): pass
    @abstractmethod
    def set_title(self, title): pass
    title = abstractproperty(get_title, set_title)

    # methods
    @abstractmethod
    def append_panel(self): pass

    @abstractmethod
    def set_menubar(self): pass

    @abstractmethod
    def set_statusbar(self): pass

    @abstractmethod
    def set_toolbar(self): pass


class FrameView(IFrameView, wx.Frame):
    def __init__(self, id=-1, title='',
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE|wx.SUNKEN_BORDER|wx.CLIP_CHILDREN,
                ):
        wx.Frame.__init__(self, None, id, title, pos, size, style)
        
        # setup aui manager
        self.__auimgr = wx.aui.AuiManager()
        self.__auimgr.SetManagedWindow(self)

        self.SetMinSize(wx.Size(1024, 768))


        # define properties
        self._title = 'title'

        # generate events
        self._close_event = NagaraEvent()

    # events
    @property
    def close_event(self):
        return self._close_event

    # properties with setter
    def get_title(self):
        return self._title
    def set_title(self, title):
        self._title = title
    title = property(get_title, set_title)

    # methods
    def append_panel(self, panel):
        self.__auimgr.AddPane(
            panel,
            wx.aui.AuiPaneInfo().
            Name('ProjectView').Caption('Project').Right().Layer(0).
            CloseButton(True).MaximizeButton(True).
            MinSize(wx.Size(200,100))
        )
        self.__auimgr.Update()

    def set_menubar(self, menubar):
        self.SetMenuBar( menubar )

    def set_statusbar(self, statusbar):
        self.CreateStatusBar()

    def set_toolbar(self, toolbar):
        pass

################################################################################

def main():
    logfile =  "_error.log"
    app = wx.App(redirect=False, filename=logfile)
    frame = FrameView()
    panel = wx.Panel(frame, -1)
    frame.append_panel(panel)

    frame.Show()

    try:
        app.MainLoop()
    except:
        app.RedirectStdio()

if __name__ == '__main__':
    main()
