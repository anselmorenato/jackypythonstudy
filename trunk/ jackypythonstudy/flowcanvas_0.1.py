#! /usr/bin/env python 2.5.4
# _*_ coding: utf-8 _*_
# Copyright (C)  2009 Biao Ma

# work_flow_canvas.py

"""
This file is base as OGL 
"""

import wx
import wx.lib.ogl as ogl
import cPickle

class DataShapeSimple(ogl.RectangleShape):
    """ This is the simple data shape. """
    def __init__(self, w=0.0, h=0.0,text =''):
        ogl.RectangleShape.__init__(self, w, h)
        self.SetCornerRadius(-0.3)
        self.AddText(text)
        
class DataShape(ogl.CompositeShape,ogl.DrawnShape):
    def __init__(self, canvas, name=''):
        ogl.CompositeShape.__init__(self)
        ogl.DrawnShape.__init__(self)

        self.SetCanvas(canvas)        
        
        shape1 = ogl.RectangleShape(100, 60)
        self.AddChild(shape1)
        shape2 = ogl.CircleShape(10)
        shape2.SetBrush(wx.GREEN_BRUSH)
        #shape2.SetY(-35)
        #shape2.Select(select)
        self.AddChild(shape2)
        shape2.SetDraggable(1)
        constraint = ogl.Constraint(ogl.CONSTRAINT_RIGHT_OF ,shape1, [shape2])
        self.AddConstraint(constraint)
        self.Recompute()
        shape1.SetSensitivityFilter(0)
        shape2.SetSensitivityFilter(0)
    def _delete(self):
        self.Delete()
        

#----------------------------------------------------------------------
# Begin here make the shapes for TaskShape

class TaskShape(ogl.CompositeShape):
    """
    This shape is Consists of three parts, InputSocketShape, 
    """
    def __init__(self, canvas,name =''):
        ogl.CompositeShape.__init__(self)
        self.SetCanvas(canvas)
        self.taskobject_name = name
        #shape1 = MiddleShape(canvas)

        middleshape = MiddleShape(100,120,canvas,self.taskobject_name)  # this is the  the constraining shape

        inputshape = InputSocketShape(30,120)
        inputshape.SetBrush(wx.WHITE_BRUSH)

        outputshape = ogl.DrawnShape()
        outputshape.SetDrawnBrush(wx.GREEN_BRUSH)
        outputshape.DrawPolygon([(0,60),(0,0),(0,-60),(30,0)])

        self.AddChild(inputshape)
        self.AddChild(middleshape)
        self.AddChild(outputshape)

        # If we don't do this, the shapes will be able to move on their
        # own, instead of moving the composite
        middleshape.SetDraggable(True)
        inputshape.SetDraggable(0)
        outputshape.SetDraggable(0)

        # ------------------------------------------------------------
        constraint = ogl.Constraint(ogl.CONSTRAINT_LEFT_OF,middleshape, [inputshape])
        constraint.SetSpacing(0.2,0)
        constraint2 = ogl.Constraint(ogl.CONSTRAINT_MIDALIGNED_RIGHT,middleshape,[outputshape])
        constraint2.SetSpacing(1,0)
        
        self.AddConstraint(constraint)
        self.AddConstraint(constraint2)
        self.Recompute()
        # If we don't do this the shape will take all left-clicks for itself
        middleshape.SetSensitivityFilter(0)
        inputshape.SetSensitivityFilter(0)
        outputshape.SetSensitivityFilter(0)

    def _delete(self):
        self.Delete()
        
class InputSocketShape(ogl.RectangleShape):
    """this shape is one part of the TaskShape"""
    def __init__(self,w = 0.0,h = 0.0):
        ogl.RectangleShape.__init__(self, w, h) 

class MiddleShape(ogl.DividedShape):
    """this shape is one part of the TaskShape"""
    def __init__(self, width, height, canvas,name =''):
        ogl.DividedShape.__init__(self, width, height)
        self.taskobject_name = name
        
        region1 = ogl.ShapeRegion()
        region1.SetText(self.taskobject_name)
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
        region3.SetFormatMode(ogl.FORMAT_CENTRE_HORIZ|ogl.FORMAT_CENTRE_VERT)
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

class OutputSocketShape(ogl.PolygonShape):
    """this shape is one part of the TaskShape"""
    def __init__(self, w=0.0, h=0.0):
        ogl.PolygonShape.__init__(self)
        if w == 0.0:
            w = 90.0
        if h == 0.0:
            h = 90.0

        points = [ (0.0,    h/2.0),
                   (0.0,    -h/2.0),
                   (w/2.0,  0.0),
                   ]

        self.Create(points)
        
