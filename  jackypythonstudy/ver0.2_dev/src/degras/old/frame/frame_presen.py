#! /opt/python2.6/bin/python
#  -*- encoding: utf-8 -*-
# Copyright (C)  2009 Takakazu Ishikura

# standard modules
import os, sys

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from  utils.event import  EventBindManager
from  core.log    import  Log

class FramePresenter(object):
    
    binder = EventBindManager()    

    def __init__(self, model, view):
        self.model = model
        self.view = view
    
        self.binder.bind_all(self)

    @binder("model.init_event")
    def init_on_model(self, msg):
        self._log_recieve('init_on_model')
        self.model.append_panel(self.view)

        # menubar
        menubar = self.model.get_menubar()
        self.view.set_menubar( menubar )


    @binder("view.close_event")
    def close_on_view(self, msg):
        self._log_recieve('close_on_view')


    def _log_recieve(self, listener_name):
        info_list = self.binder.get_info(listener_name)
        for info in info_list:
            obj = info['object_name']
            evt = info['event_name']
            cls = info['class_name']
            mes = 'Recieved {0} of {1}:{2} at {3}'
            Log( mes.format(evt, obj, cls, listener_name) )

def main():
    import wx
    from frame_view  import FrameView
    from frame_model import FrameModel


    logfile =  "_error.log"
    app = wx.App(redirect=False, filename=logfile)
    fv, fm = FrameView(), FrameModel()
    fp = FramePresenter(fm, fv)
    panel = wx.Panel(fv, -1)
    fv.append_panel(panel)

    # menubar
    from menubar_view      import MenubarView
    from menubar_model     import MenubarModel
    from menubar_presenter import MenubarPresenter
    mm, mv = MenubarModel(), MenubarView(fv)
    mp = MenubarPresenter(mm, mv)
    mm.init_event.fire()
    fv.set_menubar(mv)

    fv.Show()

    try:
        app.MainLoop()
    except:
        app.RedirectStdio()

if __name__ == '__main__':
    main()
