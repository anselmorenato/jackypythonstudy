#  -*- encoding: utf-8 -*-
# Copyright (C)  2009 Takakazu Ishikura

# standard modules
import os, sys
from abc import ABCMeta, abstractmethod, abstractproperty

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from utils.event import NagaraEvent


class IMenubarView():
    __metaclass__ =  ABCMeta

    # events
    @abstractproperty
    def test_event(self): pass

    # methods
    @abstractmethod
    def get_menubar(self): pass

    @abstractmethod
    def set_edit_menu(self): pass

    @abstractmethod
    def set_file_menu(self): pass

    @abstractmethod
    def set_help_menu(self): pass

    @abstractmethod
    def set_nagara_menu(self): pass

    @abstractmethod
    def set_plugin_menu(self): pass

    @abstractmethod
    def set_project_menu(self): pass

    @abstractmethod
    def set_tool_menu(self): pass

    @abstractmethod
    def set_view_menu(self): pass

    @abstractmethod
    def set_workflow_menu(self): pass


class MenubarView(IMenubarView):
    def __init__(self):

        # define properties

        # generate events
        self._test_event = NagaraEvent()

    # events
    @property
    def test_event(self):
        return self._test_event

    # send events
    def _send_test(self, event):
        self.test_event.fire()

    # methods
    def set_nagara_menu(self):
        pass

    def set_file_menu(self):
        pass

    def set_project_menu(self):
        pass

    def set_edit_menu(self):
        pass

    def set_view_menu(self):
        pass

    def set_workflow_menu(self):
        pass

    def set_tool_menu(self):
        pass

    def set_plugin_menu(self):
        pass

    def set_help_menu(self):
        pass

    def get_menubar(self):
        pass

