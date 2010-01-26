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


class MenubarView(wx.MenuBar):

    def __init__(self):
        """Constructor."""
        wx.MenuBar.__init__(self)

        # define dict
        self.item_dict = {}

        nagara_menu = self.init_nagara_menu()
        self.Append(nagara_menu, 'Nagara')

        file_menu = self.init_file_menu()
        self.Append(file_menu, 'File')

        edit_menu = self.init_edit_menu()
        self.Append(edit_menu, 'Edit')

        project_menu = self.init_project_menu()
        self.Append(project_menu, 'Project')

        view_menu = self.init_view_menu()
        self.Append(view_menu, 'View')

        tool_menu = self.init_tool_menu()
        self.Append(tool_menu, 'Tool')

        workflow_menu = self.init_workflow_menu()
        self.Append(workflow_menu, 'Workflow')

        plugin_menu = self.init_plugin_menu()
        self.Append(plugin_menu, 'Plugin')


    def is_enabled(self, itempath):
        id, item = self.get_item(itempath)
        return item.IsEnabled()

    def enable(self, itempath, enable=True):
        id, item = self.get_item(itempath)
        item.Enable(enable)

    def check(self, itempath, check=True):
        id, item = self.get_item(itempath)
        item.Check(enable)

    def is_checked(self, itempath):
        id, item = self.get_item(itempath)
        return item.IsChecked()

    def get_item(self, item):
        return self.item_dict.get(itempath)

    def get_menu(self, menulabel):
        for menu, label in self.GetMenus():
            if menulabel == label:
                ret = menu
                break
        else:
            raise NotFoundMenuError(menulabel)
        return ret

    def init_nagara_menu(self):
        menu = wx.Menu()

        # about nagara
        id = wx.NewId()
        menuitem = wx.MenuItem(
            menu, id, 'About NAGARA',
            'About NAGARA', wx.ITEM_NORMAL)
        menu.AppendItem(menuitem)
        self.item_dict['nagara:about_nagara'] = (id, menuitem)

        # separator
        menu.AppendSeparator()

        # check update
        id = wx.NewId()
        menuitem = wx.MenuItem(
            menu, id, 'Check Update',
            'Check Update', wx.ITEM_NORMAL)
        menu.AppendItem(menuitem)
        self.item_dict['nagara:check_update'] = (id, menuitem)

        # quit
        id = wx.NewId()
        menuitem = wx.MenuItem(
            menu, id, 'Quit',
            'Quit NAGARA', wx.ITEM_NORMAL)
        menu.AppendItem(menuitem)
        self.item_dict['nagara:quit'] = (id, menuitem)

        return menu


    def init_file_menu(self):
        menu = wx.Menu()

        # open molecule
        id = wx.NewId()
        menuitem = wx.MenuItem(
            menu, id, 'Open Molecule',
            'Open Molecule', wx.ITEM_NORMAL)
        menu.AppendItem(menuitem)
        self.item_dict['file:open_molecule'] = (id, menuitem)

        # open data
        id = wx.NewId()
        menuitem = wx.MenuItem(
            menu, id, 'Open Data',
            'Open Data', wx.ITEM_NORMAL)
        menu.AppendItem(menuitem)
        self.item_dict['file:open_data'] = (id, menuitem)

        return menu

    def init_project_menu(self):
        menu = wx.Menu()

        # add task submeu
        taskmenu = self.init_task_menu()
        menu.AppendMenu(-1, 'Add Task', taskmenu)

        # delete task
        id = wx.NewId()
        menuitem = wx.MenuItem(
            menu, id, 'Delete Task',
            'Delete Task', wx.ITEM_NORMAL)
        menu.AppendItem(menuitem)
        self.item_dict['project:delete_task'] = (id, menuitem)

        # recent project
        taskmenu = wx.Menu()
        menuitem = wx.MenuItem(
            menu, id, 'Recent Project',
            'Recent Project', wx.ITEM_NORMAL)
        menu.AppendItem(menuitem)
        self.item_dict['project:recent_project'] = (id, menuitem)

        return menu

    def init_task_menu(self):
        menu = wx.Menu()

        # energy
        id = wx.NewId()
        menuitem = wx.MenuItem(
            menu, id, 'Energy',
            'Energy', wx.ITEM_NORMAL)
        menu.AppendItem(menuitem)
        self.item_dict['project:add_task:energy'] = (id, menuitem)

        # optimize
        id = wx.NewId()
        menuitem = wx.MenuItem(
            menu, id, 'Optimize',
            'Optimize', wx.ITEM_NORMAL)
        menu.AppendItem(menuitem)
        self.item_dict['project:add_task:optimize'] = (id, menuitem)

        # Dynamics
        id = wx.NewId()
        menuitem = wx.MenuItem(
            menu, id, 'Dynamics',
            'Dynamics', wx.ITEM_NORMAL)
        menu.AppendItem(menuitem)
        self.item_dict['project:add_task:dynamics'] = (id, menuitem)

        # Docking
        id = wx.NewId()
        menuitem = wx.MenuItem(
            menu, id, 'Docking',
            'Docking', wx.ITEM_NORMAL)
        menu.AppendItem(menuitem)
        self.item_dict['project:add_task:docking'] = (id, menuitem)

        return menu
    
    def init_wf_task_menu(self):
        menu = wx.Menu()

        # energy
        id = wx.NewId()
        menuitem = wx.MenuItem(
            menu, id, 'Energy',
            'Energy', wx.ITEM_NORMAL)
        menu.AppendItem(menuitem)
        self.item_dict['workflow:add_task:energy'] = (id, menuitem)

        # optimize
        id = wx.NewId()
        menuitem = wx.MenuItem(
            menu, id, 'Optimize',
            'Optimize', wx.ITEM_NORMAL)
        menu.AppendItem(menuitem)
        self.item_dict['workflow:add_task:optimize'] = (id, menuitem)

        # Dynamics
        id = wx.NewId()
        menuitem = wx.MenuItem(
            menu, id, 'Dynamics',
            'Dynamics', wx.ITEM_NORMAL)
        menu.AppendItem(menuitem)
        self.item_dict['workflow:add_task:dynamics'] = (id, menuitem)

        # Docking
        id = wx.NewId()
        menuitem = wx.MenuItem(
            menu, id, 'Docking',
            'Docking', wx.ITEM_NORMAL)
        menu.AppendItem(menuitem)
        self.item_dict['workflow:add_task:docking'] = (id, menuitem)

        return menu

    def init_edit_menu(self):
        menu = wx.Menu()

        # undo
        id = wx.NewId()
        menuitem = wx.MenuItem(
            menu, id, 'Undo',
            'Undo', wx.ITEM_NORMAL)
        menu.AppendItem(menuitem)
        self.item_dict['edit:undo'] = (id, menuitem)

        # redo
        id = wx.NewId()
        menuitem = wx.MenuItem(
            menu, id, 'Redo',
            'Redo', wx.ITEM_NORMAL)
        menu.AppendItem(menuitem)
        self.item_dict['edit:redo'] = (id, menuitem)

        return menu

    def init_view_menu(self):
        menu = wx.Menu()

        # show project
        id = wx.NewId()
        menuitem = wx.MenuItem(
            menu, id, 'Show Project',
            'Show Project', wx.ITEM_CHECK)
        menu.AppendItem(menuitem)
        self.item_dict['view:show_project'] = (id, menuitem)

        # show task property
        id = wx.NewId()
        menuitem = wx.MenuItem(
            menu, id, 'Show Task Property',
            'Show Task Property', wx.ITEM_CHECK)
        menu.AppendItem(menuitem)
        self.item_dict['view:show_task_property'] = (id, menuitem)

        # show atom property
        id = wx.NewId()
        menuitem = wx.MenuItem(
            menu, id, 'Show Atom Property',
            'Show Atom Property', wx.ITEM_CHECK)
        menu.AppendItem(menuitem)
        self.item_dict['view:show_atom_property'] = (id, menuitem)

        return menu

    def init_tool_menu(self):
        menu = wx.Menu()
        
        
        return menu

    def init_workflow_menu(self):
        menu = wx.Menu()
        
        # add data
        add_data_id = wx.NewId()
        menuitem = wx.MenuItem(
            menu, add_data_id, 'Add Data', 
            'Add Data', wx.ITEM_NORMAL)
        menu.AppendItem(menuitem)
        self.item_dict['workflow:add_data'] = (add_data_id,menuitem)
        
        # add task submenu
        #add_task_id = wx.NewId()
        taskmenu = self.init_wf_task_menu()
        
        menu.AppendMenu(-1, 'Add Task', taskmenu)
        #self.item_dict['workflow:Add Task'] = (add_task_id,menuitem)
        return menu

    def init_plugin_menu(self):
        menu = wx.Menu()
        return menu

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

    def append_item(self, iteminfo):
        menulabel = iteminfo.get('menu_label')
        menu = self.get_menu( menulabel )

        id      = iteminfo.get('id')
        type    = iteminfo.get('type')
        label   = unicode(iteminfo.get('label'))
        enable  = iteminfo.get('enable')
        context = iteminfo.get('context')
        keybind = iteminfo.get('keybind')
        help    = unicode(iteminfo.get('help'))
        icon    = iteminfo.get('icon')

        if keybind:
            label = label + '\t' + keybind

        if type == 'nothing':
            menuitem = wx.MenuItem( menu, wx.NewId(),
                                   label, help, wx.ITEM_NORMAL)
            menu.AppendItem(menuitem)

        elif type == 'command':
            menuitem = wx.MenuItem( menu, wx.NewId(),
                                   label, help, wx.ITEM_NORMAL)
            menu.AppendItem(menuitem)

        elif type == 'separator':
            menu.AppendSeparator()

        elif type == 'checkable':
            menuitem = wx.MenuItem( menu, wx.NewId(),
                                   label, help, wx.ITEM_CHECK)
            menu.AppendItem(menuitem)
            menu.Check(wx.NewId(), context)

        elif type == 'radio':
            menuitem = wx.MenuItem( menu, wx.NewId(),
                                   label, help, wx.ITEM_RADIO)
            menu.AppendItem(menuitem)
            menu.Check(wx.NewId(), context)

        elif type == 'submenu': # sub menu item will be created
            submenu = wx.Menu()

            item_id = menu.label + ':' + id
            self.__itemid_dict[submenu_id] = item_id
            submenu.label = id 
            self.__append_item_list(submenu, context)
            menu.AppendMenu(submenu_id, label, submenu, help)

        else:
            raise InvalidMenuTypeError()

        item_id = menu.label + ':' + id

        menuitem.Enable(enable)
        if icon: menuitem.SetBitmap( wx.Bitmap(icon) )

        self.menuitem_dict[item_id] = menuitem





        # for item_path, menuitem in self.menuitem_dict.items():
            # menu_and_item = item_path.split(:)

            # handler = bind_table.get(item_path)
            # if handler:
                # lambda event: getattr(self.presenter, 'handler')

            # if len(menu_and_item) == 2:
                # menulabel, itemid = menu_and_item
                # menu = self.view.get_menu(menulabel)

                # menu.Bind(wx.EVT_MENU, 
                          # lambda event: getattr(self.presenter, handler)
                         # )

            # elif len(menu_and_item) == 3:
                # menulabel, submenulabel, itemid = menu_and_item
                # submenu = self.view.get_menu(submenulabel)
                # submenu.Bind(wx.EVT_MENU,
                             # lambda event: getattr(self.presenter, handler)
                            # )

            # else:
                # pass # Error



            # itemlabel = item_id.split(':')[-1]



    # def append_item(self, iteminfo):
        # menulabel = iteminfo.get('menu_label')
        # menu = self.get_menu( menulabel )

        # type = iteminfo.get('type')
        # menuitem = wx.MenuItem(
            # menu, wx.NewId(),
            # unicode( iteminfo.get('label') ),
            # iteminfo.get('help'),
            # self.get_kind(type),
        # )
            # elif type == 'separator':
                # menu.AppendSeparator()

        # if iteminfo.get('type'):
            # menuitem.SetKind(wx.RA

            # if type == 'nothing':
                # menuitem_id = wx.NewId()
                # menuitem = wx.MenuItem(
                    # menu, menuitem_id, label, help, wx.ITEM_NORMAL)
                # menu.AppendItem(menuitem)

            # elif type == 'command':
                # menuitem_id = wx.NewId()
                # menuitem = wx.MenuItem(
                    # menu, menuitem_id, label, help, wx.ITEM_NORMAL)
                # menu.AppendItem(menuitem)

            # elif type == 'separator':
                # menu.AppendSeparator()

            # elif type == 'checkable':
                # menuitem_id = wx.NewId()
                # menuitem = wx.MenuItem(
                    # menu, menuitem_id, label, help, wx.ITEM_CHECK)
                # menu.AppendItem(menuitem)
                # menu.Check(menuitem_id, context)

            # elif type == 'radio':
                # menuitem_id = wx.NewId()
                # menuitem = wx.MenuItem(
                    # menu, menuitem_id, label, help, wx.ITEM_RADIO)
                # menu.AppendItem(menuitem)
                # menu.Check(menuitem_id, context)

            # elif type == 'submenu': # sub menu item will be created
                # submenu_id = wx.NewId()
                # submenu = wx.Menu()

                # item_id = menu.label + ':' + id
                # self.__itemid_dict[submenu_id] = item_id
                # submenu.label = id 
                # self.__append_item_list(submenu, context)
                # menu.AppendMenu(submenu_id, label, submenu, help)


        # menuitem.Enable(iteminfo.get('enable'))
        # menuitem.Check(iteminfo.get('context'))

                    # , help, wx.ITEM_RADIO)

            # id      = item.get('id')
            # type    = item.get('type')
            # label   = unicode(item.get('label'))
            # enable  = item.get('enable')
            # context = item.get('context')
            # keybind = item.get('keybind')
            # help    = unicode(item.get('help'))
            # icon    = item.get('icon')

        # menuitem = wx.MenuItem(menu, wx.NewId(), 

            # menu, 

    # def get_type(self, type):
        # return dict(
            # nothing = wx.NORMAL,
            # command = 
            # separator= wx.
            # checkable
            # radio
            # submenu

            # checkable, 



        


            # elif type == 'radio':
                # menuitem_id = wx.NewId()
                # menuitem = wx.MenuItem(
                    # menu, menuitem_id, label, help, wx.ITEM_RADIO)
                # menu.AppendItem(menuitem)
                # menu.Check(menuitem_id, context)


if __name__ == '__main__':
    app = wx.App(redirect=False)
    v = MenubarView()
