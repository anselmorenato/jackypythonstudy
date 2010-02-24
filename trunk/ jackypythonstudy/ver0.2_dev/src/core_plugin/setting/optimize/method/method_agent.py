#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura
#
# $Date: 2010-02-22 21:35:39 +0900 (月, 22 2 2010) $
# $Rev: 105 $
# $Author: ishikura $
#
import os, sys

# nagara modules
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



from method_view      import MethodView, MethodInteracter
from method_presenter import MethodPresenter
class MethodSetting(object):

    def __init__(self, parent, model=None):

        self.__view   = MethodView(parent)
        self.__presen = MethodPresenter(self.__view, model)
        MethodInteracter(self.__view, self.__presen)

    def getView(self):
        return self.__view


def main():
    import wx
    app = wx.App(redirect=True)
    frame = wx.Frame(None, -1, 'Method Panel')

    from method_model import MethodModel
    model = MethodModel()
    agent = MethodSetting(frame, model)

    view = agent.getView()
    print view.optmethod, view.ncycle
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()

