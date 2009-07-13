
import wx
import htlpanel 

class RemotePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self,parent,-1)
        
        #splitter = wx.SplitterWindow(self, -1, style=wx.CLIP_CHILDREN | wx.SP_LIVE_UPDATE | wx.SP_3D)
        #panel = wx.Panel(splitter, -1, style=wx.WANTS_CHARS)
          
        listbox = wx.ListBox(self, size=(200,100),
                       choices="Local Paic Visn three four five six seven eight nine".split())
        htl = htlpanel.HyperTreeListPanel(self)
        okBtn = wx.Button(self, -1, "Save")
        cancelBtn = wx.Button(self, -1, "Cancel")
        
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
        
        

        mainsizer = wx.BoxSizer(wx.VERTICAL)
        
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
                                
        sizer_1.Add(listbox, 1, wx.EXPAND,5)
        
        
        sizer_1_bt = wx.BoxSizer(wx.VERTICAL)
        sizer_1_bt.Add(b1)
        sizer_1_bt.Add(b2)
        sizer_1_bt.Add(b3)
        
        sizer_1.Add(sizer_1_bt,0,wx.ALIGN_RIGHT|wx.ALL,5)
        
        
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(okBtn,0,wx.ALIGN_RIGHT,5)
        sizer_2.Add(cancelBtn,0,wx.ALIGN_RIGHT,5)
                
        mainsizer.Add(sizer_1,0,wx.ALIGN_CENTER, 5)
        mainsizer.Add(htl,1,wx.EXPAND,5)
        mainsizer.Add(sizer_2,0,wx.ALIGN_RIGHT, 5)
        
        
        self.SetSizer(mainsizer)
        mainsizer.Fit(self)
        mainsizer.SetSizeHints(self)
        
    def OnClick(self, event): pass