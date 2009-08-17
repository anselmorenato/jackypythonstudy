#!/usr/bin/python

# timezone.py 

import wx
from time import *

class Listbox(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)

        zone_list = ['CET', 'GMT', 'MSK', 'EST', 'PST', 'EDT']

        self.full_list = {
            'CET': 'Central European Time',
            'GMT': 'Greenwich Mean Time',
            'MSK': 'Moscow Time',
            'EST': 'Eastern Standard Time',
            'PST': 'Pacific Standard Time',
            'EDT': 'Eastern Daylight Time'
        }

        self.time_diff = {
            'CET' : 1,
            'GMT' : 0,
            'MSK': 3,
            'EST': -5,
            'PST': -8,
            'EDT': -4
        }

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)

        self.timer = wx.Timer(self, 1)
        self.diff = 0

        #panel = wx.Panel(self, -1)

        self.time_zones = wx.ListBox(self, 26, (-1, -1), (170, 130), 
		zone_list, wx.LB_SINGLE)
        self.time_zones.SetSelection(0)
        self.text = wx.TextCtrl(self, -1, 'Central European Time', 
		size=(200, 130), style=wx.TE_MULTILINE)
        self.time = wx.StaticText(self, -1, '')
        btn = wx.Button(self, wx.ID_CLOSE, 'Close')
        hbox1.Add(self.time_zones, 0, wx.TOP, 40)
        hbox1.Add(self.text, 1, wx.LEFT | wx.TOP, 40)
        hbox2.Add(self.time, 1, wx.ALIGN_CENTRE)
        hbox3.Add(btn, 0, wx.ALIGN_CENTRE)
        vbox.Add(hbox1, 0, wx.ALIGN_CENTRE)
        vbox.Add(hbox2, 1, wx.ALIGN_CENTRE)
        vbox.Add(hbox3, 1, wx.ALIGN_CENTRE)
		
        self.SetSizer(vbox)
        vbox.Fit(self)
        self.timer.Start(100)

        wx.EVT_BUTTON(self, wx.ID_CLOSE, self.OnClose)
        wx.EVT_LISTBOX(self, 26, self.OnSelect)
        wx.EVT_TIMER(self, 1, self.OnTimer)

        #self.Show(True)
        #self.Centre()

    def OnClose(self, event):
        self.Close()

    def OnSelect(self, event):
        index = event.GetSelection()
        time_zone = self.time_zones.GetString(index)
        self.diff = self.time_diff[time_zone]
        self.text.SetValue(self.full_list[time_zone])

    def OnTimer(self, event):
        ct = gmtime()
        print_time = (ct[0], ct[1], ct[2], ct[3]+self.diff, 
			ct[4], ct[5], ct[6], ct[7], -1)
        self.time.SetLabel(strftime("%H:%M:%S", print_time))
        event.Skip()


def main():
    import nagaratest
    app = nagaratest.FrameTest()
    log = app.log
    frame = app.frame
    
    dlg = wx.Dialog(None, -1, title='Amber Dialog',size =(700,500),style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
    
    time =Listbox(dlg,-1)
    
    #dlg.SetSize(dlg.GetBestSize())
    
    #sizer = wx.BoxSizer(wx.VERTICAL)
    #sizer.Add(remote,0,wx.EXPAND)
    #dlg.SetSizer(sizer)
    #sizer.Fit(dlg)
    #dlg.SetAutoLayout(True)
    dlg.ShowModal()                
    
    dlg.Destroy()
    # app.MainLoop()

    try:
        app.MainLoop()
    except:
        app.RedirectStdio()


if __name__ == '__main__':
    main()