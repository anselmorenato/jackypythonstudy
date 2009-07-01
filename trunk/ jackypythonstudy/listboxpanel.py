import wx
import  wx.lib.scrolledpanel as scrolled

class MyFrame(wx.Frame):
    def __init__(
            self, parent, ID, title, pos=wx.DefaultPosition,
            size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE
            ):

        wx.Frame.__init__(self, parent, ID, title, pos, size, style)
        panel = wx.Panel(self, -1)
        panel1 = wx.StaticText(panel,-1,"why i cannot do it")
        panel1.SetFont(wx.Font(18,wx.SWISS,wx.NORMAL,wx.BOLD))
        

        listbox = wx.ListBox(panel, size=(100,80),
                        choices="Local Paic Visn three four five six seven eight nine".split())
        scrolledpanel = scrolled.ScrolledPanel(panel, -1, size=(100, 100),
                                 style = wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER, name="scrolledpanel" )
        scrolledpanel.SetBackgroundColour("white")
        spb1 = wx.Button(scrolledpanel, -1, "New")
        spb2 = wx.Button(scrolledpanel, -1, "New")
        spb3 = wx.Button(scrolledpanel, -1, "New")
        spb4 = wx.Button(scrolledpanel, -1, "New")
        spb5 = wx.Button(scrolledpanel, -1, "New")
        spb6 = wx.Button(scrolledpanel, -1, "New")
        spb7 = wx.Button(scrolledpanel, -1, "New")
        
        b1 = wx.Button(panel, -1, "New")
        self.Bind(wx.EVT_BUTTON, self.OnClick, b1)
        b1.SetDefault()
        b1.SetSize(b1.GetBestSize())
        b2 = wx.Button(panel, -1, "Edit")
        self.Bind(wx.EVT_BUTTON, self.OnClick, b2)
        b2.SetDefault()
        b2.SetSize(b2.GetBestSize())
        b3 = wx.Button(panel, -1, "Copy")
        self.Bind(wx.EVT_BUTTON, self.OnClick, b3)
        b3.SetDefault()
        b3.SetSize(b3.GetBestSize())
        
        

        mainsizer = wx.BoxSizer(wx.VERTICAL)
        mainsizer.Add(panel1, 0, wx.ALIGN_LEFT|wx.ALL, 5)
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1_sp = wx.BoxSizer(wx.VERTICAL)
        sizer_1_sp.Add(spb1)
        sizer_1_sp.Add(spb2)
        sizer_1_sp.Add(spb3)
        sizer_1_sp.Add(spb4)
        sizer_1_sp.Add(spb5)
        sizer_1_sp.Add(spb6)
        sizer_1_sp.Add(spb7)
        
        scrolledpanel.SetSizer(sizer_1_sp)
        scrolledpanel.SetupScrolling()
        
        sizer_1.Add(listbox, 0, wx.ALIGN_LEFT,5)
        #sizer_1.Add(sizer_1_sp,0,wx.ALIGN_CENTER|wx.ALL,5)
        sizer_1.Add(scrolledpanel,0,wx.ALIGN_CENTER,5)
        sizer_1_bt = wx.BoxSizer(wx.VERTICAL)
        sizer_1_bt.Add(b1)
        sizer_1_bt.Add(b2)
        sizer_1_bt.Add(b3)
        
        sizer_1.Add(sizer_1_bt,0,wx.ALIGN_RIGHT|wx.ALL,5)
        
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        
        mainsizer.Add(sizer_1,0,wx.EXPAND|wx.ALL, 5)
        
        
        panel.SetSizer(mainsizer)
        mainsizer.Fit(self)
        mainsizer.SetSizeHints(self)
        
        self.Show()
        
    def OnClick(self, event): pass


    
        
app = wx.App()
frame = MyFrame(None, -1, "This is a wx.Frame", size=(350, 600),
                  style = wx.DEFAULT_FRAME_STYLE)
#frame.Show()
app.MainLoop()
