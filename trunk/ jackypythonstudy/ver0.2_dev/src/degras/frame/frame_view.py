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


class FrameInteractor(object):

    def __init__(self, view, presenter):
        pass


class FrameView(wx.Frame):
    def __init__(self, id=-1, title='',
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE|wx.SUNKEN_BORDER|wx.CLIP_CHILDREN,
                ):
        wx.Frame.__init__(self, None, id, title, pos, size, style)
        
        # setup aui manager
        self.__auimgr = wx.aui.AuiManager()
        self.__auimgr.SetManagedWindow(self)

        self.SetMinSize(wx.Size(1024, 768))
        self.CentreOnScreen()

    # getset: title
    def get_title(self):
        return self.GetTitle()
    def set_title(self, title):
        self.SetTitle( title )
    title = property(get_title, set_title)

    # methods
    def append_pane(self, panel, paneinfo=None):
        self.__auimgr.AddPane( panel, paneinfo)
        self.__auimgr.Update()

    def set_menubar(self, menubar):
        self.SetMenuBar( menubar )

    def set_statusbar(self, statusbar):
        self.CreateStatusBar()

    def set_toolbar(self, toolbar):
        pass

    def show(self):
        self.CenterOnScreen()
        self.Show()

    def close(self):
        """Close the frame."""
        self.__auimgr.UnInit()
        del self.__auimgr
        self.Destroy()

    def get_perspective(self):
        return self.__auimgr.SavePerspective()

    def set_perspective(self, perspective):
        self.__aurmgr.LoadPerspective( perspective )
        self.__aurmgr.Update()

    def get_all_panes(self):
        return self.__auimgr.GetAllPanes()

    def get_pane(self, pane_name):
        return self.__auimgr.GetPane(pane_name)

    def refresh(sefl):
        self.__aurmgr.Update()
        self.Refresh()


def main():
    logfile =  "_error.log"
    app = wx.App(redirect=False, filename=logfile)
    frame = FrameView()
    panel = wx.Panel(frame, -1)
    frame.append_pane(panel)

    frame.Show()

    try:
        app.MainLoop()
    except:
        app.RedirectStdio()

if __name__ == '__main__':
    main()
