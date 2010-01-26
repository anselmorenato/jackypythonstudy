# _*_ coding: utf-8 _*_
# Copyright (C)  2009 Takakazu Ishikura

import sys, os
import exception
import wx
import wx.wizard as wiz

#-------------------------------------------------------------------------------

class Wizard(wiz.Wizard):

    """
    Wizard class
    """

    def __init__(self, id, title, image=None, log=None):
        """Constructor."""
        wiz.Wizard.__init__(self, None, -1, title)
        # __init__(self, parent, id, title, bitmap, pos, style)
        # if image:
        #     image_ctrl = wx.StaticBitmap(self, -1, image)

        self._wizard_pages = None
        self.log = log

        self.initBinds()

    def initBinds(self):
        """Initialize the binds."""
        self.Bind(wiz.EVT_WIZARD_PAGE_CHANGED, self.OnWizPageChanged)
        self.Bind(wiz.EVT_WIZARD_PAGE_CHANGING, self.OnWizPageChanging) 
        self.Bind(wiz.EVT_WIZARD_CANCEL, self.OnWizCancel)

    def OnWizPageChanging(self, event):
        pass

    def OnWizPageChanged(self, event):
        pass

    def OnWizCancel(self, event):
        page = event.GetPage()
        comment = 'Wizard was canceled: %s\n' % page.GetName()
        if self.log:
            self.log.write(comment)
        else:
            print(comment)

    def OnWizFinished(self, event):
        comment = 'Wizard was finished completely.'
        if self.log:
            self.log.write(comment)
        else:
            print(comment)

    def setPages(self, pages):
        """Set the panels and make the wizard widget."""
        self._wizard_pages = [ WizardPage(self, p) for p in pages ] 

        nwp = len(self._wizard_pages)
        if nwp == 0:
            prev = None
            curr = self._wizard_pages[0]
            next = None

            curr.setPrev(prev)
            curr.setNext(next)
        else:
            for iwp in range(nwp):
                if iwp==0:
                    prev = None
                    curr = self._wizard_pages[0]
                    next = self._wizard_pages[1]
                elif iwp==nwp-1:
                    prev = self._wizard_pages[-2]
                    curr = self._wizard_pages[-1]
                    next = None
                else:
                    prev = self._wizard_pages[iwp-1]
                    curr = self._wizard_pages[iwp]
                    next = self._wizard_pages[iwp+1]
                curr.SetPrev(prev)
                curr.SetNext(next)

    def getPages(self):
        """Return the pages in this wizard."""
        self._wizard_pages
        return 

    def run(self):
        """Start this wizard."""
        page1 = self._wizard_pages[0]
        self.GetPageAreaSizer().Add(page1)
        self.FitToPage(page1)
        if self.RunWizard(page1):
            wx.MessageBox('Wizard completed successfully', "That's all folks!")
        else:
            wx.MessageBox('Wizard was conceled', "That's all folks!")

    def setFstLst(self, text_fst, text_lst):
        """Set the comment into first page and last page
        if you would like to.
        """
        page_fst = self._wizard_pages[0]
        page_lst = self._wizard_pages[-1]
        page_fst.sizer.Add(wx.StaticText(page_fst, -1, text_fst))
        page_lst.sizer.Add(wx.StaticText(page_lst, -1, text_lst))

#-------------------------------------------------------------------------------

class WizardPage(wiz.PyWizardPage):

    """
    WizardPage class
    """

    def __init__(self, parent, page, image=None, skip=False):
        """Constructor."""
        wiz.PyWizardPage.__init__(self, parent)
        self._page = page
        self._next = None
        self._prev = None
        self.sizer = self.makePageTitle()

        self._image = image

        # self.cb = wx.CheckBox(seelf, -1, 'Skip next page')
        # self.sizer.Add(wx.Panel(self, -1), 0, wx.ALL, 5)
        self.sizer.Add(self._page, 0, wx.ALL, 5)

    def SetNext(self, next_page):
        """Set the next page."""
        self._next = next_page

    def SetPrev(self, prev_page):
        """Set the previous page."""
        self._prev = prev_page

    def GetNext(self):
        """Return the next page, overriding parent class."""
        return self._next

    def GetPrev(self):
        """Return the previous page, overriding parent class."""
        return self._prev

    def GetBitmap(self):
        """Return the image, overriding parent class."""
        if self._image:
            return self._image

    def makePageTitle(self):
        """Make the title of this wizard page."""
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        title = wx.StaticText(self, -1, self._page.GetName())
        title.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        sizer.Add(title, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.ALL, 5)
        return sizer


#-------------------------------------------------------------------------------

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title)

        btn = wx.Button(self, -1, 'Run Test Wizard', pos=(50,50))
        self.Bind(wx.EVT_BUTTON, self.OnRunWizard, btn)

    def OnRunWizard(self, event):
        image = wx.Image('..\images\Nagaragawa_Gujo-Minami.jpg')
        wizard = Wizard(-1, 'Test Wizard', image)
        #wizard = Wizard(-1, 'Test Wizard', image=image, log)
        panel1 = wx.Panel(wizard, -1, name='page 1')
        panel2 = wx.Panel(wizard, -1, name='page 2')
        panel3 = wx.Panel(wizard, -1, name='page 3')
        panel4 = wx.Panel(wizard, -1, name='page 4')
        panel5 = wx.Panel(wizard, -1, name='page 5')

        print 1
        wizard.setPages([panel1, panel2, panel3, panel4, panel5])
        print 2
        wizard.run()
        print 3



#-------------------------------------------------------------------------------

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




