
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
class RemotePanel(wx.Panel):
    def __init__(self, parent,id,size):
        wx.Panel.__init__(self,parent,-1,size=(500,500))
        
        #splitter = wx.SplitterWindow(self, -1, style=wx.SPLIT_VERTICAL| wx.SP_3D)
        #self.splitter = wx.SplitterWindow(self, ID_SPLITTER, style=wx.SP_BORDER)
        #panel = wx.Panel(splitter, -1, style=wx.WANTS_CHARS)
        choice =['vlsn','rccs','lacal','email','phcs']
        listbox = wx.ListBox(self, size = (130,50),
                       choices=choice)
        tag = listbox.GetSelection()
        listbox.SetFont(wx.Font(11,wx.SWISS,wx.NORMAL,wx.NORMAL))
        #listbox.SetSize(listbox.GetBestFittingSize())
        listbox.Bind(wx.EVT_LISTBOX_DCLICK, self.EvtListBoxDClick, listbox)
        #htl = HyperTreeListPanel(self)
        tree = HyperTreeList(self,-1,size=(500,600),style=wx.TR_DEFAULT_STYLE)
        
        okBtn = wx.Button(self, -1, "Ok")
        cancelBtn = wx.Button(self, -1, "Cancel")
        self.Bind(wx.EVT_BUTTON, self.OnCancel, cancelBtn)
        b1 = wx.Button(self, -1, "New")
        self.Bind(wx.EVT_BUTTON, self.OnClick, b1)
        b1.SetDefault()
        b1.SetSize(b1.GetBestSize())
        b2 = wx.Button(self, -1, "Edit")
        self.Bind(wx.EVT_BUTTON, self.OnClick, b2)
        b2.SetDefault()
        b2.SetSize(b2.GetBestSize())
        b3 = wx.Button(self, -1, "Copy")
        self.Bind(wx.EVT_BUTTON, self.OnClick, b3)
        b3.SetDefault()
        b3.SetSize(b3.GetBestSize())
        b4 = wx.Button(self, -1, "Delete")
        self.Bind(wx.EVT_BUTTON, self.OnClick, b4)
        b4.SetDefault()
        b4.SetSize(b4.GetBestSize())
              
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        sizer_1_stb = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'ListBox'), orient=wx.VERTICAL)
        
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_1_stb.Add(listbox,1,wx.EXPAND,5)                        
        sizer_1.Add(sizer_1_stb, 1, wx.EXPAND|wx.ALL,5)
        
        
        sizer_1_bt = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Edit Botton'),orient = wx.VERTICAL)
        sizer_1_bt.Add(b1,0,wx.EXPAND|wx.ALL)
        sizer_1_bt.Add(b2,0,wx.EXPAND|wx.ALL)
        sizer_1_bt.Add(b3,0,wx.EXPAND|wx.ALL)
        sizer_1_bt.Add(b4,0,wx.EXPAND|wx.ALL)
        sizer_1.Add((80,-1))
        sizer_1.Add(sizer_1_bt,0,wx.EXPAND|wx.ALL,5)
        
        
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(okBtn,0,wx.ALIGN_RIGHT,5)
        sizer_2.Add(cancelBtn,0,wx.ALIGN_RIGHT,5)
        
        #mainsizer.Add((5,20),wx.EXPAND,5)
        mainsizer.Add(sizer_1,0,wx.ALIGN_CENTER, 5)
        #mainsizer.Add((5,20),wx.EXPAND,5)
        mainsizer.Add(tree,1,wx.EXPAND,5)
        mainsizer.Add(sizer_2,0,wx.ALIGN_RIGHT, 5)
        
        
        self.SetSizer(mainsizer)
        mainsizer.Fit(self)
        mainsizer.SetSizeHints(self)
        mainsizer.Layout()
        
    def OnClick(self, event): pass
    def OnCancel(self,event):
        self.Close()
    
    #----------------------------------------------------------------------
    def EvtListBoxDClick(self,event):
        """"""
        lb = event.GetEventObject()
        tag = lb.GetSelection()
        if tag == 2:
            import settingdlg
            dlg = settingdlg.SettingDialog(None,-1)
            dlg.Show()
            event.Skip()
        
    '''        
class HyperTreeListPanel(wx.Panel):
    """This is a HyperTreeListPanel"""
       
    #----------------------------------------------------------------------
    def __init__(self,parent):
        """Constructor"""   
        wx.Panel.__init__(self,parent,-1)
        sizer = wx.BoxSizer(wx.VERTICAL)
        # Create the HyperTreeList
        tree = HyperTreeList(self,-1)
        #tree.Bind(wx.EVT_RIGHT_DOWN, HyperTreeList.OnRightUp, tree)
        sizer.Add(tree,0,wx.EXPAND)
        self.SetSizer(sizer)
        sizer.Fit(self)
        sizer.SetSizeHints(self)
        sizer.Layout()
        
    '''        
        
