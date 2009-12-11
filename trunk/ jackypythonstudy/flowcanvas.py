#! /usr/bin/env python
# _*_ coding: utf-8 _*_
# Copyright (C)  2009 Biao Ma

# work_flowcanvas.py

'''
This file is base as OGL 
'''

import wx
import wx.lib.ogl as ogl

class DataShape(ogl.RectangleShape):
    def __init__(self, w=0.0, h=0.0):
        ogl.RectangleShape.__init__(self, w, h)
        self.SetCornerRadius(-0.3)
        
class CompositeDataShape(ogl.CompositeShape):
    def __init__(self,canvas):
        ogl.CompositeShape.__init__(self)
        self.SetCanvas(canvas)

        constraining_shape = ogl.RectangleShape(100, 75)
        constrained_shape1 = ogl.CircleShape(50)
        
        constraining_shape.SetBrush(wx.BLUE_BRUSH)
        constrained_shape1.SetBrush(wx.BLUE_BRUSH)
        
        self.AddChild(constraining_shape)
        self.AddChild(constrained_shape1)
        
        constraint = ogl.Constraint(ogl.CONSTRAINT_MIDALIGNED_RIGHT, constraining_shape, [constrained_shape1])
        self.AddConstraint(constraint)
        self.Recompute()

        # If we don't do this, the shapes will be able to move on their
        # own, instead of moving the composite
        constraining_shape.SetDraggable(False)
        constrained_shape1.SetDraggable(False)
        #constrained_shape2.SetDraggable(True)

        # If we don't do this the shape will take all left-clicks for itself
        constraining_shape.SetSensitivityFilter(0)
        
#----------------------------------------------------------------------

class TaskShape(ogl.DividedShape):
    def __init__(self, width, height, canvas):
        ogl.DividedShape.__init__(self, width, height)

        region1 = ogl.ShapeRegion()
        region1.SetText('DividedShape')
        region1.SetProportions(0.0,0.2)
        region1.SetFormatMode(ogl.FORMAT_CENTRE_HORIZ)
        self.AddRegion(region1)

        region2 = ogl.ShapeRegion()
        region2.SetText('This is Region number two.')
        region2.SetProportions(0.0,0.3)
        region2.SetFormatMode(ogl.FORMAT_CENTRE_HORIZ|ogl.FORMAT_CENTRE_VERT)
        self.AddRegion(region2)

        region3 = ogl.ShapeRegion()
        region3.SetText('Region 3\nwith embedded\nline breaks')
        region3.SetProportions(0.0,0.5)
        region3.SetFormatMode(ogl.FORMAT_NONE)
        self.AddRegion(region3)

        self.SetRegionSizes()
        self.ReformatRegions(canvas)
        

    def ReformatRegions(self, canvas=None):
        rnum = 0

        if canvas is None:
            canvas = self.GetCanvas()

        dc = wx.ClientDC(canvas)  # used for measuring

        for region in self.GetRegions():
            text = region.GetText()
            self.FormatText(dc, text, rnum)
            rnum += 1


    def OnSizingEndDragLeft(self, pt, x, y, keys, attch):
        print "***", self
        ogl.DividedShape.OnSizingEndDragLeft(self, pt, x, y, keys, attch)
        self.SetRegionSizes()
        self.ReformatRegions()
        self.GetCanvas().Refresh()
        
class DiamondShape(ogl.PolygonShape):
    def __init__(self, w=0.0, h=0.0):
        ogl.PolygonShape.__init__(self)
        if w == 0.0:
            w = 60.0
        if h == 0.0:
            h = 60.0

        points = [ (0.0,    -h/2.0),
                   (w/2.0,  0.0),
                   (0.0,    h/2.0),
                   (-w/2.0, 0.0),
                   ]

        self.Create(points)
