#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura
#
# $Date: 2010-02-02 21:59:40 +0900 (火, 02 2 2010) $
# $Rev: 77 $
# $Author: ishikura $
#
# standard modules
import os, sys

# nagara modules
from wfcanvas_view import WorkFlowCanvasView
from  wfcanvas_presenter import WorkFlowCanvasPresenter
from wfcanvas_view import WorkFlowCanvasInteractor as wfcInteractor

class WorkFlowCanvas(object):

    def __init__(self, parent, model=None):

        # setup view
        try:
            parent_view = parent.get_view()
        except AttributeError:
            parent_view = parent

        self.__model = model
        #self.__view = WorkFlowCanvasView(parent_view)
        # setup presenter
        #self.__presen = WorkFlowCanvasPresenter( self.__model, self.get_view())
        # setup interactor
        #self.__interactor = wfcInteractor(self.__view,self.__presen)
        
        from flowcanvas import FlowCanvas
        self.__view = FlowCanvas( parent_view )

    def get_view(self):
        return self.__view
    
    def get_presenter(self):
        return self.__presen

    def get_interactor(self):
        return self.__interactor


if __name__ == '__main__':
    import wx 
    app = wx.App(redirect=False)
    frame = wx.Frame(None, -1, 'Work Flow Canvas', size=(800,600))

    wfc = WorkFlowCanvas( frame )

    frame.Show()
    app.MainLoop()


    # wx.InitAllImageHandlers()
    # ogl.OGLInitialize()

    # from flowcanvas import FlowFrame
    # frame = FlowFrame(None, -1, 'Work Flow Canvas')
    # app.SetTopWindow(frame)
    # frame.Show(True)
    # app.MainLoop()
