#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Biao Ma and Takakazu Ishikura
import os, sys
import wx
import wx.gizmos

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from utils.event import NagaraEvent
from core.exception import NagaraException, DialogCancelException


class CtrlNotFoundError(NagaraException): pass

ArtIDs = [ "None",
           "wx.ART_ADD_BOOKMARK",
           "wx.ART_DEL_BOOKMARK",
           "wx.ART_HELP_SIDE_PANEL",
           "wx.ART_HELP_SETTINGS",
           "wx.ART_HELP_BOOK",
           "wx.ART_HELP_FOLDER",
           "wx.ART_HELP_PAGE",
           "wx.ART_GO_BACK",
           "wx.ART_GO_FORWARD",
           "wx.ART_GO_UP",
           "wx.ART_GO_DOWN",
           "wx.ART_GO_TO_PARENT",
           "wx.ART_GO_HOME",
           "wx.ART_FILE_OPEN",
           "wx.ART_PRINT",
           "wx.ART_HELP",
           "wx.ART_TIP",
           "wx.ART_REPORT_VIEW",
           "wx.ART_LIST_VIEW",
           "wx.ART_NEW_DIR",
           "wx.ART_HARDDISK",
           "wx.ART_FLOPPY",
           "wx.ART_CDROM",
           "wx.ART_REMOVABLE",
           "wx.ART_FOLDER",
           "wx.ART_FOLDER_OPEN",
           "wx.ART_GO_DIR_UP",
           "wx.ART_EXECUTABLE_FILE",
           "wx.ART_NORMAL_FILE",
           "wx.ART_TICK_MARK",
           "wx.ART_CROSS_MARK",
           "wx.ART_ERROR",
           "wx.ART_QUESTION",
           "wx.ART_WARNING",
           "wx.ART_INFORMATION",
           "wx.ART_MISSING_IMAGE",
           "SmileBitmap"
           ]


#from wx.lib.mixins.listctrl import CheckListCtrlMixin
#class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin):

    #def __init__(self, parent):
        #wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
        #CheckListCtrlMixin.__init__(self)

    ## this is called by the base class when an item is checked/unchecked
    #def OnCheckItem(self, index, flag):
        #data = self.GetItemData(index)
        #title = musicdata[data][1]
        #if flag:
            #what = "checked"
        #else:
            #what = "unchecked"
        #self.log.write('item "%s", at index %d was %s\n' % (title, index, what))

#===============================================================================


from  utils.wxutils import BindManager
class LocationManagerInteractor(object):

    binder = BindManager()

    def __init__(self, view, presenter):

        self.presen = presenter
        self.binder.bindAll(view, self)

    # for loc list
    @binder(wx.EVT_LISTBOX, 'ID_loc_list')
    def h1(self, event):
        self.presen.select()

    @binder(wx.EVT_LISTBOX_DCLICK, 'ID_loc_list')
    def h2(self, event):
        self.presen.edit()

    @binder(wx.EVT_RIGHT_UP, 'ID_loc_list')
    def h3(self, event):
        self.presen.popup()
    
    # for popup menu
    @binder(wx.EVT_MENU, id='ID_new_menu')
    def h4(self, event):
        self.presen.create()

    @binder(wx.EVT_MENU, id='ID_edit_menu')
    def h5(self, event):
        self.presen.edit()

    @binder(wx.EVT_MENU, id='ID_copy_menu')
    def h6(self, event):
        self.presen.copy()

    @binder(wx.EVT_MENU, id='ID_del_menu')
    def h7(self, event):
        self.presen.delete()

    # for edit buttons
    @binder(wx.EVT_BUTTON, 'ID_new_button')
    def h8(self, event):
        self.presen.create()

    @binder(wx.EVT_BUTTON, 'ID_edit_button')
    def h9(self, event):
        self.presen.edit()

    @binder(wx.EVT_BUTTON, 'ID_copy_button')
    def h10(self, event):
        self.presen.copy()

    @binder(wx.EVT_BUTTON, 'ID_del_button')
    def h11(self, event):
        self.presen.delete()

    # for choice
    @binder(wx.EVT_CHOICE, 'ID_default_choice')
    def h12(self, event):
        self.presen.setDefault()

    # for close
    @binder(wx.EVT_BUTTON, 'ID_close_button')
    def h13(self, event):
        self.presen.close()


