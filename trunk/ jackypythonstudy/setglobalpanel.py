import wx
import wx.lib.colourselect as csel
import os
import sys
import remotepanel

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

bitmapDir = os.path.join(dirName, 'images')
sys.path.append(os.path.split(dirName)[0])

try:
    from agw import labelbook as LB
    from agw.fmresources import *
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.labelbook as LB
    from wx.lib.agw.fmresources import *
   
#import images
_pageTexts = ["Local", "Remote", "wxPython", "LabelBook", "Demo"]
_pageIcons = ["roll.png", "charge.png"]
#_pageIcons = ["roll.png", "charge.png", "add.png", "decrypted.png", "news.png"]

#_pageIcons = ["icon-equiv.png","icon-minimiz.png","icon-product.png","icon-setup.png","product4x.png"]
_pageColours = [wx.RED, wx.GREEN, wx.WHITE, wx.BLUE, "Pink"]

class SetGlobalPanel(wx.Panel):
    '''
    The panel to setting configution base LabelBook
    '''
    
    def __init__(self, parent,id):
        wx.Panel.__init__(self, parent,-1,size =(800,500))
        #self.mainpanel = wx.Panel(self, -1)
      
        
        self.CreateLabelBook()
        self.DoLayout()

        

        #self.SetIcon(images.Mondrian.GetIcon()) 
        self.Center()

        #self.initializing = False
        self.SendSizeEvent()
       
    
       
    def DoLayout(self):
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        #panelsizer = wx.BoxSizer(wx.VERTICAL)
       
        mainsizer.Add(self.book, 1, wx.EXPAND, 0)
        #self.mainpanel.SetSizer(panelsizer)
        #panelsizer.Layout()
      
        #mainsizer.Add(self, 1, wx.EXPAND, 0)

        self.SetSizer(mainsizer)
        mainsizer.Fit(self)
        mainsizer.Layout()
        self.Layout()

    def CreateLabelBook(self):
        '''
        Create the labebook
        '''
        style = self.GetBookStyles() 
               
        self.book = LB.LabelBook(self, -1,style=style)                     
        # self.book = LB.FlatImageBook(self.mainpanel, -1, style=style)  #change the type of labelbook to Flatimagebook          

        self.imagelist = self.CreateImageList()
        self.book.AssignImageList(self.imagelist)
        self.Refresh()
        '''
        for indx, txts in enumerate(_pageTexts):
            #label = "This is panel number %d"%(indx+1)
            self.book.AddPage(TestPanel(self.book,_pageColours[indx]),
                              txts, True, indx)
        '''
        #for i in range(3):
         #   self.book.AddPage(TestPanel(self.book,_pageColours[i]),_pageTexts[0],True,i)

        self.book.AddPage(TestPanel(self.book,_pageColours[1]),_pageTexts[0],True,0)
        self.book.AddPage(remotepanel.RemotePanel(self.book,-1,(-1,-1)),_pageTexts[1],True,1)
        
        self.book.SetSelection(1)
        #self.book.SetWindowStyleFlag(style=LB.INB_FIT_BUTTON)
        
        self.SendSizeEvent()

    def GetBookStyles(self):
        style = INB_FIT_BUTTON
        style |= INB_FIT_LABELTEXT
        #style |= INB_DEFAULT_STYLE
        #style |= INB_WEB_HILITE
        #style |= INB_USE_PIN_BUTTON
        #style |= INB_BORDER
        #style |= LB.INB_SHOW_ONLY_TEXT   #This stytle is only used in FlatImageBook type
        
        style = self.GetBookOrientation(style)
        
        return style           


    def CreateImageList(self):

        imagelist = wx.ImageList(32, 32)    # (*,*) is the size of icon's heigh and width
        for img in _pageIcons:
            newImg = os.path.join(bitmapDir, "lb%s"%img)
            bmp = wx.Bitmap(newImg, wx.BITMAP_TYPE_PNG)
            imagelist.Add(bmp)
       
        #bmp = imagebmp.GetBitmap()
        #for i in range(5):
        #    imagelist.Add(bmp)

        return imagelist

    def GetBookOrientation(self, style):

        style |= INB_LEFT
        #style |= INB_RIGHT
        #style |= LB.INB_TOP   #only used in FlatImageBook type
        #style |= INB_BOTTOM  #only used in FlatImageBook type

        return style
  
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

        b = wx.Button(self, -1, " Test Messagedialog ", (100,100))
       
       
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)
        self.SetBackgroundColour(colour)

    def OnButton(self, evt):
        msg= "this is a botton!"
        dlg = wx.MessageDialog(self,msg,"this my test",wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
#---------------------------------------------------------------------------

def main():
    import nagaratest
    app = nagaratest.FrameTest()
    log = app.log
    frame = app.frame
    
    dlg = wx.Dialog(None, -1, title='Amber Dialog',size =(600,300))
    # paicspanel.MarvinPanel(dlg, -1, 'marvin', log=self.getLog())
    SetGlobalPanel(dlg,-1)
    dlg.ShowModal()
    #dlg.SetSize(dlg.GetBestSize())
    dlg.Destroy()

    # app.MainLoop()

    try:
        app.MainLoop()
    except:
        app.RedirectStdio()


if __name__ == '__main__':
    main()
    