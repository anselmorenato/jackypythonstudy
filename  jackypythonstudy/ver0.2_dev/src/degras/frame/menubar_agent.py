#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura

# standard modules
import os, sys

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from  utils.event import  EventBindManager
from  core.log    import  Log


class Menubar(object):

    def __init__(self):
        import menubar_view as mv
        from menubar_presenter import MenubarPresenter

        self.view = mv.MenubarView()
        # model = MenubarModel()
        p = MenubarPresenter( self.view)
        interactor = mv.MenubarInteractor(self.view,p)
        
    
    def get_view(self):
        return self.view

if __name__ == '__main__':

    import wx

    app = wx.App(redirect=False)
    frame = wx.Frame(None, -1, 'Test')
    menubar = Menubar()
    frame.SetMenuBar(menubar.get_view())
    frame.Show()

    app.MainLoop()
