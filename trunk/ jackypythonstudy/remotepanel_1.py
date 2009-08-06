
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
choice =['vlsn','rccs','lacal','email','phcs']#item = None
        
class RemotePanel(wx.Panel):
    def __init__(self, parent,id,size):
        wx.Panel.__init__(self,parent,-1)
        
        self.listbox = wx.ListBox(self, size = (130,50),choices=choice)
        index = self.listbox.SetSelection(0)
        self.listbox.SetFont(wx.Font(11,wx.SWISS,wx.NORMAL,wx.NORMAL))
        self.listbox.Bind(wx.EVT_LISTBOX_DCLICK, self.EvtListBoxDClick, self.listbox)
        self.listbox.Bind(wx.EVT_LISTBOX, self.EvtListBox, self.listbox)
        
        self.tree = HyperTreeList(self,-1,size=(800,800),style=wx.TR_DEFAULT_STYLE)
        self.root = self.tree.root
        
        self.okBtn = wx.Button(self, -1, "Ok")
        self.cancelBtn = wx.Button(self, -1, "Cancel")
        self.Bind(wx.EVT_BUTTON, self.OnCancel, self.cancelBtn)
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
        
    def Dolayout(self):
              
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1_lb = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'ListBox'), orient=wx.VERTICAL)
        sizer_1_bt = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Edit Botton'),orient = wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_1_lb.Add(self.listbox,1,wx.EXPAND,5)                        
        sizer_1.Add(sizer_1_lb, 1, wx.EXPAND|wx.ALL,5)

        sizer_1_bt.Add(self.b1,0,wx.EXPAND|wx.ALL)
        sizer_1_bt.Add(self.b2,0,wx.EXPAND|wx.ALL)
        sizer_1_bt.Add(self.b3,0,wx.EXPAND|wx.ALL)
        sizer_1_bt.Add(self.b4,0,wx.EXPAND|wx.ALL)
        sizer_1.Add((80,-1))
        sizer_1.Add(sizer_1_bt,0,wx.EXPAND|wx.ALL,5)

        sizer_2.Add(self.okBtn,0,wx.ALIGN_RIGHT,5)
        sizer_2.Add(self.cancelBtn,0,wx.ALIGN_RIGHT,5)


        sizer_tree = wx.BoxSizer(wx.VERTICAL)
        sizer_tree.Add(self.tree,0,wx.EXPAND,5)

        
        #mainsizer.Add((5,20),wx.EXPAND,5)
        mainsizer.Add(sizer_1,0,wx.ALIGN_CENTER, 5)
        #mainsizer.Add((5,20),wx.EXPAND,5)
        mainsizer.Add(sizer_tree,0,wx.EXPAND,5)
        mainsizer.Add(sizer_2,0,wx.ALIGN_RIGHT, 5)
        

        self.SetSizer(mainsizer)
        mainsizer.Fit(self)

        
        
        
        self.SetSizer(mainsizer)
        #mainsizer.Fit(self)
        #self.SetAutoLayout(True)

        #sizer.SetSizeHints(self)

        mainsizer.Layout()
    def OnClick(self, event): 
        pass

        #sizer.Layout()
    def OnClick(self, event): pass

    def OnCancel(self,event):
        self.Close()
    
    #----------------------------------------------------------------------
    def OnAddNewListItem(self,event):
        self.listbox.Insert('new',5)
        
    def OnEditListItem():
        pass
    def OnCopyListItem():
        pass
    def OnDeleteListItem():
        pass
    
    def EvtListBoxDClick(self,event):
        """"""
        lb = event.GetEventObject()
        tag = lb.GetSelection()
        if tag == 2:
            import settingdlg
            dlg = settingdlg.SettingDialog(None,-1)
            dlg.Show()
            event.Skip()
    def EvtListBox(self,event):
        '''
        '''
        self.root = self.tree.SetItemText(self.tree.GetRootItem(),event.GetString()) 
        
        #self.tree.SetItemText(self.tree.GetItemText(1),event.GetString())
        #item = self.tree.SetItemText(self.tree.GetFirstChild(),event.GetString())#event.GetString()
        #self.text = parent.GetParent().rightPanel.text
        #item = event.GetString()

class HyperTreeList(HTL.HyperTreeList):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 style=wx.TR_HAS_BUTTONS | wx.TR_HAS_VARIABLE_ROW_HEIGHT,
                 log=None):

        HTL.HyperTreeList.__init__(self, parent, id, pos, size, style)
       
        il = wx.ImageList(16, 16)

        for items in ArtIDs[1:-1]:
            print items
            bmp = wx.ArtProvider_GetBitmap(eval(items), wx.ART_TOOLBAR, (16, 16))
            il.Add(bmp)

        #smileidx = il.Add(images.Smiles.GetBitmap())
        numicons = il.GetImageCount()
        self.AssignImageList(il)

        # create some columns
        self.AddColumn("Main column")
        self.AddColumn("Column 1")
        self.AddColumn("Column 2")
        self.SetMainColumn(0) # the one with the tree in it...
        self.SetColumnWidth(0, 175)
        

        self.root = self.AddRoot('vlsn')

        
        self.SetPyData(self.root, None)
        self.SetItemImage(self.root, 24, which=wx.TreeItemIcon_Normal)
        self.SetItemImage(self.root, 13, which=wx.TreeItemIcon_Expanded)
        self.SetItemText(self.root, "col 1 root", 1)
        self.SetItemText(self.root, "col 2 root", 2)
        
        
        for item, val in remote_configs.items():
                       
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
    

    dlg = wx.Dialog(None, -1, title='Amber Dialog',size =(600,600))
    
    remote = RemotePanel(dlg,-1,'size')
    

    dlg = wx.Dialog(None, -1, title='Amber Dialog',size =(500,500))
    # paicspanel.MarvinPanel(dlg, -1, 'marvin', log=self.getLog())
    remote=RemotePanel(dlg,-1,size=(500,500))
    dlg.ShowModal()

    #dlg.SetSize(dlg.GetBestSize())
    dlg.ShowModal()
    dlg.Destroy()
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(remote,0,wx.EXPAND)
    dlg.SetSizer(sizer)
    sizer.Fit(dlg)
    dlg.SetAutoLayout(True)
                    

    try:
        app.MainLoop()
    except:
        app.RedirectStdio()


if __name__ == '__main__':
    main()
    
   
    
        
