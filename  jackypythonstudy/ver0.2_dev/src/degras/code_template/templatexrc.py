import wx
import wx.xrc as xrc

class MyPanel(wx.Panel):
    def __init__(self, parent):
        self.res = xrc.XmlResource('configremote.xrc')
        pre = wx.PrePanel()
        self.res.LoadOnPanel(pre, parent, 'ConfigRemote')
        self.PostCreate(pre)

def main():
    logfile =  "_error.log"
    app = wx.App(redirect=False, filename=logfile)
    frame = wx.Frame(None, -1, "TestFrame")
    panel = MyPanel(frame)
    frame.Show()

    try:
        app.MainLoop()
    except:
        app.RedirectStdio()

if __name__ == '__main__':
    main()