# TaskShape is end.
class Linker(ogl.LineShape):
    def __init__(self,parent,shape,frame):
        ogl.LineShape.__init__(self)
        #ogl.ShapeCanvas.__init__(self,parent)
        self.shapes = shape
        print self.shapes
        #self.diagram = ogl.Diagram()
        #parent.SetDiagram(self.diagram)
        for x in range(len(self.shapes)):
            print x
            fromShape = self.shapes[x]
            if x+1 == len(self.shapes):
                toShape = self.shapes[0]
            else:
                toShape = self.shapes[x+1]
        # toShape = self.shapes[1]  # make all shapes point to TaskShape

            #line = ogl.LineShape()
            #self.SetCanvas(parent)
            self.SetPen(wx.BLACK_PEN)
            self.SetBrush(wx.BLACK_BRUSH)
            self.AddArrow(ogl.ARROW_ARROW)
            self.MakeLineControlPoints(2)
            fromShape.AddLine(self, toShape)
            #self.diagram.AddShape(self)
            #self.Show(True)


class EvtHander(ogl.ShapeEvtHandler):
    
    def __init__(self, frame, canvas):
        ogl.ShapeEvtHandler.__init__(self)
        #self.log = log
        self.frame = frame
        self.canvas = canvas
        self.shape = self.GetShape()

    def up_data_statusbar(self, shape):
        x, y = shape.GetX(), shape.GetY()
        width, height = shape.GetBoundingBoxMax()
        self.frame.SetStatusText("Pos: (%d, %d)  Size: (%d, %d)" %
                                        (x, y, width, height))

    def OnLeftClick(self, x, y, keys=0, attachment=0):
        shape = self.GetShape()
        canvas = shape.GetCanvas()
        dc = wx.ClientDC(canvas)
        canvas.PrepareDC(dc)
        sx,sy = self.canvas.CalcUnscrolledPosition(x, y) 
        if isinstance(self.canvas.FindShape(x,y),wx.lib.ogl._basic.CircleShape):
            print 'iam circle'
        print self.canvas.FindShape(sx,sy)[0],sx,sy
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
                canvas.Refresh(True) #Flase 
        
        self.up_data_statusbar(shape)
    def OnBeginDragLeft(self,x,y,key=0,attachment=0):
        print 'drag begin at',x,y
        ogl.ShapeEvtHandler.OnBeginDragLeft(self, x, y, keys = 0, attachment = 0)
        if isinstance(self.canvas.FindShape(x,y),(wx.lib.ogl._basic.CircleShape)):
            #x=old_x 
            #y=old_y            
            print 'hello'
            ogl.ShapeEvtHandler.OnBeginDragLeft(self, x, y, keys = 0, attachment = 0)          
    
        
    def OnEndDragLeft(self, x, y, keys=0, attachment=0):
        shape = self.GetShape()
        sx,sy = self.canvas.CalcUnscrolledPosition(x, y)
        _shape = self.canvas.FindShape(x,y)
        print 'shape is ',_shape,'the type is',type(_shape)
        ogl.ShapeEvtHandler.OnEndDragLeft(self, x, y, keys, attachment)
        if isinstance(self.canvas.FindShape(sx,sy)[0],InputSocketShape):
            print 'now task is start'
        
        self.up_data_statusbar(shape)

        # add the evt process begin here 

        message = str(('The shape',str(shape),'has End the  draged /n Please add the evt process in Method OnEndDragLeft'))
        dlg = wx.MessageDialog(None,message,'test',style = wx.OK|wx.ICON_INFORMATION)
    # dlg.ShowModal()
        #dlg.Destroy()
        

    def OnSizingEndDragLeft(self, pt, x, y, keys, attch):
        ogl.ShapeEvtHandler.OnSizingEndDragLeft(self, pt, x, y, keys, attch)
        self.up_data_statusbar(self.GetShape())


    def OnMovePost(self, dc, x, y, oldX, oldY, display):
        shape = self.GetShape()
        ogl.ShapeEvtHandler.OnMovePost(self, dc, x, y, oldX, oldY, display)
        self.up_data_statusbar(shape)
        if "wxMac" in wx.PlatformInfo:
            shape.GetCanvas().Refresh(False)
    def OnRightClick(self,x,y,keys = 0, attachment =0): 
        pass
        #popmenu = self.frame.make_popmenu()
        #self.canvas.Bind(wx.EVT_MENU,self.on_menu_delete)
        
        #if shape.Haschild
        #if shape == TaskShape(shape.GetCanvas()):
        #print 'this is right ckick',shape
    def on_end_dragright(self,x,y,keys = 0, attachment =0):
        pass
    def OnLeftDoubleClick(self,x,y,keys = 0, attachment =0):
        
        shape = self.GetShape()
        #canvas = shape.Getcanvas()
        self.canvas.diagram.RemoveShape(shape)
        self.canvas.Refresh()
        
        print shape ,'is deleted'
    def on_menu_delete(self,event):
        shape = self.GetShape()
        
        shape.DeleteControlPoints()
        shape.Delete()
        self.canvas.Refresh()
        print shape ,'is deleted'
