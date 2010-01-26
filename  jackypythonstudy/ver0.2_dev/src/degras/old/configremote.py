#! /usr/bin/env python
# _*_ coding: utf-8 _*_
# Copyright (C)  2009 Takakazu Ishikura

import os, sys
import wx
import wx.xrc as xrc
from configremote_xrc import xrcConfigRemote

#-------------------------------------------------------------------------------

class ConfigRemote(xrcConfigRemote):

    """
    The Dialog Remote class.
    """

    def __init__(self, parent, name='Remote', log=None):
        xrcConfigRemote.__init__(self, parent)
        self.__name = name
        self.__ctrls = {}
        self.log = log
        self.initView(parent)
        self.initConfig()
        self.initBind()
        
    def initView(self, parent):
        pass

    def initConfig(self, configs=None):

        # for dictionary of config
        self.__cache = dict(
            user = 'ishikura',
            host = ['133.66.117.139', '133.66.117.138',
                    'hpc.cc.nagoya-u.ac.jp', 'ccfep1.center.ims.ac.jp'],
            port = 22,
            passwd = '',
        )
        if not configs:
            configs = dict(
                user = 'ishikura',
                host = '133.66.117.139',
                port = 22,
                passwd = '',
            )
        # dictionary of controls
        for ctrl_name in self.__cache:
            self.__ctrls[ctrl_name] = xrc.XRCCTRL(self, ctrl_name)

        # set values to text ctrl from
        self.setConfigs(**configs)

    def initBind(self):
        self.Bind(wx.EVT_BUTTON, self.onOk, id=xrc.XRCID('ok'))
        self.Bind(wx.EVT_BUTTON, self.onCancel, id=xrc.XRCID('cancel'))

    def saveConfigs(self):
        for (key, ctrl) in self.__ctrls.items():
            self.__cache[key] = ctrl.GetValue()

    def getConfigs(self):
        return self.__cache

    def onOk(self, event):
        """Store the remote setting and destroy self object."""
        for (key, ctrl) in self.__ctrls.items():
            self.__cache[key] = ctrl.GetValue()
        self.SetReturnCode(wx.ID_OK)
        self.Destroy()

    def onCancel(self, event):
        """Destroy self object without saveing remote configs."""
        self.__cache = None
        self.SetReturnCode(wx.ID_CANCEL)
        self.Destroy()

    def setConfigs(self, **configs):
        """Set the remote configs."""
        for key, value in configs.items():
            if self.__ctrls.get(key):
                self.__ctrls[key].SetValue( str(value) )

    # context manager
    def __enter__(self):
        self.ShowModal()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.Destroy()
        if exc_type:
            return False
        return True

################################################################################

def main():
    logfile =  "_error.log"
    app = wx.App(redirect=False, filename=logfile)
    frame = wx.Frame(None, -1, "TestFrame")
    frame.Show()

    with ConfigRemote(frame) as dlg:
        remote_configs = dlg.getConfigs()

    print remote_configs

    try:
        app.MainLoop()
    except:
        app.RedirectStdio()


if __name__ == '__main__':
    main()