class Linker(ogl.LineShape):
    def __init__(self,parent,shape):
        ogl.LineShape.__init__(self)
        self.shapes = shape
        print self.shapes
        #self.diagram = ogl.Diagram()
        #parent.SetDiagram(self.diagram)
        
        for x in range(len(self.shapes)):
            print x
            
            
            fromShape = self.shapes[x]
            toShape = self.shapes[0]
              # make all shapes point to TaskShape
            #line = ogl.LineShape()
            self.SetCanvas(parent)
            self.SetPen(wx.BLACK_PEN)
            self.SetBrush(wx.BLACK_BRUSH)
            self.AddArrow(ogl.ARROW_ARROW)
            self.MakeLineControlPoints(1)
            fromShape.AddLine(self, toShape)

            #self.diagram.AddShape(self)
            self.Show(True)

            
class EvtHander(ogl.ShapeEvtHandler):
    def __init__(self, frame):
        ogl.ShapeEvtHandler.__init__(self)
        #self.log = log
        self.statbarFrame = frame

    def up_data_statusbar(self, shape):
        x, y = shape.GetX(), shape.GetY()
        width, height = shape.GetBoundingBoxMax()
        self.statbarFrame.SetStatusText("Pos: (%d, %d)  Size: (%d, %d)" %
                                        (x, y, width, height))


    def OnLeftClick(self, x, y, keys=0, attachment=0):
        shape = self.GetShape()
        canvas = shape.GetCanvas()
        dc = wx.ClientDC(canvas)
        canvas.PrepareDC(dc)

        if shape.Selected():
            shape.Select(False, dc)
            #canvas.Redraw(dc)
            canvas.Refresh(False)
        else:
            redraw = False
            shapeList = canvas.GetDiagram().GetShapeList()
            toUnselect = []

            for s in shapeList:
                if s.Selected():
                    # If we unselect it now then some of the objects in
                    # shapeList will become invalid (the control points are
                    # shapes too!) and bad things will happen...
                    toUnselect.append(s)

            shape.Select(True, dc)

            if toUnselect:
                for s in toUnselect:
                    s.Select(False, dc)

                ##canvas.Redraw(dc)
                canvas.Refresh(False)

        self.up_data_statusbar(shape)
    def OnEndDragLeft(self, x, y, keys=0, attachment=0):
        shape = self.GetShape()
        ogl.ShapeEvtHandler.OnEndDragLeft(self, x, y, keys, attachment)

        if not shape.Selected():
            self.OnLeftClick(x, y, keys, attachment)

        self.up_data_statusbar(shape)
        
        # add the evt process begin here 
        
        message = str(('The shape',str(shape),'has End the  draged /n Please add the evt process in Method OnEndDragLeft'))
        dlg = wx.MessageDialog(None,message,'test',style = wx.OK|wx.ICON_INFORMATION)
        #dlg.ShowModal()
        #dlg.Destroy()
        print message
        
    def OnSizingEndDragLeft(self, pt, x, y, keys, attch):
        ogl.ShapeEvtHandler.OnSizingEndDragLeft(self, pt, x, y, keys, attch)
        self.up_data_statusbar(self.GetShape())


    def OnMovePost(self, dc, x, y, oldX, oldY, display):
        shape = self.GetShape()
        ogl.ShapeEvtHandler.OnMovePost(self, dc, x, y, oldX, oldY, display)
        self.up_data_statusbar(shape)
        if "wxMac" in wx.PlatformInfo:
            shape.GetCanvas().Refresh(False)
    def OnRightClick(self, *dontcare): 
        shape = self.GetShape()
        print shape
    def on_end_dragright(self,x,y,keys = 0, attachment =0):
        pass

