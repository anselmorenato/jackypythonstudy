import wx
import remotepanel
import htlpanel
import setglobalpanel



class MyFrame(wx.Frame):
    '''This is a frame for newpanel test'''    
    def __init__(self, parent, ID):

        wx.Frame.__init__(self, parent, -1,size=(600,500))
        #panel = remotepanel.RemotePanel(self)
        
        #panel = htlpanel.HyperTreeListPanel(self)
        
        panel = setglobalpanel.SetGlobalPanel(self,-1)


        self.Show()





app = wx.App()

frame = MyFrame(None, -1)
app.MainLoop()
