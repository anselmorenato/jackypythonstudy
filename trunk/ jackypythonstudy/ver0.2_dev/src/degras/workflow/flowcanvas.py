# _*_ coding: utf-8 _*_
# Copyright (C)  2009 Biao Ma

# flowcanvas.py

"""
This file is base as OGL 
"""

import wx
import wx.lib.ogl as ogl
#import cPickle

class DataShapeSimple(ogl.RectangleShape):
    """ This is the simple data shape. """
    def __init__(self, w=0.0, h=0.0,text =''):
        ogl.RectangleShape.__init__(self, w, h)
        self.SetCornerRadius(-0.3)
        self.AddText(text)
        
class DataShape(ogl.CompositeShape):
    """ this is the composite data shape.
    """
    def __init__(self, canvas, name=''):
        ogl.CompositeShape.__init__(self)

        self.SetCanvas(canvas)        
        
        shape1 = ogl.RectangleShape(100, 60)
        self.AddChild(shape1)
        #shape2 = ogl.CircleShape(10)
        shape2 = Connector(canvas, self)
        shape2.SetBrush(wx.GREEN_BRUSH)
        shape2.SetY(-35)
        #shape2.Select(select)
        self.AddChild(shape2)
        #shape2.SetDraggable(1)
        constraint = ogl.Constraint(ogl.CONSTRAINT_RIGHT_OF ,shape1, [shape2])
        self.AddConstraint(constraint)
        self.Recompute()
        shape1.SetSensitivityFilter(0)
        shape2.SetSensitivityFilter(5)
    def _delete(self):
        self.Delete()
        

class Connector(ogl.CircleShape):
    
    def __init__(self, canvas, data_shape, size = 10):
        ogl.CircleShape.__init__(self, size)
        self.SetCanvas(canvas)
        #self.SetDraggable(False)
        self.data_shape = data_shape
        self.canvas = canvas
        
    def OnBeginDragLeft(self, x, y,keys =0,attachment =0 ):
        ogl.ShapeEvtHandler.OnBeginDragLeft(self, x, y, keys, attachment)
        self.canvas._isDragging(True)
        
    def OnEndDragLeft(self, x, y, keys=0, attachment=0):
        self.canvas._isDragging(False)
        sx,sy = self.GetCanvas().CalcUnscrolledPosition(x, y)
        _shape,attachment = self.GetCanvas().FindShape(x,y)
        print 'shape is ',_shape,'the type is',type(_shape)
        ogl.ShapeEvtHandler.OnEndDragLeft(self, x, y, keys, attachment)

        if isinstance(_shape,InputSocketShape):
            
            print 'now task is start'
            print self.data_shape
            fromShape = self.data_shape
            
            toShape = _shape
            self.GetCanvas().add_linker(fromShape,toShape)

        
        

#----------------------------------------------------------------------
# Begin here make the shapes for TaskShape

