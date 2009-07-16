import wx
import htlpanel

########################################################################
class SettingDialog(wx.Frame):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent, id):
        wx.Frame.__init__(self,parent,-1,'Setting dialog',size=(500,450))
        
        #panel = wx.Panel(self)
        nb = wx.Notebook(self, id, size=(30,30), style=
                             wx.BK_DEFAULT
                             #wx.BK_TOP 
                             #wx.BK_BOTTOM
                             #wx.BK_LEFT
                             #wx.BK_RIGHT
                             # | wx.NB_MULTILINE
                             )
        

        win = htlpanel.HyperTreeListPanel(nb)
        nb.AddPage(win, "Blue")
       
        win = htlpanel.HyperTreeListPanel(nb)
        nb.AddPage(win, "green")
        
        self.CenterOnParent()
    
        
    
app = wx.App()
frame = SettingDialog(None,-1)
frame.Show()
app.MainLoop()