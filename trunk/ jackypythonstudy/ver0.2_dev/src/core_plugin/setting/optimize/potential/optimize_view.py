#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura
#
# $Date: 2010-02-22 21:35:39 +0900 (月, 22 2 2010) $
# $Rev: 105 $
# $Author: ishikura $
#
import os, sys
import wx

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )

from utils.deco    import nproperty
from core.model    import *


class IOptimizeView(Interface):
    optmethod     = Attribute("""Optimeze method.""")
    ncycle        = Attribute("""The number of cycle for optimization.""")
    ncycle_switch = Attribute("""Changing cycle number for sd + cg method.""")


from utils.wxutils import ViewBase
from optimize_xrc import xrcOptimize
class OptimizeView(xrcOptimize, ViewBase):

    implements(IOptimizeView)

    def __init__(self, parent):
        """Constructor."""
        xrcOptimize.__init__(self, parent)
        ViewBase.__init__(self)

    @nproperty
    def optmethod():

        ctrl_dict = {
            'ID_sd_method'    : 'sd'    , 
            'ID_cg_method'    : 'cg'    , 
            'ID_sd+cg_method' : 'sd+cg' , 
            'ID_nr_method'    : 'nr'    , 
        }

        def get(self):
            for id, method in ctrl_dict.items():
                if self.getCtrl(id).GetValue():
                    return method

        def set(self, method_name):
            rctrl_dict = dict( 
                [(value, key) for key, value in ctrl_dict.items()]
            )
            id = rctrl_dict[method_name]
            self.getCtrl(id).SetValue(True)

        return locals()

    @nproperty
    def ncycle():

        def get(self):
            return self.getCtrl('ID_ncycle').GetValue()

        def set(self, value):
            self.getCtrl('ID_ncycle').SetValue(value)

        return locals()

    @nproperty
    def ncycle_switch():

        def get(self):
            return self.getCtrl('ID_ncycle_switch').GetValue()

        def set(self, value):
            self.getCtrl('ID_ncycle_switch').SetValue(value)

        return locals()


from utils.wxutils import BindManager
class OptimizeInteracter(object):

    binder = BindManager()

    def __init__(self, view, presen):
        self.presen = presen
        self.binder.bindAll(view, self)

    @binder(wx.EVT_RADIOBUTTON, 'ID_sd_method')
    @binder(wx.EVT_RADIOBUTTON, 'ID_cg_method')
    @binder(wx.EVT_RADIOBUTTON, 'ID_sd+cg_method')
    @binder(wx.EVT_RADIOBUTTON, 'ID_nr_method')
    def h1(self, event):
        self.presen.selectMethod()
        self.presen.updateModel('optmethod')

    @binder(wx.EVT_TEXT, 'ID_ncycle')
    def h2(self, event):
        self.presen.updateModel('ncycle')

    @binder(wx.EVT_TEXT, 'ID_ncycle_switch')
    def h3(self, event):
        self.presen.updateModel('ncycle_switch')


def main():
    app = wx.App(redirect=False)
    frame = wx.Frame(None, -1, 'Optimize Panel')

    view = OptimizeView(frame)

    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()

