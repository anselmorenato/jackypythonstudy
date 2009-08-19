
import wx
#import htlpanel 
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
remote_configs = dict(
    # email = 'ishikura@gifu-u.ac.jp',
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
choice =remote_configs.keys() #['vlsn','rccs','local','email','hpcs']
        
class RemotePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self,parent,-1)
        
        self.listbox = wx.ListBox(self, size = (130,50),choices=choice)
        index = self.listbox.SetSelection(0)
        self.listbox.SetFont(wx.Font(11,wx.SWISS,wx.NORMAL,wx.NORMAL))
        
        
        self.CreateTreeList()
        #self.root = self.tree.root
        
        self.okBtn = wx.Button(self, -1, "Ok")
        self.cancelBtn = wx.Button(self, -1, "Cancel")
        self.Bind(wx.EVT_BUTTON, self.OnCancel, self.cancelBtn)
        # create the edit button
        self.b1 = wx.Button(self, -1, "New")
        self.Bind(wx.EVT_BUTTON, self.OnAddNewListItem, self.b1)
        self.b1.SetDefault()
        self.b1.SetSize(self.b1.GetBestSize())
        self.b2 = wx.Button(self, -1, "Edit")
        self.Bind(wx.EVT_BUTTON, self.OnEditListItem, self.b2)
        self.b2.SetDefault()
        self.b2.SetSize(self.b2.GetBestSize())
        self.b3 = wx.Button(self, -1, "Copy")
        self.Bind(wx.EVT_BUTTON, self.OnCopyListItem, self.b3)
        self.b3.SetDefault()
        self.b3.SetSize(self.b3.GetBestSize())
        self.b4 = wx.Button(self, -1, "Delete")
        self.Bind(wx.EVT_BUTTON, self.OnDeleteListItem, self.b4)
        self.b4.SetDefault()
        self.b4.SetSize(self.b4.GetBestSize())
        
        self.Dolayout()
        self.initBind()
    def Dolayout(self):
        # create the mainsizer      
        self.mainsizer = wx.BoxSizer(wx.VERTICAL)
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        # The sizer_1 has two subsizer
        sizer_1_lb = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'ListBox'), orient=wx.VERTICAL)
        sizer_1_bt = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Edit Botton'),orient = wx.VERTICAL)
        # The sizer_2 has two button
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_1_lb.Add(self.listbox,1,wx.EXPAND,5)                        
        sizer_1.Add(sizer_1_lb, 0, wx.EXPAND|wx.ALL,5)

        sizer_1_bt.Add(self.b1,0,wx.EXPAND|wx.ALL)
        sizer_1_bt.Add(self.b2,0,wx.EXPAND|wx.ALL)
        sizer_1_bt.Add(self.b3,0,wx.EXPAND|wx.ALL)
        sizer_1_bt.Add(self.b4,0,wx.EXPAND|wx.ALL)
        sizer_1.Add((150,-1))
        sizer_1.Add(sizer_1_bt,0,wx.EXPAND|wx.ALL,5)

        sizer_2.Add(self.okBtn,0,wx.ALIGN_RIGHT)
        sizer_2.Add(self.cancelBtn,0,wx.ALIGN_RIGHT)

        self.mainsizer.Add(sizer_1,0,wx.ALIGN_CENTER, 5)
        self.mainsizer.Add(self.tree,3,wx.EXPAND)
        self.mainsizer.Add(sizer_2,0,wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT)

        self.SetSizer(self.mainsizer)
        self.mainsizer.Fit(self.GetParent())
        #self.SetAutoLayout(True)
        #self.mainsizer.SetSizeHints(self)
    def initBind(self):
        # show a dialog by double click
        self.listbox.Bind(wx.EVT_LISTBOX_DCLICK, self.EvtListBoxDClick, self.listbox)
        # select the item which control the TreeListCtrl
        self.listbox.Bind(wx.EVT_LISTBOX, self.EvtListBox, self.listbox)
        # right click
        self.listbox.Bind(wx.EVT_RIGHT_UP, self.EvtRightClick)

    def OnClick(self, event): 
        pass

        #sizer.Layout()
    def OnClick(self, event): pass

    def OnCancel(self,event):
        self.GetParent().Close(True)
    
    #----------------------------------------------------------------------
    def OnAddNewListItem(self,event):
        dlg = wx.TextEntryDialog(self,'Please enter the item name you want to add!','Add the new item','new')
        if dlg.ShowModal()== wx.ID_OK:
            self.listbox.Insert(dlg.GetValue(),self.listbox.GetSelection())
        dlg.Destroy()
    def OnEditListItem(self,event):
        selection = self.listbox.GetSelection()
        dlg = wx.TextEntryDialog(self,'Please enter the item name you want to Edit!','Edit the item',self.listbox.GetString(selection))
        if dlg.ShowModal()== wx.ID_OK:
            
            self.listbox.Insert(dlg.GetValue(),selection)
            self.listbox.Delete(selection+1)
        dlg.Destroy()
    def OnCopyListItem(self,event):
        pass
    def OnDeleteListItem(self,event):
        pass
    
    def EvtListBoxDClick(self,event):
        """"""
        lb = event.GetEventObject()
        tag = lb.GetSelection()
    
        import settingdlg
        dlg = settingdlg.SettingDialog(None,-1)
        dlg.Show()
        event.Skip()
    def EvtListBox(self,event):
        #change the ItemText of root
        self.tree.SetItemText(self.tree.GetRootItem(),event.GetString())
        if remote_configs.has_key(event.GetString())==True and type(remote_configs[event.GetString()])==str:
            self.tree.SetItemText(self.tree.GetRootItem(),remote_configs[event.GetString()],1)
        else:
            self.tree.SetItemText(self.tree.GetRootItem(),event.GetString(),1)
        
        if self.tree.HasChildren(self.tree.GetRootItem())==True:
            self.tree.DeleteChildren(self.tree.GetRootItem())
            if remote_configs.has_key(event.GetString())==True and type(remote_configs[event.GetString()])==dict:
                self.AddTreeNodes(self.tree.GetRootItem(),remote_configs[event.GetString()])
                self.tree.Expand(self.tree.GetRootItem())
        elif remote_configs.has_key(event.GetString())==True and type(remote_configs[event.GetString()])==dict:
            self.AddTreeNodes(self.tree.GetRootItem(),remote_configs[event.GetString()])
            self.tree.Expand(self.tree.GetRootItem())
    def EvtRightClick(self,event):
        
        self.popupID1 = wx.NewId()
        self.popupID2 = wx.NewId()
        self.popupID3 = wx.NewId()
        self.popupID4 = wx.NewId()
        self.popupID5 = wx.NewId()
        self.popupID6 = wx.NewId()
        self.popupID7 = wx.NewId()
        self.popupID8 = wx.NewId()
        self.popupID9 = wx.NewId()
        # make a menu
        menu = wx.Menu()
        # Show how to put an icon in the menu
        item = wx.MenuItem(menu, self.popupID1,"New")
        #bmp = images.Smiles.GetBitmap()
        #item.SetBitmap(bmp)
        menu.AppendItem(item)
        # add some other items
        menu.Append(self.popupID2, "Edit")
        menu.Append(self.popupID3, "Copy")
        menu.Append(self.popupID4, "Delete")
        
        # make a submenu
        # sm = wx.Menu()
        # sm.Append(self.popupID8, "sub item 1")
        # sm.Append(self.popupID9, "sub item 1")
        # menu.AppendMenu(self.popupID7, "Test Submenu", sm)


        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        self.PopupMenu(menu)
        menu.Destroy()

    def CreateTreeList(self):
        il = wx.ImageList(16, 16)
        for items in ArtIDs[1:-1]:
            bmp = wx.ArtProvider_GetBitmap(eval(items), wx.ART_TOOLBAR, (16, 16))
            il.Add(bmp)
        #smileidx = il.Add(images.Smiles.GetBitmap())
        numicons = il.GetImageCount()
        # Create the tree
        self.tree = wx.gizmos.TreeListCtrl(self, style =
                                           wx.TR_DEFAULT_STYLE
                                           #| wx.TR_HAS_BUTTONS
                                           #| wx.TR_TWIST_BUTTONS
                                           #| wx.TR_ROW_LINES
                                           #| wx.TR_COLUMN_LINES
                                           #| wx.TR_NO_LINES 
                                           | wx.TR_FULL_ROW_HIGHLIGHT
                                           )
        # Give it the image list
        self.tree.AssignImageList(il)
        # create some columns
        self.tree.AddColumn("Class Name")
        self.tree.AddColumn("Description")
        self.tree.SetMainColumn(0) # the one with the tree in it...
        self.tree.SetColumnWidth(0, 200)
        self.tree.SetColumnWidth(1, 300)
        # Add a root node and assign it some images
        self.root = self.tree.AddRoot("vlsn")
        self.tree.SetItemText(self.root, "Description", 1)
        #self.tree.SetItemImage(self.root, 24,which=wx.TreeItemIcon_Normal)
        #self.tree.SetItemImage(self.root, 13,which=wx.TreeItemIcon_Expanded)
        
    def AddTreeNodes(self,parentItem,items):
        ''''''
        self.root = parentItem
        for item, val in items.items():
            if not isinstance(val,dict):                      
                self.child = self.tree.AppendItem(parentItem, item)
                #self.tree.SetPyData(child, None)
                #self.tree.SetItemText(child, item, 1)
                if type(val)==str:
                    self.tree.SetItemText(self.child,  val, 1)
                #self.tree.SetItemText(self.child, item + " (c2)", 1)
                #self.tree.SetItemImage(self.child, 24, which=wx.TreeItemIcon_Normal)
                #self.tree.SetItemImage(self.child, 13, which=wx.TreeItemIcon_Expanded)
            
            else:
                self.child = self.tree.AppendItem(parentItem, item)
                #self.tree.SetPyData(child, None)
                #self.tree.SetItemText(child, item, 1)
                #self.tree.SetItemText(self.child, item + " (c2)", 1)
                #self.tree.SetItemImage(self.child, 24, which=wx.TreeItemIcon_Normal)
                #self.tree.SetItemImage(self.child, 13, which=wx.TreeItemIcon_Expanded)
                self.AddTreeNodes(self.child, val)
                
def main():
    import nagaratest
    app = nagaratest.FrameTest()
    log = app.log
    frame = app.frame

    dlg = wx.Dialog(None, -1, title='Remote Setting Dialog',size =(500,500),style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
    remote = RemotePanel(dlg)

    #dlg.SetSize(dlg.GetBestSize())
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(remote,1,wx.EXPAND)
    dlg.SetSizer(sizer)
    #sizer.Fit(dlg)
    #dlg.SetAutoLayout(True)
    dlg.ShowModal()
    dlg.Destroy()                

    try:
        app.MainLoop()
    except:
        app.RedirectStdio()


if __name__ == '__main__':
    main()
    
   
    
        
