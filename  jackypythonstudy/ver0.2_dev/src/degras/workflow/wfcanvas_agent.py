#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura
#
# $Date: 2010-01-26 15:36:28 +0900 (火, 26 1 2010) $
# $Rev: 69 $
# $Author: ma $
#
import os, sys

class WorkFlowCanvas(object):

    def __init__(self, parent, model=None):

        # setup view
        try:
            parent_view = parent.get_view()
        except AttributeError:
            parent_view = parent

        self.__model = model
        from wfcanvas_view import WorkFlowCanvasView
        self.__view = WorkFlowCanvasView(parent_view)
        from  wfcanvas_presenter import WorkFlowCanvasPresenter
        self.__presen = WorkFlowCanvasPresenter( self.__model, self.get_view())
        #from flowcanvas import FlowCanvas
        #self.__view = FlowCanvas( parent_view )
        
        from wfcanvas_view import WorkFlowCanvasInteractor as wfcInteractor
        self.__inerractor = wfcInteractor(self.__view,self.__presen)

    def get_view(self):
        return self.__view


if __name__ == '__main__':
    import wx 
    app = wx.App(redirect=False)
    frame = wx.Frame(None, -1, 'Work Flow Canvas')

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
