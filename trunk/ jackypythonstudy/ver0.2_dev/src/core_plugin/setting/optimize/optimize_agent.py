#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura
#
# $Date: 2010-02-22 21:35:39 +0900 (月, 22 2 2010) $
# $Rev: 105 $
# $Author: ishikura $
#
import os, sys

# naga a modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from  utils.event import  EventBindManager
from  core.log    import  Log

"""
    def save():
        "Save"

    def load(filename):
        "Load"
"""

from optimize_view      import OptimizeView, OptimizeInteracter
from optimize_presenter import OptimizePresenter
class OptimizeSetting(object):

    def __init__(self, parent, model=None):

        self.__view   = OptimizeView(parent)
        self.__presen = OptimizePresenter(self.__view, model)
        self.__model = model
        OptimizeInteracter(self.__view, self.__presen)

    def getView(self):
        return self.__view

    def getModel(self):
        return self.__model




def main():
    import wx
    app = wx.App(redirect=False)
    frame = wx.Frame(None, -1, 'Optimize Panel')

    from optimize_model import OptimizeModel
    model = OptimizeModel()
    agent = OptimizeSetting(frame, model)

    view = agent.getView()
    # print view.optmethod, view.ncycle
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()

