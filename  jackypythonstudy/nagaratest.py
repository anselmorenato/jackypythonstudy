#! /usr/bin/env python
# _*_ coding: utf-8 _*_
# Copyright (C)  2009 Takakazu Ishikura

import wx
import logview
class FrameTest(wx.App):
    """Small frame test when called directly."""

    def __init__(self):
        logfile = '_error.log'
        wx.App.__init__(self, redirect=True, filename=logfile)

        self.frame = wx.Frame(None, -1, 'FrameTest')
        self.log = logview.LogView(self.frame)
        self.frame.Show()

