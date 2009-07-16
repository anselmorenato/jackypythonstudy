import wx
import remotepanel
import htlpanel



class MyFrame(wx.Frame):
    '''This is a frame for newpanel test'''    
    def __init__(self, parent, ID):

        wx.Frame.__init__(self, parent, -1)
        panel = remotepanel.RemotePanel(self)
        
        #panel = htlpanel.HyperTreeListPanel(self)


        self.Show()





app = wx.App()

frame = MyFrame(None, -1)
app.MainLoop()
