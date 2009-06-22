#!/usr/bin/env python
#coding=utf-8

import wx
import wx.lib.agw.labelbook as LB

from wx.lib.embeddedimage import PyEmbeddedImage

imagebmp = PyEmbeddedImage(

"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAHFJ"

"REFUWIXt1jsKgDAQRdF7xY25cpcWC60kioI6Fm/ahHBCMh+BRmGMnAgEWnvPpzK8dvrFCCCA"

"coD8og4c5Lr6WB3Q3l1TBwLYPuF3YS1gn1HphgEEEABcKERrGy0E3B0HFJg7C1N/f/kTBBBA"
    "+Vi+AMkgFEvBPD17AAAAAElFTkSuQmCC")

class MyFrame(wx.Frame):
    def _InitCtrl(self):
        self.panel = wx.Panel(self)
#        自定义style时,要修改下一行,或后面用self.labelbook.SetWindowStyleFlag(style)修改
        self.labelbook = LB.LabelBook(self.panel, -1)

        self.imagelist = self.CreateImageList()
        self.labelbook.AssignImageList(self.imagelist)

        for i in range(5):
            self.labelbook.AddPage(wx.StaticText(self.labelbook, -1,
u'Panel%d'%i),
                                      u'Panel%d'%i, True, i)

        self.labelbook.SetSelection(0)

    def _InitSizer(self):
        self._szMainSizer = wx.BoxSizer(wx.VERTICAL)
        self._szMainSizer.AddWindow(self.labelbook, 1, flag=wx.EXPAND)

        self.panel.SetSizer(self._szMainSizer)

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, u'Rank Contral',
size=wx.Size(800,600))
        self.Centre()

        self._InitCtrl()
        self._InitSizer()

    def CreateImageList(self):

        imagelist = wx.ImageList(32, 32)

        bmp = imagebmp.GetBitmap()

        for i in range(5):
            imagelist.Add(bmp)

        return imagelist

class MyApp(wx.App):
    def OnInit(self):
        self.main = MyFrame(None)
        self.main.Show()
        self.SetTopWindow(self.main)
        return True

def main():
    app = MyApp(0)
    app.MainLoop()

if __name__ == '__main__':
    main() 