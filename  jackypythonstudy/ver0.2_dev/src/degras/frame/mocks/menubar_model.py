#  -*- encoding: utf-8 -*-
# Copyright (C)  2009 Takakazu Ishikura

# standard modules
import os, sys
from abc import ABCMeta, abstractmethod, abstractproperty

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from utils.event import NagaraEvent


class IMenubarModel():
    __metaclass__ =  ABCMeta

    # events
    @abstractproperty
    def update_edit_event(self): pass

    @abstractproperty
    def update_file_event(self): pass

    @abstractproperty
    def update_plugin_event(self): pass

    @abstractproperty
    def update_project_event(self): pass

    @abstractproperty
    def update_tool_event(self): pass

    @abstractproperty
    def update_view_event(self): pass

    @abstractproperty
    def update_workflow_event(self): pass

    # properties with setter
    @abstractmethod
    def get_edit_menu(self): pass
    @abstractmethod
    def set_edit_menu(self, edit_menu): pass
    edit_menu = abstractproperty(get_edit_menu, set_edit_menu)

    @abstractmethod
    def get_file_menu(self): pass
    @abstractmethod
    def set_file_menu(self, file_menu): pass
    file_menu = abstractproperty(get_file_menu, set_file_menu)

    @abstractmethod
    def get_help_menu(self): pass
    @abstractmethod
    def set_help_menu(self, help_menu): pass
    help_menu = abstractproperty(get_help_menu, set_help_menu)

    @abstractmethod
    def get_nagara_menu(self): pass
    @abstractmethod
    def set_nagara_menu(self, nagara_menu): pass
    nagara_menu = abstractproperty(get_nagara_menu, set_nagara_menu)

    @abstractmethod
    def get_plugin_menu(self): pass
    @abstractmethod
    def set_plugin_menu(self, plugin_menu): pass
    plugin_menu = abstractproperty(get_plugin_menu, set_plugin_menu)

    @abstractmethod
    def get_project_menu(self): pass
    @abstractmethod
    def set_project_menu(self, project_menu): pass
    project_menu = abstractproperty(get_project_menu, set_project_menu)

    @abstractmethod
    def get_tool_menu(self): pass
    @abstractmethod
    def set_tool_menu(self, tool_menu): pass
    tool_menu = abstractproperty(get_tool_menu, set_tool_menu)

    @abstractmethod
    def get_view_menu(self): pass
    @abstractmethod
    def set_view_menu(self, view_menu): pass
    view_menu = abstractproperty(get_view_menu, set_view_menu)

    @abstractmethod
    def get_workflow_menu(self): pass
    @abstractmethod
    def set_workflow_menu(self, workflow_menu): pass
    workflow_menu = abstractproperty(get_workflow_menu, set_workflow_menu)


class MenubarModel(IMenubarModel):
    def __init__(self):

        # define properties
        self._edit_menu = None
        self._file_menu = None
        self._help_menu = None
        self._nagara_menu = None
        self._plugin_menu = None
        self._project_menu = None
        self._tool_menu = None
        self._view_menu = None
        self._workflow_menu = None

        # generate events
        self._update_edit_event = NagaraEvent()
        self._update_file_event = NagaraEvent()
        self._update_plugin_event = NagaraEvent()
        self._update_project_event = NagaraEvent()
        self._update_tool_event = NagaraEvent()
        self._update_view_event = NagaraEvent()
        self._update_workflow_event = NagaraEvent()

    # events
    @property
    def update_edit_event(self):
        return self._update_edit_event

    @property
    def update_file_event(self):
        return self._update_file_event

    @property
    def update_plugin_event(self):
        return self._update_plugin_event

    @property
    def update_project_event(self):
        return self._update_project_event

    @property
    def update_tool_event(self):
        return self._update_tool_event

    @property
    def update_view_event(self):
        return self._update_view_event

    @property
    def update_workflow_event(self):
        return self._update_workflow_event

    # properties with setter
    def get_edit_menu(self):
        return self._edit_menu
    def set_edit_menu(self, edit_menu):
        self._edit_menu = edit_menu
    edit_menu = property(get_edit_menu, set_edit_menu)

    def get_file_menu(self):
        return self._file_menu
    def set_file_menu(self, file_menu):
        self._file_menu = file_menu
    file_menu = property(get_file_menu, set_file_menu)

    def get_help_menu(self):
        return self._help_menu
    def set_help_menu(self, help_menu):
        self._help_menu = help_menu
    help_menu = property(get_help_menu, set_help_menu)

    def get_nagara_menu(self):
        return self._nagara_menu
    def set_nagara_menu(self, nagara_menu):
        self._nagara_menu = nagara_menu
    nagara_menu = property(get_nagara_menu, set_nagara_menu)

    def get_plugin_menu(self):
        return self._plugin_menu
    def set_plugin_menu(self, plugin_menu):
        self._plugin_menu = plugin_menu
    plugin_menu = property(get_plugin_menu, set_plugin_menu)

    def get_project_menu(self):
        return self._project_menu
    def set_project_menu(self, project_menu):
        self._project_menu = project_menu
    project_menu = property(get_project_menu, set_project_menu)

    def get_tool_menu(self):
        return self._tool_menu
    def set_tool_menu(self, tool_menu):
        self._tool_menu = tool_menu
    tool_menu = property(get_tool_menu, set_tool_menu)

    def get_view_menu(self):
        return self._view_menu
    def set_view_menu(self, view_menu):
        self._view_menu = view_menu
    view_menu = property(get_view_menu, set_view_menu)

    def get_workflow_menu(self):
        return self._workflow_menu
    def set_workflow_menu(self, workflow_menu):
        self._workflow_menu = workflow_menu
    workflow_menu = property(get_workflow_menu, set_workflow_menu)

    # send events
    def _send_update_edit(self, event):
        self.update_edit_event.fire()

    def _send_update_file(self, event):
        self.update_file_event.fire()

    def _send_update_plugin(self, event):
        self.update_plugin_event.fire()

    def _send_update_project(self, event):
        self.update_project_event.fire()

    def _send_update_tool(self, event):
        self.update_tool_event.fire()

    def _send_update_view(self, event):
        self.update_view_event.fire()

    def _send_update_workflow(self, event):
        self.update_workflow_event.fire()

