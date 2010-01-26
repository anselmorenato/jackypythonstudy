#  -*- encoding: utf-8 -*-
import os, sys

import wx

class MyApp(wx.PySimpleApp):
    def OnInit(self):
        self.Frm = wx.Frame(None, -1, "wxPython", size=(200,120))
        self.Frm.Show()
        self.StTxt = wx.StaticText(self.Frm, -1, "ARIA", pos=(20,10))
        self.StTxt.Bind(wx.EVT_CONTEXT_MENU, self.OnRClick)
        self.StTxt.Bind(wx.EVT_MENU, self.OnRMenu)

        ID100 = wx.NewId()
        ID101 = wx.NewId()
        self.Menu = wx.Menu()
        self.Menu.Append(ID100, "Alicia", "Alicia")
        self.Menu.Append(ID101, "Akari", "Akari")

        return 1

    def OnRClick(self, event):
        self.StTxt.PopupMenu(self.Menu)

    def on_menu_item(self, event):
        MenuId = event.GetId()
        MenuObj = event.GetEventObject()
        MenuLabel = MenuObj.GetLabel(MenuId)
        self.StTxt.SetLabel(MenuLabel)

app = MyApp()
app.MainLoop()
