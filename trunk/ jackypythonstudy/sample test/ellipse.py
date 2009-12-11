import wx
import wx.lib.ogl as ogl

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__( self, None, wx.ID_ANY,
            "objects", size=(400,300))

        canvas = ogl.ShapeCanvas(self)
        canvas.SetBackgroundColour("white")

        diagram = ogl.Diagram()
        canvas.SetDiagram(diagram)
        diagram.SetCanvas(canvas)

        ellipse = ogl.EllipseShape(100, 80) 
        ellipse.SetX(180.0)  
        ellipse.SetY(100.0)  
        ellipse.SetPen(wx.Pen("red", 2))        
        canvas.AddShape(ellipse)

        text = ogl.TextShape(250, 30)  
        text.SetX(180)  
        text.SetY(240)
        text.SetPen(wx.Pen("red", 2))
        text.AddText("draggable text but can I give it a border?")
        canvas.AddShape(text)


        diagram.ShowAll(True)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(canvas, 1, wx.GROW)
        self.SetSizer(sizer)



app = wx.App(0)
ogl.OGLInitialize()
MyFrame().Show()
app.MainLoop()