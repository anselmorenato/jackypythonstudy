#! /opt/python2.6/bin/python
#  -*- encoding: utf-8 -*-
# Copyright (C)  2009 Takakazu Ishikura

# standard modules
import os, sys
from abc import ABCMeta, abstractmethod, abstractproperty
import wx

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from core.exception import NagaraException
from utils.event    import NagaraEvent
from core.log       import Log


# exceptions
class MenuException(NagaraException): pass
class InvalidMenuTypeError(MenuException): pass
class NotFoundMenuError(MenuException): pass


class MenubarView(wx.MenuBar):

    def __init__(self, frame):
        """Constructor."""
        wx.MenuBar.__init__(self)
        self.__frame = frame

        # define dict
        self.__menuitem_dict = {}
        self.__itemid_dict = {}

        # generate events
        self.__run_api_event        = NagaraEvent()
        self.__search_help_event    = NagaraEvent()
        self.__recent_project_event = NagaraEvent()
        self.__recent_file_event    = NagaraEvent()

        # bind wx event handler
        self.__frame.Bind(wx.EVT_MENU, self.on_menuitem)

    # events
    @property
    def run_api_event(self):
        return self.__run_api_event

    @property
    def search_help_event(self):
        return self.__search_help_event

    @property
    def recent_project_event(self):
        return self.__recent_project_event
    
    @property
    def recent_file_event(self):
        return self.__recent_file_event

    # wx event handlers
    def on_menuitem(self, event):
        Log( 'in on_menuitem: ' + self.get_itemid_by_miid( event.GetId() ) )
        menuitem_id = event.GetId()
        item_id = self.get_itemid_by_miid( menuitem_id )

        ids = item_id.split(':')
        if ids[1] == 'search_help':
            help_word = self.GetHelpString(menuitem_id)
            self.search_help_event.fire(help_word)

        elif ids[1] == 'recent_project':
            self.recent_project_event.fire(item_id)

        elif ids[1] == 'recent_file':
            self.recent_file_event.fire(item_id)

        else:
            self.run_api_event.fire( item_id )

    def on_menuitem_old(self, event):
        Log('in on_menuitem: ' + str(event.GetId()) )
        menuitem_id = event.GetId()
        item_id = self.__itemid_dict.get(menuitem_id)
        if item_id: self.run_api_event.fire( item_id )

    # methods
    def init_menubar(self, *menu_list):
        for menu_label, item_list in menu_list:
            if menu_label == 'Help':
                self.__init_help_menu(item_list)
            elif menu_label == 'Plugin':
                self.__init_plugin_menu(item_list)
            else:
                self.__init_menu_any(menu_label, item_list)

        # for i in range(101, 115):
        #     self.Bind(wx.EVT_MENU, self.on_menuitem, id=i)

    def update_menu(self, menu_label, item_list):
        menu = self.get_menu(menu_label)

        if menu_label not in ['Plugin', 'Help']:
            for menu_item in menu.GetMenuItems():
                menu.RemoveItem(menu_item)

            self.__append_item_list(menu, item_list)
            menu.UpdataUI()

    def update_menuitem(self, item_id, item):
        menuitem = self.get_menuitem_by_itemid(item_id)
        menuitem.SetItemLabel( item['label'] )
        menuitem.Enable( item['enable'] )
        menuitem.SetAccel( item['keybind'] )
        menuitem.SetHelp( item['help'] )
        if item['icon']: menuitem.SetBitmap( wx.Bitmap(item['icon']) )

        if item['type'] == 'submenu':
            self.__append_item_list( menuitem, item['context'] ) 
        
        menu_label = item_id.split(':')[0]
        menu = self.get_menu(menu_label)
        menu.UpdataUI()

    def set_plugin_menu(self):
        pass

    def set_help_menu(self):
        pass

    def get_menu(self, menu_label):
        for menu, label in self.GetMenus():
            if menu_label == label:
                ret = menu
                break
        else:
            raise NotFoundMenuError(label)
        return ret

    def get_menuitem_by_id(self, id):
        return self.FindItemById(id)

    def get_itemid_by_miid(self, id):
        return self.__itemid_dict.get(id)

    def get_menuitem_by_itemid(self, item_id):
        return self.__menuitem_dict[item_id] 

    def __init_menu_any(self, menu_label, item_list):
        # menu = wx.Menu(menu_label)
        menu = wx.Menu()
        menu.label = menu_label
        self.Append(menu, menu_label)
        # self.__menu_dict[menu_label] = menu
        self.__append_item_list(menu, item_list)

    def __init_plugin_menu(self, item_list):
        menu = wx.Menu()
        menu.label = 'Plugin'
        self.Append(menu, 'Plugin')
        # self.__menu_dict['Plugin'] = menu
        self.__append_item_list(menu, item_list)

    def __init_help_menu(self, item_list):
        menu = wx.Menu()
        menu.label = 'Help'
        self.Append(menu, 'Help')
        # self.__menu_dict['Help'] = menu
        self.__append_item_list(menu, item_list)

    def __append_item_list(self, menu, item_list):
        menuitem_id = -1
        print menu.label
        
        if not item_list: return None

        for item in item_list:
            id      = item.get('id')
            type    = item.get('type')
            label   = unicode(item.get('label'))
            enable  = item.get('enable')
            context = item.get('context')
            keybind = item.get('keybind')
            help    = unicode(item.get('help'))
            icon    = item.get('icon')

            if keybind:
                label = label + '\t' + keybind

            if type == 'nothing':
                menuitem_id = wx.NewId()
                menuitem = wx.MenuItem(
                    menu, menuitem_id, label, help, wx.ITEM_NORMAL)
                menu.AppendItem(menuitem)

            elif type == 'command':
                menuitem_id = wx.NewId()
                menuitem = wx.MenuItem(
                    menu, menuitem_id, label, help, wx.ITEM_NORMAL)
                menu.AppendItem(menuitem)

            elif type == 'separator':
                menu.AppendSeparator()

            elif type == 'checkable':
                menuitem_id = wx.NewId()
                menuitem = wx.MenuItem(
                    menu, menuitem_id, label, help, wx.ITEM_CHECK)
                menu.AppendItem(menuitem)
                menu.Check(menuitem_id, context)

            elif type == 'radio':
                menuitem_id = wx.NewId()
                menuitem = wx.MenuItem(
                    menu, menuitem_id, label, help, wx.ITEM_RADIO)
                menu.AppendItem(menuitem)
                menu.Check(menuitem_id, context)

            elif type == 'submenu': # sub menu item will be created
                submenu_id = wx.NewId()
                submenu = wx.Menu()

                item_id = menu.label + ':' + id
                self.__itemid_dict[submenu_id] = item_id
                submenu.label = id 
                self.__append_item_list(submenu, context)
                menu.AppendMenu(submenu_id, label, submenu, help)

            else:
                raise InvalidMenuTypeError()
            
            # store menu item and relationship between menuitem id and item id
            if menuitem_id == -1: continue

            item_id = menu.label + ':' + id

            menuitem.Enable(enable)
            self.__menuitem_dict[item_id] = menuitem
            self.__itemid_dict[menuitem_id] = item_id

            if icon: menuitem.SetBitmap( wx.Bitmap(icon) )
