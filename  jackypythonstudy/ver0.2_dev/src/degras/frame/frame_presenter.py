#  -*- encoding: utf-8 -*-
# Copyright (C)  2009 Takakazu Ishikura

# standard modules
import os, sys

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from  utils.event import  NagaraEvent
from  core.log    import  Log

class FramePresenter(object):

    def __init__(self, model=None, view=None):
        self.model = model
        self.view = view
        self.init()
    
    def init(self):
        # self._log_recieve('init')

        pass

        # # statusbar
        # from statusbar import Statusbar
        # statusbar = Statusbar()
        # self.view.set_statusbar( statusbar.get_view() )

        # p

        # Project Manger pane
        # from projectmanager import 
        # projectmanger = ProjectManager()
        # self.view.append_pane( projectmanager.get_view() )

    def append_pane(self, pane, paneinfo):
        try:
            window = pane.get_view()
        except AttributeError:
            window = pane

        self.view.append_pane( window, paneinfo )


    # def onExit(self, event):
        # """Exit the frame."""
        # self.molview.OnClose(event)
        # self.OnClose(event)

    # def onCloseRemote(self, event):
        # self.closeRemote()


    # def _log_recieve(self, listener_name):
        # info_list = self.binder.get_info(listener_name)
        # for info in info_list:
            # obj = info['object_name']
            # evt = info['event_name']
            # cls = info['class_name']
            # mes = 'Recieved {0} of {1}:{2} at {3}'
            # Log( mes.format(evt, obj, cls, listener_name) )

def main():
    import wx
    from frame_view       import FrameView
    from frame_interactor import FrameInteractor

    logfile =  "_error.log"
    app = wx.App(redirect=False, filename=logfile)

    fv = FrameView()
    fp = FramePresenter(fv)
    panel = wx.Panel(fv, -1)
    fv.append_pane(panel)

    fv.Show()

    try:
        app.MainLoop()
    except:
        app.RedirectStdio()

if __name__ == '__main__':
    main()