class HyperTreeList(HTL.HyperTreeList):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 style=wx.TR_HAS_BUTTONS | wx.TR_HAS_VARIABLE_ROW_HEIGHT,
                 log=None):

        HTL.HyperTreeList.__init__(self, parent, id, pos, size, style)
        
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
            print items
            bmp = wx.ArtProvider_GetBitmap(eval(items), wx.ART_TOOLBAR, (16, 16))
            il.Add(bmp)

        #smileidx = il.Add(images.Smiles.GetBitmap())
        numicons = il.GetImageCount()

        self.AssignImageList(il)
        #self.count = 0
        #self.log = log

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
            #self.SetItemImage(self.root, 13, which=wx.TreeItemIcon_Expanded)
            self.SetItemText(self.root, "col 1 root", 1)
            self.SetItemText(self.root, "col 2 root", 2)
             
            for item, val in remote_configs.items():
                #txt = "Item %d" % x
                
                child = self.AppendItem(self.root, item)
    
                self.SetPyData(child, None)
                self.SetItemText(child, item, 1)
                self.SetItemText(child, item + " (c2)", 2)
                self.SetItemImage(child, 24, which=wx.TreeItemIcon_Normal)
                self.SetItemImage(child, 13, which=wx.TreeItemIcon_Expanded)
                
            
                if isinstance(val,dict):
                    for item2,val in remote_configs[item].items():
                        
                        
                        child2 = self.AppendItem(child, item2)
                        self.SetPyData(child2, None)
                        self.SetItemText(child2, item2[:-1], 1)
                        self.SetItemImage(child2, 24, which=wx.TreeItemIcon_Normal)
                        self.SetItemImage(child2, 13, which=wx.TreeItemIcon_Expanded)
                        if isinstance(val,dict):
                            
                            for item3,val in remote_configs[item][item2].items():
                                
                                child3 = self.AppendItem(child2,item3)
                                
                                self.SetPyData(child3,None)
                                self.SetItemText(child3, item3[:-1], 1)
                                self.SetItemImage(child3, 24, which=wx.TreeItemIcon_Normal)
                                self.SetItemImage(child3, 13, which=wx.TreeItemIcon_Expanded)
                                if isinstance(val,dict):
                                    for item4,val in remote_configs[item][item2][item3].items():
                                        child4 = self.AppendItem(child3,item4)
                                        self.SetPyData(child4,None)
                                        self.SetItemText(child4, item4[:-1], 1)
                                    
                            
def main():
    import nagaratest
    app = nagaratest.FrameTest()
    log = app.log
    frame = app.frame
    
    dlg = wx.Dialog(None, -1, title='Amber Dialog',size =(600,500))
    # paicspanel.MarvinPanel(dlg, -1, 'marvin', log=self.getLog())
    RemotePanel(dlg,-1,size=(500,500))
    dlg.ShowModal()
    dlg.SetSize(dlg.GetBestSize())
    dlg.Destroy()

    # app.MainLoop()

    try:
        app.MainLoop()
    except:
        app.RedirectStdio()


if __name__ == '__main__':
    main()
    
        