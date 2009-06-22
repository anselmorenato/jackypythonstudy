import wx
import wx.lib.colourselect as csel
import random

import os
import sys

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

bitmapDir = os.path.join(dirName, 'bitmaps')
sys.path.append(os.path.split(dirName)[0])

try:
    from agw import labelbook as LB
    from agw.fmresources import *
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.labelbook as LB
    from wx.lib.agw.fmresources import *

#import images

_pageTexts = ["Hello", "From", "wxPython", "LabelBook", "Demo"]
_pageIcons = ["roll.png", "charge.png", "add.png", "decrypted.png", "news.png"]
_pageColours = [wx.RED, wx.GREEN, wx.WHITE, wx.BLUE, "Pink"]

#----------------------------------------------------------------------
#class SamplePane(wx.Panel):
#    """
#    Just a simple test window to put into the LabelBook.
#    """
#    def __init__(self, parent, colour, label):

#        wx.Panel.__init__(self, parent, style=wx.BORDER_SUNKEN)
#        self.SetBackgroundColour(colour)

#        label = label + "\nEnjoy the LabelBook && FlatImageBook demo!"
 #       static = wx.StaticText(self, -1, label, pos=(10, 10))        

#----------------------------------------------------------------------

class LabelBookDemo(wx.Frame):

    def __init__(self, parent, log):

        wx.Frame.__init__(self, parent)

        self.initializing = True

        self.log = log

        #self.splitter = wx.SplitterWindow(self, -1, style=wx.SP_3D|wx.SP_BORDER|
        #wx.SP_LIVE_UPDATE|wx.SP_3DSASH)
        self.mainpanel = wx.Panel(self, -1)
        #self.leftpanel = wx.Panel(self.splitter, -1, style=wx.SUNKEN_BORDER)

        #self.sizer_3_staticbox = wx.StaticBox(self.leftpanel, -1, "Book Styles")
        #self.sizer_4_staticbox = wx.StaticBox(self.leftpanel, -1, "Colours")

        
        
     
        
        self.SetProperties()
        self.CreateLabelBook()
        self.DoLayout()

       

       

        

        self.Bind(LB.EVT_IMAGENOTEBOOK_PAGE_CHANGING, self.OnPageChanging)
        self.Bind(LB.EVT_IMAGENOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(LB.EVT_IMAGENOTEBOOK_PAGE_CLOSING, self.OnPageClosing)
        self.Bind(LB.EVT_IMAGENOTEBOOK_PAGE_CLOSED, self.OnPageClosed)


        statusbar = self.CreateStatusBar(2, wx.ST_SIZEGRIP)
        statusbar.SetStatusWidths([-2, -1])
        # statusbar fields
        statusbar_fields = [("LabelBook & FlatImageBook wxPython Demo, Andrea Gavana @ 03 Nov 2006"),
                            ("Welcome To wxPython!")]

        for i in range(len(statusbar_fields)):
            statusbar.SetStatusText(statusbar_fields[i], i)

        self.CreateMenu()

        self.SetSize((800,700))

        #self.SetIcon(images.Mondrian.GetIcon())  
        self.CenterOnScreen()

        self.initializing = False
        self.SendSizeEvent()


    def SetProperties(self):

        self.SetTitle("LabelBook & FlatImageBook wxPython Demo ;-)")
        #sself.pin.SetValue(1)
        #self.mainpanel.SetMinimumPaneSize(120)


    def DoLayout(self):

        mainsizer = wx.BoxSizer(wx.VERTICAL)
        panelsizer = wx.BoxSizer(wx.VERTICAL)
        #leftsizer = wx.BoxSizer(wx.VERTICAL)
        

        

        

        
       

        #self.leftpanel.SetSizer(leftsizer)
        #leftsizer.Layout()
        #leftsizer.SetSizeHints(self.leftpanel)
        #leftsizer.Fit(self.leftpanel)

        panelsizer.Add(self.book, 1, wx.EXPAND, 0)
        self.mainpanel.SetSizer(panelsizer)
        panelsizer.Layout()

        #self.splitter.SplitVertically( self.mainpanel, 200)
        mainsizer.Add(self.mainpanel, 1, wx.EXPAND, 0)

        self.SetSizer(mainsizer)
        mainsizer.Layout()
        self.Layout()


    def CreateLabelBook(self, btype=0):

        if not self.initializing:
            self.Freeze()
            panelsizer = self.mainpanel.GetSizer()
            panelsizer.Detach(0)
            self.book.Destroy()
        else:
            self.imagelist = self.CreateImageList()

        style = self.GetBookStyles()

        if btype == 0: # it is a labelbook:
            self.book = LB.LabelBook(self.mainpanel, -1, style=style)
            #if self.bookdirection.GetSelection() > 1:
            #    self.bookdirection.SetSelection(0)

            #self.SetUserColours()                

        else:
            self.book = LB.FlatImageBook(self.mainpanel, -1, style=style)

        #self.EnableChoices(btype)            

        self.book.AssignImageList(self.imagelist)

        for indx, txts in enumerate(_pageTexts):
            #label = "This is panel number %d"%(indx+1)
            self.book.AddPage(TestPanel(self.book, _pageColours[indx]),
                              txts, True, indx)

        self.book.SetSelection(0)            

        if not self.initializing:
            panelsizer.Add(self.book, 1, wx.EXPAND)
            panelsizer.Layout()
            self.GetSizer().Layout()
            self.Layout()
            self.Thaw()

        self.SendSizeEvent()


    


    def GetBookStyles(self):

        style = INB_FIT_BUTTON
        #style = self.GetBookOrientation(style)

        #style = INB_WEB_HILITE
        #style = INB_USE_PIN_BUTTON
        
        #style = INB_BORDER
        style = INB_SHOW_ONLY_TEXT
        '''if self.onlytext.IsEnabled() and self.onlytext.GetValue():
            style |= INB_SHOW_ONLY_TEXT
        if self.onlyimages.IsEnabled() and self.onlyimages.GetValue():
            style |= INB_SHOW_ONLY_IMAGES
        if self.pin.GetValue():
            style |= INB_USE_PIN_BUTTON
        if self.shadow.GetValue():
            style |= INB_DRAW_SHADOW
        if self.web.GetValue():
        style |= INB_WEB_HILITE
        if self.gradient.GetValue():
            style |= INB_GRADIENT_BACKGROUND
        if self.border.GetValue():
            style |= INB_BORDER
        '''
        return style            


    def CreateImageList(self):

        imagelist = wx.ImageList(32, 32)
        for img in _pageIcons:
            newImg = os.path.join(bitmapDir, "lb%s"%img)
            bmp = wx.Bitmap(newImg, wx.BITMAP_TYPE_PNG)
            imagelist.Add(bmp)

        return imagelist


    def GetBookOrientation(self, style):

        style |= INB_LEFT #selection = self.bookdirection.GetSelection()
        #if selection == 0:
            
        #elif selection == 1:
        #style |= INB_RIGHT
        #elif selection == 2:
        #    style |= INB_TOP
        #else:
        #    style |= INB_BOTTOM

        return style


    def OnBookType(self, event):

        self.CreateLabelBook(event.GetInt())
        event.Skip()


    def OnBookOrientation(self, event):

        style = self.GetBookStyles()
        self.book.SetWindowStyleFlag(style)

        event.Skip()


    def OnStyle(self, event):

        style = self.GetBookStyles()
        self.book.SetWindowStyleFlag(style)

        event.Skip()


    def OnBookColours(self, event):

        obj = event.GetId()
        colour = event.GetValue()

        if obj == self.background.GetId():
            self.book.SetColour(INB_TAB_AREA_BACKGROUND_COLOR, colour)
        elif obj == self.activetab.GetId():
            self.book.SetColour(INB_ACTIVE_TAB_COLOR, colour)
        elif obj == self.tabsborder.GetId():
            self.book.SetColour(INB_TABS_BORDER_COLOR, colour)
        elif obj == self.textcolour.GetId():
            self.book.SetColour(INB_TEXT_COLOR, colour)
        elif obj == self.activetextcolour.GetId():
            self.book.SetColour(INB_ACTIVE_TEXT_COLOR, colour)
        else:
            self.book.SetColour(INB_HILITE_TAB_COLOR, colour)

        self.book.Refresh()


    


    def OnPageChanging(self, event):

        oldsel = event.GetOldSelection()
        newsel = event.GetSelection()
        #self.log.write("Page Changing From: " + str(oldsel) + " To: " + str(newsel) + "\n")
        event.Skip()


    def OnPageChanged(self, event):

        newsel = event.GetSelection()
        #self.log.write("Page Changed To: " + str(newsel) + "\n")
        event.Skip()


    def OnPageClosing(self, event):

        newsel = event.GetSelection()
        #self.log.write("Closing Page: " + str(newsel) + "\n")
        event.Skip()


    def OnPageClosed(self, event):

        newsel = event.GetSelection()
        #self.log.write("Closed Page: " + str(newsel) + "\n")
        event.Skip()


    def OnAddPage(self, event):

        pageCount = self.book.GetPageCount()
        indx = random.randint(0, 4)
        label = "This is panel number %d"%(pageCount+1)
        #self.book.AddPage(TestPanel(self.book, _pageColours[indx], label),
        #                  "Added Page", True, indx)

        self.book.AddPage(TestPanel(self.book, _pageColours[indx]),
                              txts, True, indx)

    def OnDeletePage(self, event):

        msg = "Please Enter The Page Number You Want To Remove:"
        dlg = wx.TextEntryDialog(self, msg, "Enter Page")

        if dlg.ShowModal() != wx.ID_OK:
            dlg.Destroy()
            return

        userString = dlg.GetValue()
        dlg.Destroy()

        try:
            page = int(userString)
        except:
            return

        if page < 0 or page > self.book.GetPageCount() - 1:
            return

        self.book.DeletePage(page)


    def OnDeleteAllPages(self, event):

        self.book.DeleteAllPages()        


    def CreateMenu(self):

        menuBar = wx.MenuBar(wx.MB_DOCKABLE)
        fileMenu = wx.Menu()
        editMenu = wx.Menu()
        helpMenu = wx.Menu()

        item = wx.MenuItem(fileMenu, wx.ID_ANY, "E&xit")
        self.Bind(wx.EVT_MENU, self.OnQuit, item)
        fileMenu.AppendItem(item)

        item = wx.MenuItem(editMenu, wx.ID_ANY, "Add Page")
        self.Bind(wx.EVT_MENU, self.OnAddPage, item)
        editMenu.AppendItem(item)

        editMenu.AppendSeparator()

        item = wx.MenuItem(editMenu, wx.ID_ANY, "Delete Page")
        self.Bind(wx.EVT_MENU, self.OnDeletePage, item)
        editMenu.AppendItem(item)

        item = wx.MenuItem(editMenu, wx.ID_ANY, "Delete All Pages")
        self.Bind(wx.EVT_MENU, self.OnDeleteAllPages, item)
        editMenu.AppendItem(item)

        item = wx.MenuItem(helpMenu, wx.ID_ANY, "About")
        self.Bind(wx.EVT_MENU, self.OnAbout, item)
        helpMenu.AppendItem(item)

        menuBar.Append(fileMenu, "&File")
        menuBar.Append(editMenu, "&Edit")
        menuBar.Append(helpMenu, "&Help")

        self.SetMenuBar(menuBar)


    def OnQuit(self, event):

        self.Destroy()


    def OnAbout(self, event):

        msg = "This Is The About Dialog Of The LabelBook & FlatImageBook Demo.\n\n" + \
            "Author: Andrea Gavana @ 03 Nov 2006\n\n" + \
            "Please Report Any Bug/Requests Of Improvements\n" + \
            "To Me At The Following Adresses:\n\n" + \
            "andrea.gavana@gmail.com\n" + "gavana@kpo.kz\n\n" + \
            "Welcome To wxPython " + wx.VERSION_STRING + "!!"

        dlg = wx.MessageDialog(self, msg, "LabelBook wxPython Demo",
                               wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


#---------------------------------------------------------------------------


class TestPanel(wx.Panel):
    def __init__(self, parent,colour):
        #self.log = log
        wx.Panel.__init__(self, parent, -1)
        
        st = wx.StaticText(self, -1,
                          "You can put nearly any type of window here,\n"
                          "and if the platform supports it then the\n"
                          "tabs can be on any side of the notebook.",
                          (10, 10))

        b = wx.Button(self, -1, " Test LabelBook And FlatImageBook ", (100,100))
        
        
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)
        self.SetBackgroundColour(colour)

    def OnButton(self, evt):
        msg= "this is a botton!"
        dlg = wx.MessageDialog(self,msg,"this my test",wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
        

#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------


overview = LB.__doc__

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = LabelBookDemo(None,-1)
    frame.Show()
    app.MainLoop()
if not __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

