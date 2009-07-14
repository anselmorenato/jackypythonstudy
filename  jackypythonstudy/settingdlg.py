import wx
import htlpanel

########################################################################
class SettingDialog(wx.Notebook):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent, id):
        panel = wx.Panel(self)
        wx.Notebook.__init__(self, panel, id, size=(21,21), style=
                             wx.BK_DEFAULT
                             #wx.BK_TOP 
                             #wx.BK_BOTTOM
                             #wx.BK_LEFT
                             #wx.BK_RIGHT
                             # | wx.NB_MULTILINE
                             )
        

        win = htlpanel.HyperTreeListPanel(panel)
        self.AddPage(win, "Blue")
       
        win = htlpanel.HyperTreeListPanel(panel)
        self.AddPage(win, "green")
    
        
    
app = wx.App()
frame = wx.Frame(None)
frame.Show()
app.MainLoop()