class FlowCanvas(ogl.ShapeCanvas):
    #def __init__(self, parent, log, frame):

    def __init__(self, parent,frame):
        ogl.ShapeCanvas.__init__(self, parent)

        maxWidth  = 500
        maxHeight = 500
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
        
        self.Bind(wx.EVT_RIGHT_DOWN,self.on_right)
        self.Bind(wx.EVT_MOTION,self.on_motion)
        #self.Bind(wx.EVT_CHILD_FOCUS,self.on_motion)
        #self.Bind(wx.EVT_LEFT_DOWN,self.on_left)
        #self.Bind(wx.EVT_ENTER_WINDOW,self.on_motion)

        # Begin here add the shape to shapecanvas
        # add the data shape1 to shapecanvas, the position x=80,y=158
       
        # begin here is add the linkline to shapecanvas

        for x in range(len(self.shapes)):
            fromShape = self.shapes[x]
            toShape = self.shapes[1]

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
        
        #shape.AddText(shape.taskobject_name)
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

        self.evthandler = EvtHander( frame=self.frame,canvas=self)
        self.evthandler.SetShape(shape)
        self.evthandler.SetPreviousHandler(shape.GetEventHandler())
        shape.SetEventHandler(self.evthandler)

        self.shapes.append(shape)
        return shape
    def delete_shape(self):
        pass
        shape = self.shapes[0]
        print shape
        self.diagram.RemoveShape(shape)
        
        self.Refresh()
    
    @property
    def selected_shape(self):
        return self.__selected_shape
    
    def on_select(self, event):
        x,y = event.GetPosition()
        sx, sy = self.CalcUnscrolledPosition(x, y)
        shape, attachment = self.FindShape(sx, sy)
        print x,y
        self.__selected_shape = shape
    
    def on_right(self,event):
        x,y = event.GetPosition()
        sx, sy = self.CalcUnscrolledPosition(x, y)
        shape, attachment = self.FindShape(sx, sy)
        print x,y
        #print shape
        
        def on_delete(event):
            #x,y = event.GetEventObject().GetPosition()
            #sx, sy = self.CalcUnscrolledPosition(x, y)
            #self.shape, attachment = self.FindShape(sx, sy)
            #print x,y
            #print shape        
            #if not self.shape == None :
            shape.GetParent().DeleteControlPoints()
            shape.GetParent().Delete()
            self.Refresh()
            

        if shape:
            popmenu = self.frame.make_popmenu()
            #self.frame.Bind(wx.EVT_MENU,on_delete,id=popmenu)
  
    def on_motion(self,event):
        x,y = event.GetPosition()
        sx, sy = self.CalcUnscrolledPosition(x, y)
        shape, attachment = self.FindShape(sx, sy)
        print sx,sy
        if isinstance(shape, InputSocketShape):
        #if not shape ==None:
            print "the mouse in input"
            
    def on_left(self,event):
        x,y = event.GetPosition()
        sx, sy = self.CalcUnscrolledPosition(x, y)
        shape, attachment = self.FindShape(sx, sy)
        if isinstance(shape,wx.lib.ogl._basic.CircleShape):
            shape.GetParent().SetDraggable(False)
            #shape.SetDraggable(True)
            print 'i am circle' 
        else: 
            self.Unbind(wx.EVT_LEFT_DOWN)
            shape.GetParent().SetDraggable(True)