class TaskShape(ogl.CompositeShape):
    """
    This shape is Consists of three parts, InputSocketShape, Middleshape and OutputsocketShape.
    """
    def __init__(self, canvas,name =''):
        ogl.CompositeShape.__init__(self)
        self.SetCanvas(canvas)
        self.taskobject_name = name

        middleshape = MiddleShape(100,120,canvas,self.taskobject_name)  # this is the  the constraining shape

        inputshape1 = InputSocketShape(10,30)
        inputshape2 = InputSocketShape(10,30)
        inputshape3 = InputSocketShape(10,30)
        # set the inputsocket background color
        inputshape1.SetBrush(wx.GREEN_BRUSH)
        inputshape2.SetBrush(wx.GREEN_BRUSH)
        inputshape3.SetBrush(wx.GREEN_BRUSH)
        
        outputshape = OutputSocketShape()
        # set the outputsocket background color
        outputshape.SetDrawnBrush(wx.GREY_BRUSH)
        outputshape.DrawPolygon([(0,60),(0,-60),(30,0)])

        self.AddChild(inputshape1)
        self.AddChild(inputshape2)
        self.AddChild(inputshape3)
        self.AddChild(middleshape)
        self.AddChild(outputshape)

        # If we don't do this, the shapes will be able to move on their
        # own, instead of moving the composite
        middleshape.SetDraggable(True)
        inputshape1.SetDraggable(True)
        outputshape.SetDraggable(True)

        # control the layout of inputsocket and outputsocket with middleshape
        constraint = ogl.Constraint(ogl.CONSTRAINT_LEFT_OF,middleshape, [inputshape1,inputshape2,inputshape3])
        constraint.SetSpacing(0.2,0)
        inputshape1.SetY(40)
        inputshape2.SetY(-40)
        
        constraint2 = ogl.Constraint(ogl.CONSTRAINT_MIDALIGNED_RIGHT,middleshape,[outputshape])
        constraint2.SetSpacing(1,0)
        
        self.AddConstraint(constraint)
        self.AddConstraint(constraint2)
        self.Recompute()
        # If we don't do this the shape will take all left-clicks for itself
        middleshape.SetSensitivityFilter(0)
        inputshape1.SetSensitivityFilter(0)
        inputshape2.SetSensitivityFilter(0)
        inputshape3.SetSensitivityFilter(0)
        outputshape.SetSensitivityFilter(0)

    def _delete(self):
        self.Delete()
        
class InputSocketShape(ogl.RectangleShape):
    """this shape is one part of the TaskShape"""
    def __init__(self,w=0.0,h=0.0):
        """
        ogl.CompositeShape.__init__(self) 
        self.SetCanvas(canvas)
        self.taskobject_name = name
        
        main_shape = ogl.RectangleShape(30,100)
        self.AddChild(main_shape)
        shape1 = ogl.RectangleShape(8,30)
        shape1.SetY(-40)
        self.AddChild(shape1)
        shape2 = ogl.RectangleShape(8,30)
        self.AddChild(shape2)
        shape3 = ogl.RectangleShape(8,30)
        shape3.SetY(40)
        self.AddChild(shape3)
        constraint = ogl.Constraint(ogl.CONSTRAINT_LEFT_OF, main_shape, [shape1,shape2,shape3])
        self.AddConstraint(constraint)
        self.Recompute()
        shape1.SetSensitivityFilter(0)
        shape2.SetSensitivityFilter(0)
        shape3.SetSensitivityFilter(0)
        main_shape.SetSensitivityFilter(0)
        """
        ogl.RectangleShape.__init__(self,w,h)
        self.__is_zoomed = False
        self.__width, self.__height = self.GetBoundingBoxMax()
        
    def zoom(self):
        import time
        h = 2
        w = 1
        width  = self.__width
        height = self.__height
        
        while 40 > width and 100 > height :
            self.SetSize(width, height)
            self.GetCanvas().Refresh()
            width  += w
            height += h
            # time.sleep(0.02)
        self.__is_zoomed = True
        #self.SetX(self.GetX()-10)
        print width,height
    def set_default_size(self):
        self.SetSize(self.__width, self.__height)
        #self.SetX(self.GetX()+10)
        
    def is_zoomed(self):
        return self.__is_zoomed
    
    def enable_zoom(self, enable):
        self.__is_zoomed = enable
            
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

class OutputSocketShape(ogl.DrawnShape):
    """this shape is one part of the TaskShape"""
    def __init__(self):
        ogl.DrawnShape.__init__(self)
        
class PopupShape(ogl.RectangleShape):
    """this shape is one part of the TaskShape"""
    def __init__(self,w = 0.0,h = 0.0):
        ogl.RectangleShape.__init__(self, 150, 100)
        

