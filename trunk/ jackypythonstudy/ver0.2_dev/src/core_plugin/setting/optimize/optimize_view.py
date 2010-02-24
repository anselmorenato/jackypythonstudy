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

    def appendView(view, title):
        """Append the view into the book view."""

    def getContainer():
        """Get the container to append the view."""


from utils.wxutils import ViewBase
from optimize_xrc import xrcOptimize
# class OptimizeView(xrcOptimize, ViewComponent):
class OptimizeView(xrcOptimize, ViewBase):

    implements(IOptimizeView)

    def __init__(self, parent):
        """Constructor."""
        xrcOptimize.__init__(self, parent)
        ViewBase.__init__(self)

    def appendView(self, view, title):
        ctrl = self.getCtrl('ID_MultiBook')
        ctrl.AddPage(view, title)

    def getContainer(self):
        return self.getCtrl('ID_MultiBook')


from utils.wxutils import BindManager
class OptimizeInteracter(object):

    binder = BindManager()

    def __init__(self, view, presen):
        self.presen = presen
        self.binder.bindAll(view, self)


def main():
    app = wx.App(redirect=False)
    frame = wx.Frame(None, -1, 'Optimize Panel')

    view = OptimizeView(frame)
    panel = wx.Panel(view.getContainer(), -1)
    view.appendView(panel, 'Test')

    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