class FlowCanvas(ogl.ShapeCanvas):
  # def __init__(self, parent, log, frame):
  
    def __init__(self, parent,frame):
        ogl.ShapeCanvas.__init__(self, parent)
        
        maxWidth  = 800
        maxHeight = 800
        self.SetScrollbars(20, 20, maxWidth/20, maxHeight/20)

        #self.log = log
        self.frame = frame
        self.SetBackgroundColour("LIGHT BLUE") #wx.WHITE)
        self.diagram = ogl.Diagram()
        self.SetDiagram(self.diagram)
        self.diagram.SetCanvas(self)
        self.shapes = []
        self.save_gdi = []

        rRectBrush = wx.Brush("GREEN", wx.SOLID)
        dsBrush = wx.Brush("WHEAT", wx.SOLID)

        # Begin here add the shape to shapecanvas
        
        # add the data shape1 to shapecanvas, the position x=80,y=158
        self.add_shape(
            TaskShape(140, 150, self), 
            380,158, wx.BLACK_PEN, dsBrush, ''
            )
        self.add_shape(
            DataShape(100, 80), 
            80, 158, wx.Pen(wx.BLUE, 2), rRectBrush, "Data Shape1"
            )
        self.add_shape(
            DataShape(100, 80), 
            80, 258, wx.Pen(wx.RED, 2), rRectBrush, "Data Shape2"
            )
        self.add_shape(
            CompositeDataShape(self),
            80,358,wx.Pen(wx.BLUE,2),wx.BLUE,"CompositeDataShape"
            )
        
        self.add_shape(
            DiamondShape(90, 90), 
            355, 360, wx.Pen(wx.BLUE, 3, wx.DOT), wx.RED_BRUSH, "Polygon"
            )
        
        
        # begin here is add the linkline to shapecanvas
        #self.diagram.AddShape(link)
        #link.Show(True)
       
        for x in range(len(self.shapes)):
            fromShape = self.shapes[x]
            toShape = self.shapes[0]

            line = ogl.LineShape()
            line.SetCanvas(self)
            line.SetPen(wx.BLACK_PEN)
            line.SetBrush(wx.BLACK_BRUSH)
            line.AddArrow(ogl.ARROW_ARROW)
            line.MakeLineControlPoints(2)
            fromShape.AddLine(line, toShape)
            self.diagram.AddShape(line)
            line.Show(True)
       
        
    def add_shape(self, shape, x, y, pen, brush, text):
        # Composites have to be moved for all children to get in place
        if isinstance(shape, ogl.CompositeShape):
            dc = wx.ClientDC(self)
            self.PrepareDC(dc)
            shape.Move(dc, x, y)
        else:
            shape.SetDraggable(True, True)
        shape.SetCanvas(self)
        shape.SetX(x)
        shape.SetY(y)
        if pen:    shape.SetPen(pen)
        if brush:  shape.SetBrush(brush)
        if text:
            for line in text.split('\n'):
                shape.AddText(line)
        #shape.SetShadowMode(ogl.SHADOW_RIGHT)
        self.diagram.AddShape(shape)
        shape.Show(True)

        evthandler = EvtHander( self.frame)
        evthandler.SetShape(shape)
        evthandler.SetPreviousHandler(shape.GetEventHandler())
        shape.SetEventHandler(evthandler)

        self.shapes.append(shape)
        return shape
    
class FlowFrame(wx.Frame):
        def __init__(self, *args, **kwds):
                wx.Frame.__init__(self, *args, **kwds)
                self.StatusBar = wx.StatusBar(self)

                self.SetTitle("OGL TEST")
                self.SetSize((600,600))
                self.SetBackgroundColour(wx.Colour(8, 197, 248))
                self.canvas = FlowCanvas(self,self)  
                self.Center()
                
                
#-------------------------------------------------------------------------------
   
def main():
    import nagaratest
    
    app = nagaratest.FrameTest()
    #log = app.log
    ogl.OGLInitialize()
    frame = app.frame
    
    dlg = FlowFrame(None, -1, title='OGl Test', size=(600, 600))
    # paicspanel.MarvinPanel(dlg, -1, 'marvin', log=self.getLog())
    # AmberPanel(dlg, -1, 'amber', log=log)
    
    dlg.Center()
    dlg.Show()
    
    #dlg.Show()
    #dlg.Destroy()

    # app.MainLoop()

    try:
        app.MainLoop()
    except:
        app.RedirectStdio()
        
def run():
    app = wx.PySimpleApp(False)
    wx.InitAllImageHandlers()
    ogl.OGLInitialize()
    frame = FlowFrame(None, -1, "")
    app.SetTopWindow(frame)
    frame.Show(True)
    app.MainLoop()

if __name__ =='__main__':
    #main()
    run()