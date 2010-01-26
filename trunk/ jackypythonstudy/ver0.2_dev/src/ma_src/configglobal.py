#! /opt/python2.6/bin/python
#  -*- encoding: utf-8 -*-
import os, sys

import wx
import wx.xrc as xrc
from configglobal import *

xrcfile = 'configglobal.xrc'

class ConfigGlobal(wx.Panel):
    def __init__(self, parent, name='Config Global'):
        self.name = name
        self.initView(parent)
        self.initConfig()
        self.initBind()
        
    def initView(self, parent):
        self.res = xrc.XmlResource(xrcfile)
        pre = wx.PrePanel()
        self.res.LoadOnPanel(pre, parent, "Global")
        self.PostCreate(pre)

    def initConfig(self):
        self.ctrls = {}

        # for dictionary of config
        self.cache = dict(
            user = 'ishikura',
            host = ['133.66.117.139', '133.66.117.138',
                    'hpc.cc.nagoya-u.ac.jp', 'ccfep1.center.ims.ac.jp'],
            port = 22,
            passwd = '',
            is_active = False,
            NAGARA_ROOT = '/home/ishikura/Nagara',
            PROJECT_ROOT = '/home/ishikura/Nagara/projects',
            server_cmd = '/home/ishikura/Nagara/app/src/server.py',
            project_name = 'paics-test',
        )

        init_config = dict(
            user = 'ishikura',
            host = '133.66.117.139',
            port = 22,
            passwd = '',
            is_active = False,
            NAGARA_ROOT = '/home/ishikura/Nagara',
            PROJECT_ROOT = '/home/ishikura/Nagara/projects',
            server_cmd = '/home/ishikura/Nagara/app/src/server.py',
            project_name = 'paics-test',
        )

        ctrl_names = [
            'user', 'host', 'port', 'passwd', 'NAGARA_ROOT',
            'PROJECT_ROOT', 'server_cmd', 'project_name'
        ]
        # dictionary of controls
        for ctrl_name in ctrl_names:
            self.ctrls[ctrl_name] = xrc.XRCCTRL(self, ctrl_name)

        # set values to text ctrl from
        self.setConfig(**init_config)

    def initBind(self):
        self.Bind(wx.EVT_BUTTON, self.onGetConfig, id=xrc.XRCID('get_config'))
        self.Bind(wx.EVT_BUTTON, self.onGetPasswd, id=xrc.XRCID('get_passwd'))
        # self.Bind(wx.EVT_BUTTON, self.onGetPasswd, self.ctrls['get_config'])
        # self.Bind(wx.EVT_BUTTON, self.onGetPasswd, self.ctrls['get_passwd'])


    def onGetConfig(self, event):
        """ store the config to cache
        """
        for (key, ctrl) in self.ctrls.items():
            self.cache[key] = ctrl.GetValue()

    def save_configs(self):
        """Save the configs to cache."""
        for (key, ctrl) in self.ctrls.items():
            self.cache[key] = ctrl.GetValue()

    def get_configs(self):
        """ return the remote configurations
        """
        self.save_configs()
        config = {}
        for (key, value) in self.cache.items():
            config[key] = value
        return config

    def setConfig(self, **config):
        """ set remote configurations
        """
        for key, value in config.items():
            if self.ctrls.get(key):
                self.ctrls[key].SetValue( str(value) )

    def onGetPasswd(self, event):
        # self.printLog("In onGetPasswd : ")
        username = 'ishikura'
        host = '133.66.117.139'

        # prompt for user's password
        return  wx.GetPasswordFromUser(
                    "Enter Password for " + username + "@" + host,
                    "SSH Login Password:", default_value="", parent=None)


################################################################################

def main():
    logfile =  "_error.log"
    app = wx.App(redirect=False, filename=logfile)
    frame = wx.Frame(None, -1, "TestFrame")

    # panel = wx.Panel(frame,-1)
    panel = ConfigRemote(frame)

    print panel.get_configs()

    # sizer
    # sizer = wx.BoxSizer()
    # sizer.Add(panel, 1, wx.EXPAND | wx.ALL, 20)
    # sizer.Add(panel)
    # panel.SetSizer(sizer)
    
    frame.Show()

    try:
        app.MainLoop()
    except:
        app.RedirectStdio()


if __name__ == '__main__':
    main()


