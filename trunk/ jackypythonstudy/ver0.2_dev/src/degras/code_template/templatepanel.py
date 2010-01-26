import wx
import wx.xrc as xrc


def main():
    logfile =  "_error.log"
    app = wx.App(redirect=False, filename=logfile)
    frame = wx.Frame(None, -1, "TestFrame")
    # panel = wx.Panel(frame,-1)
    panel = MyPanel(frame)
    frame.Show()

    try:
        app.MainLoop()
    except:
        app.RedirectStdio()

if __name__ == '__main__':
    main()

