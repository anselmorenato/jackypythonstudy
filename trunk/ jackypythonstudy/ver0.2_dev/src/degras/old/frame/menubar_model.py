#! /opt/python2.6/bin/python
#  -*- encoding: utf-8 -*-
# Copyright (C)  2009 Takakazu Ishikura

# standard modules
import os, sys
from abc import ABCMeta, abstractmethod, abstractproperty

# pypi modules
import yaml

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from utils.event import NagaraEvent

# type:
#     nothing, command, separator, submenu, checkable

NAGARA_MENU = """
- {id: about_nagara, label: About Nagara, type: command ,
   enable: true, context: , keybind: Alt+Shift+5, icon: ,
   help: 'This is About Nagara'}

- {id: sep, label: sep, type: separator, enable: true}

- {id: check_update, label: Check Update, type: command ,
   enable: true, context: , keybind: none, icon: , help:  }

- {id: quit, label: Quit, type: command ,
   enable: true, context: , keybind: Ctrl+q, icon: , help: }

"""

FILE_MENU = """
- {id: open_molecule, label: Open Molecule, type: command ,
   enable: true, context: , keybind: Alt+Shift+5, icon: ,
   help: 'This is About Nagara'}
"""


PROJECT_MENU = """
- id: add_task
  label: Add Task
  type: submenu
  enable: true
  keybind:
  icon:
  help:  Add selected task 
  context:
      - {id: energy, label: Energy, type: command ,
         enable: true, context: , keybind: , icon: , help: }
      - {id: optimize, label: Optimize, type: command ,
         enable: true, context: , keybind: , icon: , help: }
      - {id: dynamics, label: Dynamics, type: command ,
         enable: true, context: , keybind: , icon: , help: }
      - {id: docking, label: Docking, type: command ,
         enable: true, context: , keybind: , icon: , help: }

- {id: delete_task, label: Delete Task, type: command ,
   enable: true, context: , keybind: , icon: , help: 'Delete selected task'}

- {id: recent_project, label: Recent Projects, type: submenu ,
   enable: true, context: , keybind: , icon: , help: 'Open recent project'}

"""

EDIT_MENU = """
- {id: undo, label: Undo, type: command ,
   enable: false, context: , keybind: , icon: ,
   help: 'undo'}
- {id: redo, label: Redo, type: command ,
   enable: false, context: , keybind: , icon: ,
   help: 'redo'}
"""

VIEW_MENU = """
- {id: show_project, label: Show Project, type: checkable ,
   enable: true, context: False, keybind: , icon: ,
   help: 'Show project view'}

- {id: show_task_property, label: Show Task Property, type: checkable ,
   enable: true, context: False, keybind: , icon: ,
   help: 'Show Task Property View'}

- {id: show_atom_property, label: Show Atom Property, type: checkable ,
   enable: true, context: False, keybind: , icon: ,
   help: 'Show Atom Property View'}

"""
# work flow


TOOL_MENU = """
"""

WORKFLOW_MENU = """
"""

PLUGIN_MENU = """
"""

HELP_MENU = """
"""

itemid_api_dict = {
    'file:open_molecule'  : 'api.dialog.open_molecule',
    'project:open_project': 'api.dialog.open_project' ,
}
itemid_key_dict = {
    'file:open_molecule'  : 'Ctrl+o',
    'project:open_project': 'Ctrl+p',
}

class MenubarModel(object):

    def __init__(self):

        # define properties
        self.__nagara_menu_list = []
        self.__nagara_menu_list.append(('Nagara'  , yaml.load(NAGARA_MENU) )  )
        self.__nagara_menu_list.append(('File'    , yaml.load(FILE_MENU) )    )
        self.__nagara_menu_list.append(('Edit'    , yaml.load(EDIT_MENU) )    )
        self.__nagara_menu_list.append(('Project' , yaml.load(PROJECT_MENU) ) )
        self.__nagara_menu_list.append(('View'    , yaml.load(VIEW_MENU) )    )
        self.__nagara_menu_list.append(('Workflow', yaml.load(WORKFLOW_MENU) ))
        self.__nagara_menu_list.append(('Plugin'  , yaml.load(PLUGIN_MENU) )  )
        self.__nagara_menu_list.append(('Help'    , yaml.load(HELP_MENU) )    )

        self.__itemid_menu_dict = {}
        for menu_label, menu in self.__nagara_menu_list:
            if not menu: continue
            for item in menu:
                id = item['id']
                item_id = menu_label + ':' + id
                self.__itemid_menu_dict[item_id] = item

        self.__api_dict = itemid_api_dict

        # events to menubar_view
        self.__init_event            = NagaraEvent()
        self.__update_menu_event     = NagaraEvent()
        self.__update_item_event     = NagaraEvent()
        self.__update_plugin_event   = NagaraEvent()

        # events to api
        self.__showhelp_event        = NagaraEvent()

    # events to menubar_view
    @property
    def init_event(self):
        return self.__init_event

    @property
    def update_menu_event(self):
        return self.__update_menu_event

    @property
    def update_item_event(self):
        return self.__update_item_event

    @property
    def update_plugin_event(self):
        return self.__update_plugin_event

    # events to api
    def showhelp_event(self):
        return self.__showhelp_event

    # methods
    def init(self):
        self.init_event.fire()
        
    def get_menu_list(self):
        return self.__nagara_menu_list

    def get_menu(self, menu_label):
        for ml, menu in self.get_menu_list():
            if ml == menu_label:
                ret = menu
                break
        return menu

    def get_item(self, item_id):
        return self.__itemid_menu_dict[item_id]

    def set_project(self, project_id):
        pass

    def set_file(self, file_id):
        pass

    def set_help_word(self, help_word):
        self.__dynamic_config.help_word_history.append(help_word)
        self.__api.show_help(help_word)
        self.showhelp_event.fire()

    def request_api(self, item_id):
        print item_id
        # self.__api_dict[id].do()


if __name__ == '__main__':
    m = MenubarModel()
    # for label, menu in m.get_menu_list():
    #     print label
    #     if not menu: continue

    #     for item in menu:
    #         print item
    print m.get_item('View:show_atom_property')

