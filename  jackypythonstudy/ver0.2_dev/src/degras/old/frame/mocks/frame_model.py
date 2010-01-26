#! /opt/python2.6/bin/python
#  -*- encoding: utf-8 -*-
# Copyright (C)  2009 Takakazu Ishikura

# standard modules
import os, sys
from abc import ABCMeta, abstractmethod, abstractproperty

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from utils.event import NagaraEvent


class IFrameModel():
    __metaclass__ =  ABCMeta

    # events
    @abstractproperty
    def init_event(self): pass

    # properties
    @abstractproperty
    def menubar(self): pass

    @abstractproperty
    def panel_dict(self): pass

    @abstractproperty
    def status(self): pass

    @abstractproperty
    def toolbar(self): pass

    # properties with setter
    @abstractmethod
    def get_title(self): pass
    @abstractmethod
    def set_title(self, title): pass
    title = abstractproperty(get_title, set_title)

    # methods
    @abstractmethod
    def append_pane(self): pass

    @abstractmethod
    def append_panel(self): pass


class FrameModel(IFrameModel):
    def __init__(self):

        # define properties
        self.__title = 'title'
        self.__menubar = 'b'
        self.__panel_dict = 'a'
        self.__status = 'd'
        self.__toolbar = 'c'
        self.__perspective_list = []
        self.__panel_dict = {}

        # generate events
        self._init_event = NagaraEvent()

    # properties
    @property
    def menubar(self):
        return self._menubar

    @property
    def panel_dict(self):
        return self._panel_dict

    @property
    def status(self):
        return self._status

    @property
    def toolbar(self):
        return self._toolbar

    # events
    @property
    def init_event(self):
        return self._init_event

    # properties with setter
    def get_title(self):
        return self._title
    def set_title(self, title):
        self._title = title
    title = property(get_title, set_title)

    # methods
    def append_pane(self, parent, type):
        pass

    import wx
    def append_panel(self, parent):
        panel = wx.Panel(parent, -1)
        self.__panel_dict['panel'] = panel
        return panel