class TempCanvas(ogl.ShapeCanvas):
    def __init__(self, parent,frame):
        ogl.ShapeCanvas.__init__(self, parent)

        maxWidth  = 500
        maxHeight = 500
        self.SetScrollbars(20, 20, maxWidth/20, maxHeight/20)

        #self.log = log
        self.frame = frame
        self.SetBackgroundColour("LIGHT GREY") #wx.WHITE)
        self.diagram = ogl.Diagram()
        self.SetDiagram(self.diagram)
        self.diagram.SetCanvas(self)
        self.shapes = []
        self.save_gdi = []
        
    def add_shape(self, shape, x, y, pen, brush, text):
        # Composites have to be moved for all children to get in place
        if isinstance(shape, ogl.CompositeShape):
            dc = wx.ClientDC(self)
            self.PrepareDC(dc)
            shape.Move(dc, x, y)
        else:
            shape.SetDraggable(False, False)
            
        shape.AddText(shape.taskobject_name)
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

class TaskShapeDropTarget(wx.PyDropTarget):
    
    def __init__(self, canvas):
        wx.PyDropTarget.__init__(self)
        #self.log = log
        self.canvas = canvas

        # specify the type of data we will accept
        self.data = wx.TextDataObject()
        self.SetDataObject(self.data)
    
    def OnDrop(self, x, y):
        
        self.canvas.Refresh()
    def OnData(self, x, y, d):
        

        # copy the data from the drag source to our data object
        if self.GetData():
            # convert it back to a list of lines and give it to the viewer
            self.text = self.data.GetText()
            
        self.canvas.add_shape(TaskShape(self.canvas,self.text),x,y, wx.BLACK_PEN, wx.WHITE_BRUSH, '')
            
        # what is returned signals the source what to do
        # with the original data (move, copy, etc.)  In this
        # case we just return the suggested value given to us.
        return d  
class FlowFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        wx.Frame.__init__(self, *args, **kwds)
        #panel = wx.Panel(self)
        
        self.menu = self.make_menu()
        
        self.make_toolbar()
        
        splitter1 = wx.SplitterWindow(self, -1, style=wx.SP_3D)
        splitter2 = wx.SplitterWindow(splitter1, -1, style=wx.SP_3D)
        #log = open('log.log')

        self.SetTitle("OGL TEST")
        self.SetSize((800,600))
        self.SetBackgroundColour(wx.Colour(8, 197, 248))
        
        self.work_canvas = FlowCanvas(splitter1,frame=self)

        #self.temp_canvas = TempCanvas(splitter2,self)
        self.temp_canvas = wx.ListCtrl(splitter2, -1, style=wx.LC_LIST)
        tasklist = ["Task1","Task2","Task3","Task4"]
        for i in range(len(tasklist)):        
            #self.temp_canvas.InsertStringItem(0,i)
            self.temp_canvas.InsertStringItem(i,tasklist[i])
            
        self.temp_canvas.Bind(wx.EVT_LIST_BEGIN_DRAG, self.on_drag_start)
        
        splitter1.SplitVertically(self.work_canvas, splitter2,500)
        splitter2.Initialize(self.temp_canvas)
        self.Center()
        self.shapetaget = TaskShapeDropTarget(self.work_canvas)
        self.work_canvas.SetDropTarget(self.shapetaget)  
        
    def make_menu(self):
        #menudata =dict(['taskID1','Task1'],
        #               ['taskID2','Task2'])
        
        newtaskID = wx.NewId()
        newdataID = wx.NewId()
        deleteID = wx.NewId()
        taskID1 = wx.NewId()
        taskID2= wx.NewId()
        taskID3 = wx.NewId()
        taskID4 = wx.NewId()
        
        menu = wx.Menu()
        #item = menu.Append(newtaskID,'New Task')
        item_newdata = menu.Append(newdataID, 'New Data')
        
        menu2 =wx.Menu()
        item_delete =menu2.Append(deleteID,'Delete')
        
        submenu = wx.Menu()
        task1 = submenu.Append(taskID1,'Task1')
        task2 = submenu.Append(taskID2,'Task2')
        task3 = submenu.Append(taskID3,'Task3')
        task4 = submenu.Append(taskID4,'Task4')
        
        menu.AppendMenu(newtaskID,'New Task',submenu)
        menubar = wx.MenuBar()
        menubar.Append(menu,'New')
        menubar.Append(menu2,'Edit')
        self.SetMenuBar(menubar)
        self.StatusBar = wx.StatusBar(self)
        #for i in ('task1','task2','task3','task4'):
        self.Bind(wx.EVT_MENU,self.on_add_task,task1)
        self.Bind(wx.EVT_MENU,self.on_add_data,item_newdata)
        self.Bind(wx.EVT_MENU,self.on_remove_shape,item_delete)
    
        
    def make_toolbar(self):
        toolbar = self.CreateToolBar()
        
        tsize = (24,24)
        new_bmp =  wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, tsize)
        open_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, tsize)
        copy_bmp = wx.ArtProvider.GetBitmap(wx.ART_COPY, wx.ART_TOOLBAR, tsize)
        paste_bmp= wx.ArtProvider.GetBitmap(wx.ART_PASTE, wx.ART_TOOLBAR, tsize)

        toolbar.SetToolBitmapSize(tsize)
        
        #tb.AddSimpleTool(10, new_bmp, "New", "Long help for 'New'")
        toolbar.AddLabelTool(10, "New Date", new_bmp, shortHelp="Add new date", longHelp="Long help for 'New'")
        self.Bind(wx.EVT_TOOL, self.on_tool_click, id=10)
        #self.Bind(wx.EVT_TOOL_RCLICKED, self.OnToolRClick, id=10)

        #tb.AddSimpleTool(20, open_bmp, "Open", "Long help for 'Open'")
        toolbar.AddLabelTool(20, "Open", open_bmp, shortHelp="Open", longHelp="Long help for 'Open'")
        self.Bind(wx.EVT_TOOL, self.on_tool_click, id=20)
        #self.Bind(wx.EVT_TOOL_RCLICKED, self.OnToolRClick, id=20)

        
        # Final thing to do for a toolbar is call the Realize() method. This
        # causes it to render (more or less, that is).
        toolbar.Realize()
        
    def on_tool_click(self,event):
        id = event.GetId()
        if id == 10:
            self.on_add_data(event)
            self.work_canvas.Refresh()
        
    def on_drag_start(self,event):
        
        self.data = wx.TextDataObject(self.temp_canvas.GetItemText(event.GetIndex()))
        dropsource = wx.DropSource(self.temp_canvas)
        dropsource.SetData(self.data)
        dropsource.DoDragDrop(wx.Drag_CopyOnly)

        #self.canvas.Bind(wx.EVT_LEFT_UP, self.on_add_task,id = self.canvas.GetId())
        #self.canvas.Bind(wx.EVT_LEFT_UP, self.on_drag_init, id=self.canvas.GetId())

    def on_drag_init(self,event):
        
        # create our own data format and use it in a custom data object
        self.data = wx.CustomDataObject("TaskShape")
        # pickle the shape list
        shape_data = cPickle.dumps(TaskShape)
        #temp_shapedate = cPickle.dumps(self.canvas_temp,1)

        self.data.SetData(TaskShape)
        #data.SetData(temp_shapedate)

        #data.SetData(self.canvas)
        #data.SetData(self.canvas_temp)
        # create the droptaaget
        self.shapetaget = TaskShapeDropTarget(self.canvas_temp)
        self.canvas_temp.SetDropTarget(shapetaget)        
        
        _obj = event.GetEventObject()  #this is added new 
        text = _obj.GetShape(event.GetIndex())  # use 'obj' instead the 'self.lc1'
        tdo = wx.CustomDataObject(text)
        tds = wx.DropSource(_obj)
        tds.SetData(tdo)
        tds.DoDragDrop(True)
        
    def on_add_data(self,event):
        self.work_canvas.add_shape(DataShape(self.work_canvas,'name'), 
                200,200, wx.BLACK_PEN, wx.GREEN_BRUSH, ''
            )
        self.work_canvas.Refresh()
    def on_add_task(self,event):
        #print event.GetEventObject,type(event.GetEventObject)
        #name = self.make_menu().GetLableText(event.GetId())
        
        self.work_canvas.add_shape(TaskShape(self.work_canvas,'name'), 
                200,100, wx.BLACK_PEN, wx.WHITE_BRUSH, ''
            )
        self.work_canvas.Refresh()
    def on_remove_shape(self,event):
        x,y = event.GetPosition()
        sx, sy = self.CalcUnscrolledPosition(x, y)
        shape, attachment = self.FindShape(sx, sy)
        if shape.Selected():
            shape.Delete()
            self.work_canvas.Refresh()
        #shape = self.work_canvas.GetShape()
        #self.work_canvas.delete_shape()
        #self.work_canvas.Refresh()
#-------------------------------------------------------------------------------

def main():
    import nagaratest

    app = nagaratest.FrameTest()
    log = app.log
    ogl.OGLInitialize()
    frame = app.frame

    dlg = FlowFrame(None, -1, title='OGl Test', size=(600, 600))
   
    dlg.Center()


    dlg.Show()
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