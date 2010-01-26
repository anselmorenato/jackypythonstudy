import sys
import wx


class MouseDownTracker(wx.EvtHandler):
    def __init__(self, log):
        wx.EvtHandler.__init__(self)
        self.log = log
        wx.EVT_LEFT_DOWN(self, self.OnMouseDown)

    def OnMouseDown(self, evt):
        pos = evt.GetPosition()
        window = self.GetNextHandler()
        self.log.write("Mouse down at %s on %s\n" % (pos, window.__class__.__name__))
        evt.Skip()


class MyPanel(wx.Panel):
    def __init__(self, parent, Id, log):
        wx.Panel.__init__(self, parent, Id)

        stxt = wx.StaticText(self, -1, "Hello")
        tctl = wx.TextCtrl(self, -1, "What's up Doc?", size=(150,-1))
        btn  = wx.Button(self, -1, "Click Me!")

        stxt.PushEventHandler(MouseDownTracker(sys.stdout))
        tctl.PushEventHandler(MouseDownTracker(sys.stdout))
        btn.PushEventHandler(MouseDownTracker(sys.stdout))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add((25,25))

        row = wx.BoxSizer(wx.HORIZONTAL)
        row.Add((25,1))
        row.Add(stxt, 0, wx.ALL, 5)
        row.Add(tctl, 0, wx.ALL, 5)
        row.Add(btn, 0, wx.ALL, 5)
        sizer.Add(row)

        self.SetSizer(sizer)


app = wx.PySimpleApp()
f = wx.Frame(None, -1, "PushEventHandler Tester", size=(400,350))
p = MyPanel(f, -1, sys.stdout)
p.PushEventHandler(MouseDownTracker(sys.stdout))
f.Show()
app.MainLoop()
