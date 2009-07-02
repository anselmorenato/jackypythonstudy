import wx
import remotepanel



class MyFrame(wx.Frame):
    '''This is a frame for newpanel test'''    
    def __init__(self, parent, ID, title, pos=wx.DefaultPosition,size=wx.DefaultSize):

        wx.Frame.__init__(self, parent, ID, title, pos, size)
        panel = remotepanel.RemotePanel(self)


        self.Show()





app = wx.App()

frame = MyFrame(None, -1, "This is a Panel test Frame", size=(350, 300))
#frame.Show()
app.MainLoop()