# from interfaces.ilocationmanager_view import ILocationManagerView
# class LocationManagerView(ILocationManagerView, wx.Panel):
class LocationManagerView(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.__idctrl_dict = {}

        # create views
        # create location list
        loc_sizer = self.__create_location_list()
        # create buttons
        btn_sizer = self.__create_buttons()
        # create location viewer
        locview_sizer = self.__create_location_viewer()
        # create close button
        other_sizer = self.__create_close_button()

        # do layout
        panel_sizer  = wx.BoxSizer(wx.VERTICAL)

        split_sizer  = wx.BoxSizer(wx.HORIZONTAL)
        split_sizer.Add(loc_sizer, 0, wx.EXPAND, 5)
        split_sizer.Add(btn_sizer, 0, wx.EXPAND|wx.ALL, 5)

        panel_sizer.Add(split_sizer, 0, wx.ALIGN_CENTER, 5)
        line = wx.StaticLine(self, -1 )
        panel_sizer.Add(line, 0, wx.TOP|wx.BOTTOM|wx.EXPAND, 10)
        panel_sizer.Add(locview_sizer, 3, wx.EXPAND)
        panel_sizer.Add(other_sizer, 0, wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT)
        
        self.SetSizer(panel_sizer)
        self.SetAutoLayout(True)
        panel_sizer.Fit(self.GetParent())
        #panel_sizer.SetSizeHints(self)

    def getCtrl(self, ctrl_name):
        ctrl = self.FindWindowByName(ctrl_name)
        if not ctrl:
            raise CtrlNotFoundError(ctrl_name)
        return ctrl

    def getCtrlById(self, id_ctrl_name):
        id_ctrl = self.__idctrl_dict.get(id_ctrl_name)
        if not id_ctrl:
            raise CtrlNotFoundError(id_ctrl_name)
        return id_ctrl

    def getCtrlNames(self):
        for ctrl in self.GetChildren():
            if ctrl.GetName().startswith('ID_'):
                yield ctrl.GetName()

        for menuitem in self.__menu.GetMenuItems():
            print menuitem.GetLabel()

    def getCtrlIdList(self):
        return self.__idctrl_dict.keys()

    def __create_location_list(self):

        # create
        list_sizer = wx.StaticBoxSizer(
            wx.StaticBox(self, -1, 'Location list'), orient=wx.VERTICAL)
        self.__loc_list = wx.ListBox(
            self, size = (130,50),choices=[], name='ID_loc_list')
        # self.__loc_list.SetSelection(0)
        self.__loc_list.SetFont(wx.Font(11,wx.SWISS,wx.NORMAL,wx.NORMAL))


        # add layout
        list_sizer.Add(self.__loc_list, 1, wx.EXPAND, 5)

        # make a menu
        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        self.__idctrl_dict = {}
        self.__menu = wx.Menu()
        self.__idctrl_dict['ID_new_menu']  = id_new  = wx.NewId()
        self.__idctrl_dict['ID_edit_menu'] = id_edit = wx.NewId()
        self.__idctrl_dict['ID_copy_menu'] = id_copy = wx.NewId()
        self.__idctrl_dict['ID_del_menu']  = id_del  = wx.NewId()
        self.__menu.Append(id_new  , "New"    ) 
        self.__menu.Append(id_edit , "Edit"   ) 
        self.__menu.Append(id_copy , "Copy"   ) 
        self.__menu.Append(id_del  , "Delete" ) 

        # create default choice control
        default_text = wx.StaticText(self, -1, 'default :')
        self.__choice = wx.Choice(self, -1, choices=[],name='ID_default_choice')
        #self.__choice = wx.Choice(self, -1, pos=(20,10), choices=[])

        default_sizer  = wx.BoxSizer(wx.HORIZONTAL)
        default_sizer.Add(default_text, 0, wx.ALL|wx.EXPAND, 2)
        default_sizer.Add(self.__choice, 0, wx.ALL|wx.FIXED_MINSIZE, 2)
        #list_sizer.Add(default_sizer, 2, wx.ALL|wx.EXPAND, 5)
        list_sizer.Add(default_sizer, 0, wx.ALL|wx.FIXED_MINSIZE, 5)

        return list_sizer

    #def __create_location_list2(self):

       #self.__loc_list.InsertColumn(0, "default")
       #self.__loc_list.InsertColumn(1, "location name", wx.LIST_FORMAT_RIGHT)

    def __create_buttons(self):
        # create the edit button
        btn_sizer = wx.StaticBoxSizer(
            wx.StaticBox(self, -1, 'edit button'), orient=wx.VERTICAL)

        # create
        new_btn  = wx.Button(self, -1, "New"   , name='ID_new_button' ) 
        edit_btn = wx.Button(self, -1, "Edit"  , name='ID_edit_button') 
        copy_btn = wx.Button(self, -1, "Copy"  , name='ID_copy_button') 
        del_btn  = wx.Button(self, -1, "Delete", name='ID_del_button' ) 
        new_btn.SetSize(  new_btn.GetBestSize()  ) 
        edit_btn.SetSize( edit_btn.GetBestSize() ) 
        copy_btn.SetSize( copy_btn.GetBestSize() ) 
        del_btn.SetSize(  del_btn.GetBestSize()  ) 

        # do layout
        btn_sizer.Add(new_btn , 1, wx.EXPAND|wx.ALL, 3) 
        btn_sizer.Add(edit_btn, 1, wx.EXPAND|wx.ALL, 3) 
        btn_sizer.Add(copy_btn, 1, wx.EXPAND|wx.ALL, 3) 
        btn_sizer.Add(del_btn , 1, wx.EXPAND|wx.ALL, 3) 
        btn_sizer.Add( (100, -1) )

        return btn_sizer

    def __create_location_viewer(self):

        locview_sizer = wx.StaticBoxSizer(
            wx.StaticBox(self, -1, 'configure view'), orient=wx.VERTICAL)

        # Create the tree
        self.__loc_tree = wx.gizmos.TreeListCtrl(
            self, style = wx.TR_DEFAULT_STYLE
            #| wx.TR_HAS_BUTTONS
            #| wx.TR_TWIST_BUTTONS
            #| wx.TR_ROW_LINES
            #| wx.TR_COLUMN_LINES
            #| wx.TR_NO_LINES 
            | wx.TR_FULL_ROW_HIGHLIGHT
        )
        locview_sizer.Add(self.__loc_tree, 1, wx.EXPAND, 5)

        # create some columns
        self.__loc_tree.AddColumn("keyword")
        self.__loc_tree.AddColumn("value")
        self.__loc_tree.SetMainColumn(0) # the one with the tree in it...
        self.__loc_tree.SetColumnWidth(0, 150)
        self.__loc_tree.SetColumnWidth(1, 200)

        return locview_sizer

    def __create_close_button(self):
        close_button = wx.Button(self, -1, "Close", name='ID_close_button')

        # The other_sizer has two button
        other_sizer = wx.BoxSizer(wx.HORIZONTAL)
        other_sizer.Add(close_button, 0, wx.ALIGN_RIGHT)
        #other_sizer.Add(self.cancelBtn,0,wx.ALIGN_RIGHT)

        return other_sizer

    # methods
    def init(self):
        pass

    def clearDefault(self):
        self.__choice.Clear()

    def clearList(self):
        self.__loc_list.Clear()

    def clearTreeView(self):
        self.__loc_tree.DeleteAllItems()

    def appendToLocation(self, locname):
        count = self.__loc_list.GetCount()
        self.__loc_list.Insert(locname, count)

    def appendToDefault(self, locname):
        self.__choice.Append(locname)

    def close(self):
        pass

    # getset: default
    def getDefault(self):
        return self.__choice.GetStringSelection()
    def setDefault(self, default_locname):
        self.__choice.SetStringSelection(default_locname)
    default = property(getDefault, setDefault)

    def getNameDialog(self, name):
        return NewNameDialog(name)

    def getSelected(self):
        return self.__loc_list.GetStringSelection()

    # for config tree view
    def showConfig(self, config):
        self.__loc_tree.DeleteAllItems()
        locname = config['name']
        root = self.__loc_tree.AddRoot(locname)
        self.__add_tree_nodes(root, config)
        self.__loc_tree.ExpandAll(self.__loc_tree.GetRootItem())

    def __add_tree_nodes(self, parent_item, config):
        for key, val in config.items():

            if isinstance(val, dict):
                item = self.__loc_tree.AppendItem(parent_item, key)
                self.__add_tree_nodes(item, val)

            else:
                item = self.__loc_tree.AppendItem(parent_item, key)
                self.__loc_tree.SetItemText(item, val, 1)

    def popupMenu(self):
        self.__loc_list.PopupMenu(self.__menu)

    def enable(self, ctrl_id, enable):
        self.getCtrl(ctrl_id).Enable( enable )


########################################################################
class NewNameDialog(wx.Dialog):

    #----------------------------------------------------------------------
    def __init__(self, name='new location', pos=(100,100)):
        pos = wx.GetMousePosition()
        wx.Dialog.__init__(self, None, -1, pos=pos, size=(300,80))

        # create form
        form_sizer = self.__create_forms()
        self.__name_form.SetValue( str(name) )
        self.__name_form.SelectAll()

        # create buttons
        btn_sizer = self.__create_buttons()

        # do layout
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(form_sizer , 0 , wx.EXPAND|wx.ALL , 5 ) 
        main_sizer.Add(btn_sizer  , 0 , wx.ALIGN_RIGHT   , 5 ) 
        self.SetSizer(main_sizer)
        self.SetAutoLayout(True)

    def __create_forms(self):
        # create view
        name_label = wx.StaticText(self, -1, "Location Name: ")
        self.__name_form  = wx.TextCtrl(self, -1, "")

        # sizer
        form_sizer = wx.BoxSizer(wx.HORIZONTAL)
        form_sizer.Add(name_label, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(self.__name_form , 1, wx.EXPAND)

        return form_sizer

    def __create_buttons(self):

        # create view
        ok_btn     = wx.Button(self , wx.ID_OK     , "Ok"     ) 
        cancel_btn = wx.Button(self , wx.ID_CANCEL , "Cancel" ) 

        # sizer
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add(ok_btn     , 0 , wx.ALIGN_RIGHT , 5 ) 
        btn_sizer.Add(cancel_btn , 0 , wx.ALIGN_RIGHT , 5 ) 

        return btn_sizer

    def __enter__(self):
        self.__flag = self.ShowModal()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.Destroy()
        return True

    def getName(self):
        if self.__flag == wx.ID_CANCEL:
            self.throwException()
        return self.__name_form.GetValue()


if __name__ == '__main__':

    app = wx.App(redirect=False)
    frame = wx.Frame(None, -1, 'Location Manager View')
    lmv = LocationManagerView(frame)

    # print lmv.GetChildren()
    print lmv.getCtrl('ID_new_button').GetName()
    print list(lmv.getCtrlNames())

    frame.Show()

    config = dict(
        name = 'hoge',
        test = '',
        fuga = '999',
        ddd  = dict(
            hoge1 = 'fuga1',
            hoge2 = 'fuga2',
            hoge3 = 'fuga3',
        ),
        test2 = 'test2',
    )

    config2 = dict(
        name = 'name2',
        test = 'unnunn',
        fuga = '50',
        ddd  = dict(
            hoge1 = 'doc1',
            hoge2 = 'doc2',
            hoge3 = 'doc3',
        ),
        test2 = 'tttt2',
    )

    lmv.showConfig(config)
    loclist = ['vlsn', 'hpcs', 'test loc']


    import time
    import threading
    
    def wait1(interval):
        time.sleep(interval)
        loclist = ['a', 'b', 'c loc']
        lmv.setLocationList(loclist)
        #mv.__create_location_list()

    def wait2(interval):
        time.sleep(interval)
        lmv.setDefault('c loc')

    def wait3(interval):
        time.sleep(interval)
        lmv.setDefault('c loc')
        lmv.showConfig(config2)

    t1 = threading.Thread(name=None, target=wait1, args=[1])
    t2 = threading.Thread(name=None, target=wait2, args=[2])
    t3 = threading.Thread(name=None, target=wait3, args=[3])

    t1.start()
    t2.start()
    t3.start()


    app.MainLoop()
