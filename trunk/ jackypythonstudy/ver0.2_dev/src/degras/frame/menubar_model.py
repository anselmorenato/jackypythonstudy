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



# VIEW_MENU = """
# - {id: show_project, label: Show Project, type: checkable ,
   # enable: true, context: False, keybind: , icon: ,
   # help: 'Show project view'}

# - {id: show_task_property, label: Show Task Property, type: checkable ,
   # enable: true, context: False, keybind: , icon: ,
   # help: 'Show Task Property View'}

# - {id: show_atom_property, label: Show Atom Property, type: checkable ,
   # enable: true, context: False, keybind: , icon: ,
   # help: 'Show Atom Property View'}

# """
# work flow

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