class TaskPopupWindow(wx.PopupTransientWindow):
    """Adds a bit of text and mouse movement to the wx.PopupWindow"""
    def __init__(self, parent, style):
        wx.PopupTransientWindow.__init__(self, parent, style)
        #self.log = log
        self.SetBackgroundColour("#FFB6C1")
        st = wx.StaticText(self, -1,
                          "wx.PopupTransientWindow is a\n"
                          "wx.PopupWindow which disappears\n"
                          "automatically when the user\n"
                          "clicks the mouse outside it or if it\n"
                          "(or its first child) loses focus in \n"
                          "any other way."
                          ,
                          pos=(10,10))
        sz = st.GetBestSize()
        self.SetSize( (sz.width+20, sz.height+20) )
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER,self.on_time,self.timer)
        self.timer.Start(1000)
    def on_time(self,event):
        self.Destroy()
        
# TaskShape is end here
#----------------------------------------------------------------------
class Linker(ogl.LineShape):
    """ the link line from datashape to taskshape.
    """
    def __init__(self,fromShape,toShape,*args,**cwdargs):
        ogl.LineShape.__init__(self)
       
        fromShape = fromShape
        toShape = toShape

        self.SetPen(wx.BLACK_PEN)
        self.SetBrush(wx.BLACK_BRUSH)
        self.AddArrow(ogl.ARROW_ARROW)
        self.MakeLineControlPoints(2)
        fromShape.AddLine(self, toShape)
        #self.Show(True)
    def _delete(self):
        self.Delete()
        
    def on_fromshape_deleted(self,fromshape):
        _fromshape = fromshape
        #_fromshape.

class EvtHandler(ogl.ShapeEvtHandler):
    """ 
    """
    def __init__(self, canvas):
        ogl.ShapeEvtHandler.__init__(self)
        #self.log = log
        # self.frame = frame
        self.canvas = canvas
        self.shape = self.GetShape()

    def up_data_statusbar(self, shape):
        x, y = shape.GetX(), shape.GetY()
        width, height = shape.GetBoundingBoxMax()
        # self.frame.SetStatusText("Pos: (%d, %d)  Size: (%d, %d)" %
                                        # (x, y, width, height))

    def OnLeftClick(self, x, y, keys=0, attachment=0):
        shape = self.GetShape()
        canvas = shape.GetCanvas()
        dc = wx.ClientDC(canvas)
        canvas.PrepareDC(dc)
        sx,sy = self.canvas.CalcUnscrolledPosition(x, y)
        _shape,attachment =self.canvas.FindShape(sx,sy)
        print shape
        print _shape,'is left click'
        
        if shape.Selected():
            shape.Select(False, dc)
            canvas.Redraw(dc)
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
        #self.canvas.Unbind(wx.EVT_MOTION)
        ogl.ShapeEvtHandler.OnBeginDragLeft(self, x, y, keys = 0, attachment = 0)
        self.canvas._isDragging(True)
        shape = self.GetShape()
        sx,sy = self.canvas.CalcUnscrolledPosition(x, y)
        _shape,attachment = self.canvas.FindShape(x,y)        
        print 'drag begin at',x,y
        
        if isinstance(_shape,wx.lib.ogl._basic.CircleShape):
            #x=old_x 
            #y=old_y
            print _shape
            #shape.SetDraggable(False)
                      
    
        
    def OnEndDragLeft(self, x, y, keys=0, attachment=0):
        self.canvas._isDragging(False)
        print self.canvas.isDragging
        shape = self.GetShape()  # This is the souce shape of dragged.  
        sx,sy = self.canvas.CalcUnscrolledPosition(x, y)
        _shape,attachment = self.canvas.FindShape(x,y)  # _shape is the shape at drop position. 
        print 'shape is ',_shape,'the type is',type(_shape)
        ogl.ShapeEvtHandler.OnEndDragLeft(self, x, y, keys, attachment)
        try:
            _shape_p = _shape.GetParent()
        except:
            _shape_p =_shape
        if isinstance(_shape,InputSocketShape)& isinstance(shape,DataShape):
            print 'now task is start'
            print shape
            fromShape = shape
            toShape = _shape
            self.canvas.add_linker(fromShape,toShape)
            self.canvas._isDragging(False)
            shape.SetDraggable(True)
        self.up_data_statusbar(shape)
        
        #self.canvas.Bind(wx.EVT_MOTION,self.canvas.on_motion)
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
            
    def OnLeftDoubleClick(self,x,y,keys = 0, attachment =0):
        pass
        #shape = self.GetShape()
        #canvas = shape.Getcanvas()
        #self.canvas.diagram.RemoveShape(shape)
        #self.canvas.Refresh()
        
        #print shape ,'is deleted'
    def on_menu_delete(self,event):
        pass
       # shape = self.GetShape()
        
       # shape.DeleteControlPoints()
       # shape.Delete()
       # self.canvas.Refresh()
       # print shape ,'is deleted'
