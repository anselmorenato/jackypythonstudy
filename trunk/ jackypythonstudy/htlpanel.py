import wx

import wx.lib.agw.hypertreelist as HTL
import ListCtrl

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
        self.SetSize(sizer)
        sizer.Layout()
        
        
class HyperTreeList(HTL.HyperTreeList):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 style=wx.SUNKEN_BORDER | wx.TR_HAS_BUTTONS | wx.TR_HAS_VARIABLE_ROW_HEIGHT,
                 log=None):

        HTL.HyperTreeList.__init__(self, parent, id, pos, size, style)

        alldata = dir(HTL)

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

        textctrl = wx.TextCtrl(self.GetMainWindow(), -1, "I Am A Simple\nMultiline wx.TexCtrl", style=wx.TE_MULTILINE)
        self.gauge = wx.Gauge(self.GetMainWindow(), -1, 50, style=wx.GA_HORIZONTAL|wx.GA_SMOOTH)
        self.gauge.SetValue(0)
        combobox = wx.ComboBox(self.GetMainWindow(), -1, choices=["That", "Was", "A", "Nice", "Holiday!"], style=wx.CB_READONLY|wx.CB_DROPDOWN)
        button1 = wx.Button(self.GetMainWindow(), -1, "wxPython")
        button1.SetSize(button1.GetBestSize())
        button2 = wx.Button(self.GetMainWindow(), -1, "Rules!")
        button2.SetSize(button2.GetBestSize())
        listctrl = ListCtrl.TestListCtrlPanel(self.GetMainWindow(), self.log)
        listctrl.SetSize((500, 200))
        
        textctrl.Bind(wx.EVT_CHAR, self.OnTextCtrl)
        combobox.Bind(wx.EVT_COMBOBOX, self.OnComboBox)

        for x in range(15):
            txt = "Item %d" % x
            if x == 1:
                child = self.AppendItem(self.root, txt + "\nHello World\nHappy wxPython-ing!")
                self.SetItemBold(child, True)
            else:
                child = self.AppendItem(self.root, txt)

            self.SetPyData(child, None)
            self.SetItemText(child, txt + " (c1)", 1)
            self.SetItemText(child, txt + " (c2)", 2)
            self.SetItemImage(child, 24, which=wx.TreeItemIcon_Normal)
            self.SetItemImage(child, 13, which=wx.TreeItemIcon_Expanded)
                
            for y in range(5):
                txt = "item %d-%s" % (x, chr(ord("a")+y))
                if y == 0 and x == 1:
                    last = self.AppendItem(child, txt, ct_type=2, wnd=self.gauge)
                elif y == 1 and x == 2:
                    last = self.AppendItem(child, txt, ct_type=1, wnd=textctrl)
                elif 2 < y < 4:
                    last = self.AppendItem(child, txt)
                elif y == 4 and x == 1:
                    last = self.AppendItem(child, txt, wnd=combobox)
                else:
                    last = self.AppendItem(child, txt, ct_type=2)
                    
                self.SetPyData(last, None)
                self.SetItemText(last, txt + " (c1)", 1)
                self.SetItemText(last, txt + " (c2)", 2)
                self.SetItemImage(last, 24, which=wx.TreeItemIcon_Normal)
                self.SetItemImage(last, 13, which=wx.TreeItemIcon_Expanded)

                if y == 3 and x == 0:
                    self.SetItemWindow(last, button1, 1)
                    self.SetItemWindow(last, button2, 2)

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
                    elif x == 0 and y == 0 and z == 1:
                        self.SetItemText(item, txt + " (c1)", 1)
                        self.SetItemText(item, "", 2)
                        self.SetItemWindow(item, listctrl, 2)
                    else:
                        self.SetItemText(item, txt + " (c1)", 1)
                        self.SetItemText(item, txt + " (c2)", 2)
                        if z == 0:
                            self.SetItemHyperText(item, True)
                        
                    self.SetItemImage(item, 28, which=wx.TreeItemIcon_Normal)
                    self.SetItemImage(item, numicons-1, which=wx.TreeItemIcon_Selected)

        self.GetMainWindow().Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
        self.Bind(wx.EVT_IDLE, self.OnIdle)

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

        mainframe = wx.GetTopLevelParent(self)
        
        if not hasattr(mainframe, "leftpanel"):
            self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded)
            self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed)
            self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
            self.Bind(wx.EVT_TREE_SEL_CHANGING, self.OnSelChanging)
            self.GetMainWindow().Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
            self.GetMainWindow().Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
        else:
            for combos in mainframe.treeevents:
                self.BindEvents(combos)

        if hasattr(mainframe, "leftpanel"):
            self.ChangeStyle(mainframe.treestyles)

        if not(self.GetWindowStyle() & wx.TR_HIDE_ROOT):
            self.SelectItem(self.root)
            self.Expand(self.root)
            

    def CreateTreeCtrl(self):

        tree = wx.TreeCtrl(self.GetMainWindow(), -1, wx.Point(0, 0), wx.Size(160, 200),
                           wx.TR_DEFAULT_STYLE)
        
        items = []

        imglist = wx.ImageList(16, 16, True, 2)
        imglist.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, wx.Size(16,16)))
        imglist.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, wx.Size(16,16)))
        tree.AssignImageList(imglist)

        root = tree.AddRoot("HyperTreeList :-D", image=0)

        items.append(tree.AppendItem(root, "Item 1", 0))
        items.append(tree.AppendItem(root, "Item 2", 0))
        items.append(tree.AppendItem(root, "Item 3", 0))
        items.append(tree.AppendItem(root, "Item 4", 0))
        items.append(tree.AppendItem(root, "Item 5", 0))

        for ii in xrange(len(items)):
        
            id = items[ii]
            tree.AppendItem(id, "Subitem 1", 1)
            tree.AppendItem(id, "Subitem 2", 1)
            tree.AppendItem(id, "Subitem 3", 1)
            tree.AppendItem(id, "Subitem 4", 1)
            tree.AppendItem(id, "Subitem 5", 1)
        
        tree.Expand(root)
        tree.Expand(items[1])
        tree.Expand(items[3])
        tree.SelectItem(root)
        
        return tree


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

        if self.gauge:

            try:
                if self.gauge.IsEnabled() and self.gauge.IsShown():
                    self.count = self.count + 1

                    if self.count >= 50:
                        self.count = 0

                    self.gauge.SetValue(self.count)

            except:
                
                self.gauge = None

        event.Skip()


    def OnRightDown(self, event):
        
        pt = event.GetPosition()
        item, flags, column = self.HitTest(pt)

        if item:
            self.item = item
            self.log.write("OnRightClick: %s, %s, %s\n" % (self.GetItemText(item), type(item), item.__class__))
            self.SelectItem(item)


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
        
        self.log.write("OnBeginEdit\n")
        # show how to prevent edit...
        item = event.GetItem()
        if item and self.GetItemText(item) == "The Root Item":
            wx.Bell()
            self.log.write("You can't edit this one...\n")

            # Lets just see what's visible of its children
            cookie = 0
            root = event.GetItem()
            (child, cookie) = self.GetFirstChild(root)

            while child:
                self.log.write("Child [%s] visible = %d\n" % (self.GetItemText(child), self.IsVisible(child)))
                (child, cookie) = self.GetNextChild(root, cookie)

            event.Veto()


    def OnEndEdit(self, event):
        
        self.log.write("OnEndEdit: %s %s\n" %(event.IsEditCancelled(), event.GetLabel()))
        # show how to reject edit, we'll not allow any digits
        for x in event.GetLabel():
            if x in string.digits:
                self.log.write("You can't enter digits...\n")
                event.Veto()
                return
            

    def OnLeftDClick(self, event):
        
        pt = event.GetPosition()
        item, flags, column = self.HitTest(pt)
        if item and (flags & wx.TREE_HITTEST_ONITEMLABEL):
            if self.GetWindowStyle() & wx.TR_EDIT_LABELS:
                self.log.write("OnLeftDClick: %s (manually starting label edit)\n"% self.GetItemText(item))
                self.EditLabel(item)
            else:
                self.log.write("OnLeftDClick: Cannot Start Manual Editing, Missing Style TR_EDIT_LABELS\n")

        event.Skip()                
        

    def OnItemExpanded(self, event):
        
        item = event.GetItem()
        if item:
            self.log.write("OnItemExpanded: %s\n" % self.GetItemText(item))


    def OnItemExpanding(self, event):
        
        item = event.GetItem()
        if item:
            self.log.write("OnItemExpanding: %s\n" % self.GetItemText(item))
            
        event.Skip()

        
    def OnItemCollapsed(self, event):

        item = event.GetItem()
        if item:
            self.log.write("OnItemCollapsed: %s" % self.GetItemText(item))
            

    def OnItemCollapsing(self, event):

        item = event.GetItem()
        if item:
            self.log.write("OnItemCollapsing: %s\n" % self.GetItemText(item))
    
        event.Skip()

        
    def OnSelChanged(self, event):

        self.item = event.GetItem()
        if self.item:
            self.log.write("OnSelChanged: %s" % self.GetItemText(self.item))
            if wx.Platform == '__WXMSW__':
                self.log.write(", BoundingRect: %s\n" % self.GetBoundingRect(self.item, True))
            else:
                self.log.write("\n")
                
        event.Skip()


    def OnSelChanging(self, event):

        item = event.GetItem()
        olditem = event.GetOldItem()
        
        if item:
            if not olditem:
                olditemtext = "None"
            else:
                olditemtext = self.GetItemText(olditem)
            self.log.write("OnSelChanging: From %s To %s\n" %(olditemtext, self.GetItemText(item)))
                
        event.Skip()


    def OnBeginDrag(self, event):

        self.item = event.GetItem()
        if self.item:
            self.log.write("Beginning Drag...\n")

            event.Allow()


    def OnBeginRDrag(self, event):

        self.item = event.GetItem()
        if self.item:
            self.log.write("Beginning Right Drag...\n")

            event.Allow()
        

    def OnEndDrag(self, event):

        self.item = event.GetItem()
        if self.item:
            self.log.write("Ending Drag!\n")

        event.Skip()            


    def OnDeleteItem(self, event):

        item = event.GetItem()

        if not item:
            return

        self.log.write("Deleting Item: %s\n" % self.GetItemText(item))
        event.Skip()
        

    def OnItemCheck(self, event):

        item = event.GetItem()
        self.log.write("Item " + self.GetItemText(item) + " Has Been Cheched!\n")
        event.Skip()


    def OnItemChecking(self, event):

        item = event.GetItem()
        self.log.write("Item " + self.GetItemText(item) + " Is Being Checked...\n")
        event.Skip()
        

    def OnToolTip(self, event):

        item = event.GetItem()
        if item:
            event.SetToolTip(wx.ToolTip(self.GetItemText(item)))


    def OnItemMenu(self, event):

        item = event.GetItem()
        if item:
            self.log.write("OnItemMenu: %s\n" % self.GetItemText(item))
    
        event.Skip()


    def OnKey(self, event):

        keycode = event.GetKeyCode()
        keyname = keyMap.get(keycode, None)
                
        if keycode == wx.WXK_BACK:
            self.log.write("OnKeyDown: HAHAHAHA! I Vetoed Your Backspace! HAHAHAHA\n")
            return

        if keyname is None:
            if "unicode" in wx.PlatformInfo:
                keycode = event.GetUnicodeKey()
                if keycode <= 127:
                    keycode = event.GetKeyCode()
                keyname = "\"" + unichr(event.GetUnicodeKey()) + "\""
                if keycode < 27:
                    keyname = "Ctrl-%s" % chr(ord('A') + keycode-1)
                
            elif keycode < 256:
                if keycode == 0:
                    keyname = "NUL"
                elif keycode < 27:
                    keyname = "Ctrl-%s" % chr(ord('A') + keycode-1)
                else:
                    keyname = "\"%s\"" % chr(keycode)
            else:
                keyname = "unknown (%s)" % keycode
                
        self.log.write("OnKeyDown: You Pressed '" + keyname + "'\n")

        event.Skip()
        
        
    def OnActivate(self, event):
        
        if self.item:
            self.log.write("OnActivate: %s\n" % self.GetItemText(self.item))

        event.Skip()

        
    def OnHyperLink(self, event):

        item = event.GetItem()
        if item:
            self.log.write("OnHyperLink: %s\n" % self.GetItemText(self.item))
            

    def OnTextCtrl(self, event):

        char = chr(event.GetKeyCode())
        self.log.write("EDITING THE TEXTCTRL: You Wrote '" + char + \
                       "' (KeyCode = " + str(event.GetKeyCode()) + ")\n")
        event.Skip()


    def OnComboBox(self, event):

        selection = event.GetEventObject().GetValue()
        self.log.write("CHOICE FROM COMBOBOX: You Chose '" + selection + "'\n")
        event.Skip()


#---------------------------------------------------------------------------
            
            
        
        
    #bitmapDir = "agw/bitmaps/"