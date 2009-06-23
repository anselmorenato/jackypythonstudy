import wx
import wx.lib.colourselect as csel
#import random

import os
import sys
from wx.lib.embeddedimage import PyEmbeddedImage

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
_pageIcons = []
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
       
        self.mainpanel = wx.Panel(self, -1)
       
        self.SetProperties()
        self.CreateLabelBook()
        self.DoLayout()

        statusbar = self.CreateStatusBar(2, wx.ST_SIZEGRIP)
        statusbar.SetStatusWidths([-2, -1])
        # statusbar fields
        statusbar_fields = [("LabelBook & FlatImageBook wxPython Demo, Andrea Gavana @ 03 Nov 2006"),
                            ("Welcome To wxPython!")]

        for i in range(len(statusbar_fields)):
            statusbar.SetStatusText(statusbar_fields[i], i)

        

        self.SetSize((800,700))

        #self.SetIcon(images.Mondrian.GetIcon())  
        self.CenterOnScreen()

        self.initializing = False
        self.SendSizeEvent()


    def SetProperties(self):

        self.SetTitle("This is my code souce!-)")
        #sself.pin.SetValue(1)
        #self.mainpanel.SetMinimumPaneSize(120)


    def DoLayout(self):

        mainsizer = wx.BoxSizer(wx.VERTICAL)
        panelsizer = wx.BoxSizer(wx.VERTICAL)
        

        panelsizer.Add(self.book, 1, wx.EXPAND, 0)
        self.mainpanel.SetSizer(panelsizer)
        panelsizer.Layout()

        
        mainsizer.Add(self.mainpanel, 1, wx.EXPAND, 0)

        self.SetSizer(mainsizer)
        mainsizer.Layout()
        self.Layout()


    def CreateLabelBook(self, btype=0):


        style = self.GetBookStyles()

        if btype == 0: # it is a labelbook:
            self.book = LB.LabelBook(self.mainpanel, -1, style=style)
            #if self.bookdirection.GetSelection() > 1:
            #    self.bookdirection.SetSelection(0)

            #self.SetUserColours()                

        else:
            self.book = LB.FlatImageBook(self.mainpanel, -1, style=style)

        #self.EnableChoices(btype)            

        self.imagelist = self.CreateImageList()
        self.book.AssignImageList(self.imagelist)

        for indx, txts in enumerate(_pageTexts):
            #label = "This is panel number %d"%(indx+1)
            self.book.AddPage(TestPanel(self.book,_pageColours[indx]),
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

        #style = INB_FIT_BUTTON
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
            bmp = wx.Bitmap(newImg, wx.BITMAP_TYPE_GIF)
            imagelist.Add(bmp)
        
        #bmp = imagebmp.GetBitmap()

        #for i in range(5):
         #   imagelist.Add(bmp)

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
        



overview = LB.__doc__

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = LabelBookDemo(None,-1)
    frame.Show()
    app.MainLoop()
