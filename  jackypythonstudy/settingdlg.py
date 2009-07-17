import wx
import htlpanel

########################################################################
class SettingDialog(wx.Frame):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent, id):
        wx.Frame.__init__(self,parent,-1,'Setting Dialog',size=(500,450))
        
        panel = wx.Panel(self)
        nb = wx.Notebook(panel, id, size=(21,21), style=
                             wx.BK_DEFAULT
                             #wx.BK_TOP 
                             #wx.BK_BOTTOM
                             #wx.BK_LEFT
                             #wx.BK_RIGHT
                             # | wx.NB_MULTILINE
                             )
        
        win = htlpanel.HyperTreeListPanel(nb)
        nb.AddPage(win, "Local")
       
        win = htlpanel.HyperTreeListPanel(nb)
        nb.AddPage(win, "Remote")
        
        self.CenterOnParent()
        self.SetMinSize((400,400))
        
        okBtn = wx.Button(panel, -1, "Save")
        cancelBtn = wx.Button(panel, -1, "Cancel")
        
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(okBtn,0,wx.ALIGN_RIGHT,5)
        sizer_2.Add(cancelBtn,0,wx.ALIGN_RIGHT,5)
        
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        mainsizer.Add(nb,1,wx.EXPAND,5)
        mainsizer.Add(sizer_2,0,wx.ALIGN_RIGHT, 5)
        
        
        
        panel.SetSizer(mainsizer)
        mainsizer.Fit(panel)
        mainsizer.SetSizeHints(panel)
    
        
if __name__ =='__main__':

    app = wx.App()
    frame = SettingDialog(None,-1)
    frame.Show()
    app.MainLoop()