class FlowCanvas(ogl.ShapeCanvas):
    #def __init__(self, parent, log, frame):

    def __init__(self, parent):
        ogl.ShapeCanvas.__init__(self, parent)
        ogl.OGLInitialize()
        maxWidth  = 1500
        maxHeight = 1500
        self.SetScrollbars(20, 20, maxWidth/20, maxHeight/20)

        # self.log = log
        # self.frame = frame
        self.SetBackgroundColour("LIGHT BLUE") #wx.WHITE)
        self.diagram = ogl.Diagram()
        self.SetDiagram(self.diagram)
        self.diagram.SetCanvas(self)
        self.shapes = []
        self.save_gdi = []
        self.lines = []
        self.isDragging = False

        rRectBrush = wx.Brush("GREEN", wx.SOLID)
        dsBrush = wx.Brush("white", wx.SOLID)
        
        self.Bind(wx.EVT_RIGHT_DOWN,self.on_right)
        self.Bind(wx.EVT_MOTION,self.on_motion)
        self.Bind(wx.EVT_KEY_DOWN,self.key_press)
        #self.Bind(wx.EVT_CHILD_FOCUS,self.on_motion)
        #self.Bind(wx.EVT_LEFT_DOWN,self.on_left)
        #self.Bind(wx.EVT_ENTER_WINDOW,self.on_motion)
    def _isDragging(self,dragging):
        self.isDragging = dragging
    
    def make_popmenu(self):
        """ creat the popup menu when right click on shape.
        """
        ID_delete = wx.NewId()
        ID_property = wx.NewId()
        
        # create popmenu
        popmenu = wx.Menu()
        # delete
        item_delete =popmenu.Append(ID_delete,'Delete')
        # separator
        popmenu.AppendSeparator()
        # property
        popmenu.Append(ID_property,'Show Property')
        self.Bind(wx.EVT_MENU,self.on_delete_shape,id=ID_delete)
        self.Bind(wx.EVT_MENU,self.on_show_property, id=ID_property)
        self.PopupMenu(popmenu)
        popmenu.Destroy()
        
    def make_popmenu_2(self):
        """ creat the popup menu when right click on canvas(not on shape).
        """
        
        newtaskID = wx.NewId()
        newdataID = wx.NewId()
        deleteID = wx.NewId()
        taskID1 = wx.NewId()
        taskID2= wx.NewId()
        taskID3 = wx.NewId()
        taskID4 = wx.NewId()
        
        menu = wx.Menu()
        item_newdata = menu.Append(newdataID, 'New Data')
                
        submenu = wx.Menu()
        task1 = submenu.Append(taskID1,'Task1')
        task2 = submenu.Append(taskID2,'Task2')
        task3 = submenu.Append(taskID3,'Task3')
        task4 = submenu.Append(taskID4,'Task4')
        
        menu.AppendMenu(newtaskID,'New Task',submenu)
        #for i in list(('task1','task2','task3','task4')):
        self.Bind(wx.EVT_MENU,self.on_add_task,id= taskID1,id2=taskID4)
        self.Bind(wx.EVT_MENU,self.on_add_data,item_newdata)
        
        self.PopupMenu(menu)
        menu.Destroy()
        
    def add_linker(self,fromshape,toshape):
        """ creat the link between the data shape and task shape.
        """
        line = Linker(fromshape,toshape)
        
        line.Show(True)
        self.diagram.AddShape(line)
        fromshape.SetDraggable(True)
        self.lines.append(line)
        self.Refresh()
        return line

    def add_shape(self, shape, x, y, pen, brush, text):
        """ creat the shape on canvas, and add the new shape in shapes list.
        """
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

        self.evthandler = EvtHandler(canvas=self)
        self.evthandler.SetShape(shape)
        self.evthandler.SetPreviousHandler(shape.GetEventHandler())
        shape.SetEventHandler(self.evthandler)

        self.shapes.append(shape)
        return shape
    def on_delete_shape(self,event):
        """ event handler for delete shape.
        """
        shape = self.__selected_shape  
        print shape.GetParent(),'is deleted by delete_shape()'
        dc =wx.ClientDC(self)
        self.PrepareDC(dc)
        try:
            self.shapes.remove(shape.GetParent())  # remove the shape from the shapes list
            shape.GetParent().DeleteControlPoints()  # if we donot do it , the controlpoints will be remained
            shape.EraseLinks(dc)
            shape.GetParent().Delete()
            #self.line.Delete()
            #del self.lines[self.lines.index(self.line)]
            
            
        except:
            shape.Delete()
            
        print len(self.shapes),'shapes still in shapeslist'
        
        self.Refresh()
        
    def on_show_property(self,event):
        print 'show the property'
    def key_press(self,event):
        key = event.GetKeyCode()
        if key ==127:  # DELETE
            #self.diagram.shapes = [n for n in self.diagram.shapes if not n in self.select()]
            #for s in self.select():
            #    self.diagram.DeleteShape(s)
            #self.deselect() #remove nodes 
            for shape in self.shapes:
                if shape.Selected():
                    shape.Delete()
                    self.Refresh()
                    print shape,"is deleted by press del key"
    @property
    def selected_shape(self):
        return self.__selected_shape
    """
    def on_select(self, event):
        x,y = event.GetPosition()
        sx, sy = self.CalcUnscrolledPosition(x, y)
        shape = self.FindShape(sx, sy)
        print x,y
        self.__selected_shape = shape
    """
    def on_right(self,event):
        """ event handler of right click on canvas or shape
        """
        x,y = event.GetPosition()
        sx, sy = self.CalcUnscrolledPosition(x, y)
        
        #in ogl.CompositeShape, the getted shape is the child shape
        # we can use the shape.GetParent() get the parent shape.
        shape, attachment = self.FindShape(sx, sy)  
        self.__selected_shape = shape
        print x,y,shape,'is on_right'
        self.__x = sx
        self.__y = sy           

        if shape:
            # creat the popupmenu when right click on shape
            popmenu = self.make_popmenu()
        else:
            # creat the popupmenu when right click on canvas
            popmenu2 = self.make_popmenu_2()
            
    def on_motion(self,event):
        """ event handler of mouse moving on canvas
        """
        
        x,y = event.GetPosition()
        sx, sy = self.CalcUnscrolledPosition(x, y)
        shape, attachment = self.FindShape(sx, sy)
        # self.frame.SetStatusText("Pos: (%d, %d)" %
                                        # (sx, sy))
        
        try:
            shape_p = shape.GetParent()
        except:
            shape_p = shape
           
        if isinstance(shape, InputSocketShape) and not self.isDragging:
            
            self.zoomed_shapes = []
            self.zoomed_shapes.append(shape)#self.cache_shapes.append(shape)
            if not shape.is_zoomed()and self.isDragging==False:
                shape.zoom()
                self.Refresh()

        elif not isinstance(shape,InputSocketShape):
            try:
                if self.zoomed_shapes: # len(self.zoomed_shapes)!=0:
                    self.zoomed_shapes[0].set_default_size()
                    if self.zoomed_shapes[0].is_zoomed(): 
                        self.Refresh()
                    self.zoomed_shapes[0].enable_zoom(False)
                    del self.zoomed_shapes[self.zoomed_shapes.index(shape)]
                    #self.Refresh()
                    #self.zoomed_shapes.remove[0]
                    #self.zoomed_shapes.removeall()
                    
                    print self.zoomed_shapes[0].is_zoomed(),len(self.zoomed_shapes)#[:]
            except AttributeError as e:
                print type(e)
            except ValueError as v:
                print type(v)
      #      self.timer = wx.Timer(self)
      #      self.timer.Start(2000)
      #      self.Bind(wx.EVT_TIMER,self.on_time,self.timer)
            
        
        event.Skip(True)
            
    def on_time(self,event):
        self.popup_shape.Delete()
        self.diagram.RemoveShape(self.popup_shape)
        self.Unbind(wx.EVT_TIMER)
        self.Refresh()
        #event.Skip()
            
        #self.add_shape(InputSocketShape,sy,sx,wx.BLACK_PEN,wx.WHITE_BRUSH,'this is popup shape')
        """win = TaskPopupWindow(self.frame,
                             wx.SIMPLE_BORDER
                             )
        # Show the popup right below or above the button
        # depending on available screen space...
        btn = event.GetEventObject()
        pos = btn.ClientToScreen( (0,0) )
        #sz =  btn.GetSize()
        win.Position(pos,(sx,sy))
        win.Popup()
        """
        
        
    def on_left(self,event):
        """ event handler when left click on canvas 
        """
        #self.Unbind(wx.EVT_MOTION)
        x,y = event.GetPosition()
        sx, sy = self.CalcUnscrolledPosition(x, y)
        shape, attachment = self.FindShape(sx, sy)
        
        try:
            self.evthandler.OnLeftClick(x,y,keys='0',attachment=attachment)
        except:
            pass
        """self.__selected_shape = shape
        if isinstance(shape,wx.lib.ogl._basic.CircleShape):
            shape.GetParent().SetDraggable(False)
            #shape.SetDraggable(True)
            print 'i am circle' 
        elif shape: 
            self.Unbind(wx.EVT_LEFT_DOWN)
            shape.GetParent().SetDraggable(True)
        else:
            pass
            
        """
    def on_add_data(self,event):
        """ event handler for add data 
        """
        x = self.__x
        y = self.__y
        print 'add data'
        self.add_shape(DataShape(self,'name'), 
                x,y, wx.BLACK_PEN, wx.GREEN_BRUSH, ''
            )
        self.Refresh()
    def on_add_task(self,event):
        """ event handler for add task
        """
        x = self.__x
        y = self.__y
        # get the menu label
        menu_id = event.GetId()
        menu_obj = event.GetEventObject()
        menu_label = menu_obj.GetLabel(menu_id)
        # add task shape
        self.add_shape(TaskShape(self,name = menu_label), 
                x,y, wx.BLACK_PEN, wx.WHITE_BRUSH, ''
            )
        self.Refresh()
