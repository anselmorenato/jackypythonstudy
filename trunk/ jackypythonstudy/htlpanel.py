import wx

import wx.lib.agw.hypertreelist as HTL

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
########################################################################
class HyperTreeListPanel(wx.Panel):
    """This is a HyperTreeListPanel"""
       
    #----------------------------------------------------------------------
    def __init__(self,parent):
        """Constructor"""   
        wx.Panel.__init__(self,parent,-1)
        sizer = wx.BoxSizer(wx.VERTICAL)
        # Create the HyperTreeList
        tree = HyperTreeList(self,-1)
        
        sizer.Add(tree,1,wx.EXPAND)
        self.SetSizer(sizer)
        sizer.Layout()
        
        
class HyperTreeList(HTL.HyperTreeList):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 style=wx.SUNKEN_BORDER | wx.TR_HAS_BUTTONS | wx.TR_HAS_VARIABLE_ROW_HEIGHT,
                 log=None):

        HTL.HyperTreeList.__init__(self, parent, id, pos, size, style)
        self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
        alldata = dir(HTL)
        
        remote_configs = dict(
            email = 'ishikura@gifu-u.ac.jp',
            local = dict(
                ssh = {},
                rootdir = 'C:\path\to\nagara-root',
                workdir = '',
                jms = dict(
                    Single = dict(
                        envs = {},
                        path = {},
                    ),
                    MultiProcess = dict(
                    ),
                ),
                commands = {},
            ),
            hpcs = dict(
                ssh = dict(
                    address = '133.66.117.139',
                    user = 'ishikura',
                    passwd = '*********',
                    port = 22,
                ),
                rootdir = '/home/ishikura/Nagara/projects',
                workdir = '/work/ishikura',
                # jms = ['Single', 'MPI', 'LSF'], #Local
                jms = dict(
                    Single = dict(
                        envs = {},
                        path = {},
                    ),
                    MPI = dict(
                        envs = {},
                        path = {},
                    ),
                    LSF = dict(
                        envs = {},
                        path = {},
                        script = {},
                    ),
                ),
                commands = dict(
                    amber = dict(
                        # envs = dict(AMBERHOME = '/home/hpc/opt/amber10.eth'),
                        # path = '/home/hpcs/opt/amber10.eth/exe/sander.MPI',
                        envs = dict(AMBERHOME = '/home/ishikura/opt/amber10.eth'),
                        path = '/home/ishikura/opt/amber10.eth/exe/sander.MPI',
                    ),
                    marvin = dict(
                        envs = {},
                        # path = '/home/hpcs/Nagara/app/bin/marvin',
                        path = '/home/ishikura/Nagara/app/bin/marvin',
                    ),
                    paics = dict(
                        # envs = dict(PAICS_HOME='/home/ishi/paics/paics-20081214'),
                        # path = '/home/ishi/paics/paics-20081214/main.exe',
                        envs = dict(PAICS_HOME='/home/ishi/paics/paics-20081214'),
                        path = '/home/ishi/paics/paics-20081214/main.exe',
                    ),
                ),
            ),
            vlsn = dict(),
            rccs = dict(),
        )

        treestyles = []
        events = []
        for data in alldata:
            if data.startswith("TR_"):
                treestyles.append(data)
            elif data.startswith("EVT_"):
                events.append(data)
                
        events = events + [i for i in dir(wx) if i.startswith("EVT_TREE_")]
        for evt in ["EVT_TREE_GET_INFO", "EVT_TREE_SET_INFO", "EVT_TREE_ITEM_MIDDLE_CLICK",
                    "EVT_TREE_STATE_IMAGE_CLICK"]:
            events.remove(evt)
            
        treestyles = treestyles + [i for i in dir(wx) if i.startswith("TR_")]

        self.events = events
        self.styles = treestyles
        self.item = None
        
        il = wx.ImageList(16, 16)

        for items in ArtIDs[1:-1]:
            bmp = wx.ArtProvider_GetBitmap(eval(items), wx.ART_TOOLBAR, (16, 16))
            il.Add(bmp)

        #smileidx = il.Add(images.Smiles.GetBitmap())
        numicons = il.GetImageCount()

        self.AssignImageList(il)
        self.count = 0
        self.log = log

        # NOTE:  For some reason tree items have to have a data object in
        #        order to be sorted.  Since our compare just uses the labels
        #        we don't need any real data, so we'll just use None below for
        #        the item data.

        # create some columns
        self.AddColumn("Main column")
        self.AddColumn("Column 1")
        self.AddColumn("Column 2")
        self.SetMainColumn(0) # the one with the tree in it...
        self.SetColumnWidth(0, 175)

        self.root = self.AddRoot("The Root Item")

        if not(self.GetWindowStyle() & wx.TR_HIDE_ROOT):
            self.SetPyData(self.root, None)
            self.SetItemImage(self.root, 24, which=wx.TreeItemIcon_Normal)
            self.SetItemImage(self.root, 13, which=wx.TreeItemIcon_Expanded)
            self.SetItemText(self.root, "col 1 root", 1)
            self.SetItemText(self.root, "col 2 root", 2)
             
        for item in remote_configs:
            #txt = "Item %d" % x
            
            child = self.AppendItem(self.root, item)

            self.SetPyData(child, None)
            self.SetItemText(child, item, 1)
            self.SetItemText(child, item + " (c2)", 2)
            self.SetItemImage(child, 24, which=wx.TreeItemIcon_Normal)
            self.SetItemImage(child, 13, which=wx.TreeItemIcon_Expanded)
            
            if item == 'local':
                for item2 in remote_configs['local']:
                    
                    
                    last = self.AppendItem(child, item2)
                    self.SetPyData(last, None)
                    self.SetItemText(last, item2[:-1], 1)
                    if item2 == 'jms':
                        for item3 in remote_configs['local']['jms']:
                            
                            third = self.AppendItem(last,item3)
                            
                            self.SetPyData(third,None)
                            self.SetItemText(third, item3[:-1], 1)
            '''    
            for y in range(5):
                txt = "item %d-%s" % (x, chr(ord("a")+y))
                
                last = self.AppendItem(child, txt)
           
                #last = self.AppendItem(child, txt, ct_type=2)
                    
                self.SetPyData(last, None)
                self.SetItemText(last, txt + " (c1)", 1)
                self.SetItemText(last, txt + " (c2)", 2)
                self.SetItemImage(last, 24, which=wx.TreeItemIcon_Normal)
                self.SetItemImage(last, 13, which=wx.TreeItemIcon_Expanded)
                
                for z in range(5):                    
                    txt = "item %d-%s-%d" % (x, chr(ord("a")+y), z)
                    if z > 2:
                        item = self.AppendItem(last, txt, ct_type=1)
                    elif 0 < z <= 2:
                        item = self.AppendItem(last, txt, ct_type=2)
                    elif z == 0:
                        item = self.AppendItem(last, txt)
                        
                    self.SetPyData(item, None)

                    if x == 0 and y == 0 and z == 0:
                        self.SetItemText(item, "", 1)
                        self.SetItemText(item, txt + " (c2)", 2)
                        self.SetItemWindow(item, self.CreateTreeCtrl(), 1)
                    
                    else:
                        self.SetItemText(item, txt + " (c1)", 1)
                        self.SetItemText(item, txt + " (c2)", 2)
                        if z == 0:
                            self.SetItemHyperText(item, True)
                        
                    self.SetItemImage(item, 28, which=wx.TreeItemIcon_Normal)
                    self.SetItemImage(item, numicons-1, which=wx.TreeItemIcon_Selected)
            '''

        self.GetMainWindow().Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
        self.Bind(wx.EVT_IDLE, self.OnIdle)
        self.GetMainWindow().Bind(wx.EVT_RIGHT_UP, self.OnRightUp)

        self.eventdict = {'EVT_TREE_BEGIN_DRAG': self.OnBeginDrag, 'EVT_TREE_BEGIN_LABEL_EDIT': self.OnBeginEdit,
                          'EVT_TREE_BEGIN_RDRAG': self.OnBeginRDrag, 'EVT_TREE_DELETE_ITEM': self.OnDeleteItem,
                          'EVT_TREE_END_DRAG': self.OnEndDrag, 'EVT_TREE_END_LABEL_EDIT': self.OnEndEdit,
                          'EVT_TREE_ITEM_ACTIVATED': self.OnActivate, 'EVT_TREE_ITEM_CHECKED': self.OnItemCheck,
                          'EVT_TREE_ITEM_CHECKING': self.OnItemChecking, 'EVT_TREE_ITEM_COLLAPSED': self.OnItemCollapsed,
                          'EVT_TREE_ITEM_COLLAPSING': self.OnItemCollapsing, 'EVT_TREE_ITEM_EXPANDED': self.OnItemExpanded,
                          'EVT_TREE_ITEM_EXPANDING': self.OnItemExpanding, 'EVT_TREE_ITEM_GETTOOLTIP': self.OnToolTip,
                          'EVT_TREE_ITEM_MENU': self.OnItemMenu, 'EVT_TREE_ITEM_RIGHT_CLICK': self.OnRightDown,
                          'EVT_TREE_KEY_DOWN': self.OnKey, 'EVT_TREE_SEL_CHANGED': self.OnSelChanged,
                          'EVT_TREE_SEL_CHANGING': self.OnSelChanging, "EVT_TREE_ITEM_HYPERLINK": self.OnHyperLink}

       

    

    def BindEvents(self, choice, recreate=False):

        value = choice.GetValue()
        text = choice.GetLabel()
        
        evt = "wx." + text
        binder = self.eventdict[text]

        if value == 1:
            if evt == "wx.EVT_TREE_BEGIN_RDRAG":
                self.GetMainWindow().Bind(wx.EVT_RIGHT_DOWN, None)
                self.GetMainWindow().Bind(wx.EVT_RIGHT_UP, None)
            try:
                self.Bind(eval(evt), binder)
            except:
                self.Bind(eval("HTL." + text), binder)
        else:
            try:
                self.Bind(eval(evt), None)
            except:
                self.Bind(eval("HTL." + text), None)

            if evt == "wx.EVT_TREE_BEGIN_RDRAG":
                self.GetMainWindow().Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
                self.GetMainWindow().Bind(wx.EVT_RIGHT_UP, self.OnRightUp)


    def ChangeStyle(self, combos):

        style = 0
        for combo in combos:
            if combo.GetValue() == 1:
                try:
                    style = style | eval("wx." + combo.GetLabel())
                except:
                    style = style | eval("HTL." + combo.GetLabel())

        if self.GetWindowStyle() != style:
            self.SetWindowStyle(style)
            

    def OnCompareItems(self, item1, item2):
        
        t1 = self.GetItemText(item1)
        t2 = self.GetItemText(item2)
        
        self.log.write('compare: ' + t1 + ' <> ' + t2 + "\n")

        if t1 < t2:
            return -1
        if t1 == t2:
            return 0

        return 1

    
    def OnIdle(self, event):

        pass

    def OnRightDown(self, event):pass


    def OnRightUp(self, event):

        item = self.item
        
        if not item:
            event.Skip()
            return

        if not self.IsItemEnabled(item):
            event.Skip()
            return

        # Item Text Appearance
        ishtml = self.IsItemHyperText(item)
        back = self.GetItemBackgroundColour(item)
        fore = self.GetItemTextColour(item)
        isbold = self.IsBold(item)
        font = self.GetItemFont(item)

        # Icons On Item
        normal = self.GetItemImage(item, wx.TreeItemIcon_Normal)
        selected = self.GetItemImage(item, wx.TreeItemIcon_Selected)
        expanded = self.GetItemImage(item, wx.TreeItemIcon_Expanded)
        selexp = self.GetItemImage(item, wx.TreeItemIcon_SelectedExpanded)
        
        # Enabling/Disabling Windows Associated To An Item
        haswin = self.GetItemWindow(item)

        # Enabling/Disabling Items
        enabled = self.IsItemEnabled(item)

        # Generic Item's Info
        children = self.GetChildrenCount(item)
        itemtype = self.GetItemType(item)
        text = self.GetItemText(item)
        pydata = self.GetPyData(item)
        
        self.current = item
        self.itemdict = {"ishtml": ishtml, "back": back, "fore": fore, "isbold": isbold,
                         "font": font, "normal": normal, "selected": selected, "expanded": expanded,
                         "selexp": selexp, "haswin": haswin, "children": children,
                         "itemtype": itemtype, "text": text, "pydata": pydata, "enabled": enabled}
        
        menu = wx.Menu()

        item2 = menu.Append(wx.ID_ANY, "Modify Item Text Colour")
        menu.AppendSeparator()
        if isbold:
            strs = "Make Item Text Not Bold"
        else:
            strs = "Make Item Text Bold"
        item3 = menu.Append(wx.ID_ANY, strs)
        item4 = menu.Append(wx.ID_ANY, "Change Item Font")
        item13 = menu.Append(wx.ID_ANY, "Change Item Background Colour")
        menu.AppendSeparator()
        if ishtml:
            strs = "Set Item As Non-Hyperlink"
        else:
            strs = "Set Item As Hyperlink"
        item5 = menu.Append(wx.ID_ANY, strs)
        menu.AppendSeparator()

        item7 = menu.Append(wx.ID_ANY, "Disable Item")
        
        menu.AppendSeparator()
        item8 = menu.Append(wx.ID_ANY, "Change Item Icons")
        menu.AppendSeparator()
        item9 = menu.Append(wx.ID_ANY, "Get Other Information For This Item")
        menu.AppendSeparator()

        item10 = menu.Append(wx.ID_ANY, "Delete Item")
        if item == self.GetRootItem():
            item10.Enable(False)
        item11 = menu.Append(wx.ID_ANY, "Prepend An Item")
        item12 = menu.Append(wx.ID_ANY, "Append An Item")

        self.Bind(wx.EVT_MENU, self.OnItemForeground, item2)
        self.Bind(wx.EVT_MENU, self.OnItemBold, item3)
        self.Bind(wx.EVT_MENU, self.OnItemFont, item4)
        self.Bind(wx.EVT_MENU, self.OnItemHyperText, item5)
        self.Bind(wx.EVT_MENU, self.OnDisableItem, item7)
        self.Bind(wx.EVT_MENU, self.OnItemIcons, item8)
        self.Bind(wx.EVT_MENU, self.OnItemInfo, item9)
        self.Bind(wx.EVT_MENU, self.OnItemDelete, item10)
        self.Bind(wx.EVT_MENU, self.OnItemPrepend, item11)
        self.Bind(wx.EVT_MENU, self.OnItemAppend, item12)
        self.Bind(wx.EVT_MENU, self.OnItemBackground, item13)
        
        self.PopupMenu(menu)
        menu.Destroy()
        event.Skip()
        

    def OnItemForeground(self, event):

        colourdata = wx.ColourData()
        colourdata.SetColour(self.itemdict["fore"])
        dlg = wx.ColourDialog(self, colourdata)
        
        dlg.GetColourData().SetChooseFull(True)

        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetColourData()
            col1 = data.GetColour().Get()
            self.SetItemTextColour(self.current, col1)
        dlg.Destroy()
        event.Skip()


    def OnItemBold(self, event):

        self.SetItemBold(self.current, not self.itemdict["isbold"])
        event.Skip()


    def OnItemFont(self, event):

        data = wx.FontData()
        font = self.itemdict["font"]
        
        if font is None:
            font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
            
        data.SetInitialFont(font)

        dlg = wx.FontDialog(self, data)
        
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetFontData()
            font = data.GetChosenFont()
            self.SetItemFont(self.current, font)

        dlg.Destroy()
        event.Skip()
        

    def OnItemHyperText(self, event):

        self.SetItemHyperText(self.current, not self.itemdict["ishtml"])
        event.Skip()


    def OnDisableItem(self, event):

        self.EnableItem(self.current, False)
        event.Skip()
        

    def OnItemIcons(self, event):

        bitmaps = [self.itemdict["normal"], self.itemdict["selected"],
                   self.itemdict["expanded"], self.itemdict["selexp"]]

        wx.BeginBusyCursor()        
        dlg = TreeIcons(self, -1, bitmaps=bitmaps)
        wx.EndBusyCursor()
        dlg.ShowModal()
        event.Skip()


    def SetNewIcons(self, bitmaps):

        self.SetItemImage(self.current, bitmaps[0], which=wx.TreeItemIcon_Normal)
        self.SetItemImage(self.current, bitmaps[1], which=wx.TreeItemIcon_Selected)
        self.SetItemImage(self.current, bitmaps[2], which=wx.TreeItemIcon_Expanded)
        self.SetItemImage(self.current, bitmaps[3], which=wx.TreeItemIcon_SelectedExpanded)


    def OnItemInfo(self, event):

        itemtext = self.itemdict["text"]
        numchildren = str(self.itemdict["children"])
        itemtype = self.itemdict["itemtype"]
        pydata = repr(type(self.itemdict["pydata"]))

        if itemtype == 0:
            itemtype = "Normal"
        elif itemtype == 1:
            itemtype = "CheckBox"
        else:
            itemtype = "RadioButton"

        strs = "Information On Selected Item:\n\n" + "Text: " + itemtext + "\n" \
               "Number Of Children: " + numchildren + "\n" \
               "Item Type: " + itemtype + "\n" \
               "Item Data Type: " + pydata + "\n"

        dlg = wx.MessageDialog(self, strs, "HyperTreeListDemo Info", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
                
        event.Skip()
        

    def OnItemDelete(self, event):

        strs = "Are You Sure You Want To Delete Item " + self.GetItemText(self.current) + "?"
        dlg = wx.MessageDialog(None, strs, 'Deleting Item', wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_QUESTION)

        if dlg.ShowModal() in [wx.ID_NO, wx.ID_CANCEL]:
            dlg.Destroy()
            return

        dlg.Destroy()

        self.DeleteChildren(self.current)
        self.Delete(self.current)
        self.current = None
        
        event.Skip()        


    def OnItemPrepend(self, event):

        dlg = wx.TextEntryDialog(self, "Please Enter The New Item Name", 'Item Naming', 'Python')

        if dlg.ShowModal() == wx.ID_OK:
            newname = dlg.GetValue()
            newitem = self.PrependItem(self.current, newname)
            self.EnsureVisible(newitem)

        dlg.Destroy()
        event.Skip()


    def OnItemAppend(self, event):

        dlg = wx.TextEntryDialog(self, "Please Enter The New Item Name", 'Item Naming', 'Python')

        if dlg.ShowModal() == wx.ID_OK:
            newname = dlg.GetValue()
            newitem = self.AppendItem(self.current, newname)
            self.EnsureVisible(newitem)

        dlg.Destroy()
        event.Skip()
        

    def OnItemBackground(self, event):

        colourdata = wx.ColourData()
        colourdata.SetColour(self.itemdict["back"])
        dlg = wx.ColourDialog(self, colourdata)
        
        dlg.GetColourData().SetChooseFull(True)

        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetColourData()
            col1 = data.GetColour().Get()
            self.SetItemBackgroundColour(self.current, col1)
            
        dlg.Destroy()
        event.Skip()
        

    def OnBeginEdit(self, event):
        
        pass

    def OnEndEdit(self, event):
        
        pass

    def OnLeftDClick(self, event):
        
        pass             
        

    def OnItemExpanded(self, event):     
        pass


    def OnItemExpanding(self, event):
        pass
               
    def OnItemCollapsed(self, event):

        pass
            

    def OnItemCollapsing(self, event):

        pass

        
    def OnSelChanged(self, event):

        pass


    def OnSelChanging(self, event):

        pass

    def OnBeginDrag(self, event):

        pass


    def OnBeginRDrag(self, event):

        pass
        

    def OnEndDrag(self, event):

        pass


    def OnDeleteItem(self, event):

        item = event.GetItem()

        if not item:
            return

        #self.log.write("Deleting Item: %s\n" % self.GetItemText(item))
        event.Skip()
        

    def OnItemCheck(self, event):

        item = event.GetItem()
        #self.log.write("Item " + self.GetItemText(item) + " Has Been Cheched!\n")
        event.Skip()


    def OnItemChecking(self, event):

        item = event.GetItem()
        #self.log.write("Item " + self.GetItemText(item) + " Is Being Checked...\n")
        event.Skip()
        

    def OnToolTip(self, event):

        pass

    def OnItemMenu(self, event):

        pass


    def OnKey(self, event):

        pass
        
        
    def OnActivate(self, event):
        
        pass
        
    def OnHyperLink(self, event):

        pass

    def OnTextCtrl(self, event):

        pass

    def OnComboBox(self, event):

        pass


#---------------------------------------------------------------------------
 
def main():
    import nagaratest
    app = nagaratest.FrameTest()
    log = app.log
    frame = app.frame

    dlg = HyperTreeListPanel(frame)
    # paicspanel.MarvinPanel(dlg, -1, 'marvin', log=self.getLog())
    
    

    # app.MainLoop()

    try:
        app.MainLoop()
    except:
        app.RedirectStdio()


if __name__ == '__main__':
    main()
    module = __file__.split('.')[0]
    print 
            
        
        
    #bitmapDir = "agw/bitmaps/"