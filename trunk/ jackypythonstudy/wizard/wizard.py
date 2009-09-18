#! /usr/bin/env python
# _*_ coding: utf-8 _*_
# Copyright (C)  2009 Biao Ma

import sys, os
#import exception
import wx
import wx.wizard as wiz
import images

#-------------------------------------------------------------------------------
def make_page_title(wizPg, title):
    sizer = wx.BoxSizer(wx.VERTICAL)
    wizPg.SetSizer(sizer)
    title = wx.StaticText(wizPg, -1, title)
    title.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL,wx.BOLD))
    sizer.Add(title, 0, wx.ALIGN_LEFT|wx.ALL, 5)
    sizer.Add(wx.StaticLine(wizPg, -1), 0, wx.EXPAND|wx.ALL, 5)
    return sizer

#-------------------------------------------------------------------------------
class TitledPage(wiz.WizardPageSimple):
    def __init__(self, parent, title):
        wiz.WizardPageSimple.__init__(self, parent)
        self.sizer = make_page_title(self, title)
        
        
class MyFrame(wx.Frame):
    
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title)
        
        panel = wx.Panel(self)

        btn = wx.Button(panel, -1, 'Run Test Wizard', pos=(50,50))
        panel.Bind(wx.EVT_BUTTON, self.OnRunWizard, btn)
    
    def OnRunWizard(self, evt):
        # Create the wizard and the pages
        image = wx.Bitmap('..\images\Nagara_setup.jpg',wx.BITMAP_TYPE_JPEG)
        wizard = wiz.Wizard(self, -1, "Simple Wizard", image)
        page1 = TitledPage(wizard, "Page 1")
        page2 = TitledPage(wizard, "License Agreement")
        page3 = TitledPage(wizard, "Page 3")
        page4 = TitledPage(wizard, "Page 4")
        self.page1 = page1

        page1.sizer.Add(wx.StaticText(page1, -1, """
This wizard is totally useless, but is meant to show how to
chain simple wizard pages together in a non-dynamic manner.
IOW, the order of the pages never changes, and so the
wxWizardPageSimple class can easily be used for the pages."""))
        wizard.FitToPage(page1)
        page2.sizer.Add(wx.StaticText(page2,-1,'''License Agreement
        
        '''))
        page4.sizer.Add(wx.StaticText(page4, -1, "\nThis is the last page."))

        # Use the convenience Chain function to connect the pages
        wiz.WizardPageSimple_Chain(page1, page2)
        wiz.WizardPageSimple_Chain(page2, page3)
        wiz.WizardPageSimple_Chain(page3, page4)

        wizard.GetPageAreaSizer().Add(page1)
        if wizard.RunWizard(page1):
            wx.MessageBox("Wizard completed successfully", "That's all folks!")
        else:
            dlg = wx.MessageDialog(self,'''Setup is not complete.If you exit now,the program will not be installed.
You may run Setup again at another time to complete the installation.
Exit Setup?''','Exit Setup',
              style = wx.OK|wx.CANCEL|wx.ICON_QUESTION
                          )
            if dlg.ShowModal()== wx.ID_OK:
                wx.MessageBox("Wizard was cancelled", "That's all folks!")

        
def main():
    logfile =  "_error.log"
    app = wx.App(redirect=False, filename=logfile)
    frame = MyFrame(None, 'Wizard Test')
    frame.Show()

    try:
        app.MainLoop()
    except:
        app.RedirectStdio()

if __name__ == '__main__':
    main()