class TempCanvas(ogl.ShapeCanvas):
    """ the templete canvas.(now it's not used)
    """
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

        evthandler = EvtHandler( self.frame)
        evthandler.SetShape(shape)
        evthandler.SetPreviousHandler(shape.GetEventHandler())
        shape.SetEventHandler(evthandler)

        self.shapes.append(shape)
        return shape

class TaskShapeDropTarget(wx.PyDropTarget):
    """ this is a customs class for drag the text from the tempcanvas.
    """
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
        sx,sy =self.canvas.CalcUnscrolledPosition(x, y)
        self.canvas.add_shape(TaskShape(self.canvas,self.text),sx,sy, wx.BLACK_PEN, wx.WHITE_BRUSH, '')
            
        # what is returned signals the source what to do
        # with the original data (move, copy, etc.)  In this
        # case we just return the suggested value given to us.
        return d  
class FlowFrame(wx.Frame):
    """ the main frame of this flowcanvas 
    """
    def __init__(self, *args, **kwds):
        wx.Frame.__init__(self, *args, **kwds)
        # creat the statusbar
        self.StatusBar = wx.StatusBar(self)     

        #self.menu = self.make_menu()
        # creat the toolbar
        self.make_toolbar()
        # split the frame into two parts
        #splitter1 = wx.SplitterWindow(self, -1, style=wx.SP_3D)
        #splitter2 = wx.SplitterWindow(splitter1, -1, style=wx.SP_3D)
        #splitter1.SetSashGravity(0.8)
        #splitter2.SetSashGravity(0.2)
        
        self.SetTitle("Flow Work Canvas")
        self.SetSize((800,600))
        #self.SetBackgroundColour(wx.Colour(8, 197, 248))
        
        self.work_canvas = FlowCanvas(self)

        #self.temp_canvas = TempCanvas(splitter2,self)
        self.temp_canvas = wx.ListCtrl(self, -1, style=wx.LC_LIST)
        tasklist = ["Task1","Task2","Task3","Task4"]
        for i in range(len(tasklist)):        
            #self.temp_canvas.InsertStringItem(0,i)
            self.temp_canvas.InsertStringItem(i,tasklist[i])
            
        self.temp_canvas.Bind(wx.EVT_LIST_BEGIN_DRAG, self.on_drag_start)
        
        #splitter1.SplitVertically(self.work_canvas, splitter2)
        #splitter2.Initialize(self.temp_canvas)
        self.Center()
        # creat the droptarget 
        self.shapetaget = TaskShapeDropTarget(self.work_canvas)
        self.work_canvas.SetDropTarget(self.shapetaget)  
        
        size = wx.BoxSizer(wx.HORIZONTAL)
        size.Add(self.work_canvas,4,wx.EXPAND|wx.ALL,0)
        size.Add(self.temp_canvas,1,wx.RIGHT|wx.EXPAND,0)
        self.SetSizer(size)
        
        
    def make_menu(self):
        """ creat the menu bar in frame
        """
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
        
        for i in ('task1','task2','task3','task4'):
            self.Bind(wx.EVT_MENU,self.on_add_task,i)
        self.Bind(wx.EVT_MENU,self.on_add_data,item_newdata)
        self.Bind(wx.EVT_MENU,self.on_remove_shape,item_delete)
    
        
    def make_toolbar(self):
        """ creat the toolbar in frame.
        """ 
        toolbar = self.CreateToolBar()
        
        tsize = (24,24)
        new_bmp =  wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, tsize)
        open_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, tsize)
        copy_bmp = wx.ArtProvider.GetBitmap(wx.ART_COPY, wx.ART_TOOLBAR, tsize)
        paste_bmp= wx.ArtProvider.GetBitmap(wx.ART_PASTE, wx.ART_TOOLBAR, tsize)

        toolbar.SetToolBitmapSize(tsize)
        
        
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
        elif id ==20:
            print 'hello'
            import os
            wildcard = "Python source (*.py)|*.py|"     \
                     "Compiled Python (*.pyc)|*.pyc|" \
                     "SPAM files (*.spam)|*.spam|"    \
                     "Egg file (*.egg)|*.egg|"        \
                     "All files (*.*)|*.*"
            dlg = wx.FileDialog(
                self, message="Choose a file",
                defaultDir=os.getcwd(), 
                defaultFile="",
                wildcard=wildcard,
                style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
                )
            if dlg.ShowModal() == wx.ID_OK:
            # This returns a Python list of files that were selected.
                paths = dlg.GetPaths()
                print paths
            dlg.Destroy()
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
        print 'add data'
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
        shape = self.work_canvas.selected_shape
        if shape:
            shape.GetParent().DeleteControlPoints()
            shape.GetParent().Delete()
            #shape.Delete()
            self.work_canvas.Refresh()
        #shape = self.work_canvas.GetShape()
        #self.work_canvas.delete_shape()
        #self.work_canvas.Refresh()
#-------------------------------------------------------------------------------



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
