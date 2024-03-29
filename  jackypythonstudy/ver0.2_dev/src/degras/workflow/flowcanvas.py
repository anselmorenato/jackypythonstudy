# _*_ coding: utf-8 _*_
# Copyright (C)  2009 Biao Ma

# flowcanvas.py

"""
This file is base as OGL 
"""

import wx
import wx.lib.ogl as ogl
import pickle
import cPickle
import copy
# Global stuff----------------------------------------------------------------

clipboard = []

# ----------------------------------------------------------------------------
class NagaraDiagram(ogl.Diagram):
    def __intt__(self):
        
        ogl.Diagram.__init__(self)
    
    def saveFile(self,file=None):
        self.file = file
        if file is None:
            return
        #try:
        pickle.dump(self._shapeList,open(self.file, 'w'))
        #except:
            #print "problem saving this diagram"
            
    def loadFile(self,file=None):
        if file is None:
            return
        try:
            self._shapeList = pickle.load(open(file))
        except:
            print "problem loading this diagram"

#Abstract Classes ------------------------------------------------------------
class Selectable:
    '''
    Allows Shape to be selected
    '''
    def __init__(self):
        pass

class Resizeable:
    '''
    Creates resize Nodes that can be drug around the canvas
    to alter the shape or size of the Shape
    '''
    def __init__(self):
        pass
    
class Connectable:
    '''
    Creates connection nodes or ports 
    '''
    def __init__(self):
        self.input=1
        self.output=3
        self.connections=[] # this will be the list containing downstream connections

    def getPort(self,type,num):
        if type=='input':
            div = float(self.input+1.0)
            x=self.x[0]
        elif type=='output':
            div = float(self.output+1.0)
            x=self.x[1]
            
        dy=float(self.y[1] - self.y[0])/div
        y= self.y[0]+dy*(num+1)
        return(x,y)

class Attributable:
    '''
    Allows AttributeEditor to edit specified properties
    of the Shape
    '''
    def __init__(self):
        self.attributes=[]

    def AddAttribute(self,name):
        self.attributes.append(name)

    def AddAttributes(self,atts):
        self.attributes.extend(atts)
        
    def RemoveAttribute(self,name):
        self.attributes.remove(name)

# Nodes----------------------------------------------------------------------
class PointShape(ogl.Shape):
    def __init__(self,x=20,y=20,size=4,type='rect'):
        ogl.Shape.__init__(self)
        self.type=type
        self.size=size
        if self.type=='rect':
            self.graphic = ogl.RectangleShape(x,y)
        self.graphic.pen = self.pen
        self.graphic.fill = self.fill

    def moveto(self,x,y):
        self.x = x
        self.y = y
        size = self.size
        self.graphic.x=[x-size,x+size]
        self.graphic.y=[y-size,y+size]

    def move(self,x,y):
        self.x = map((lambda v: v+x), self.x)
        self.y = map((lambda v: v+y), self.y)
        self.graphic.move(x,y)

    def HitTest(self, x, y):
        return self.graphic.HitTest(x,y)

    def draw(self,dc):
        self.graphic.pen = self.pen
        self.graphic.fill = self.fill
        self.graphic.draw(dc)

class Node(PointShape):
    def __init__(self,item,index,cf):
        self.item=item
        self.index = index
        self.cf =cf
        PointShape.__init__(self)

    def showProperties(self):
        self.item.showProperties

class ConnectableNode(Node):
    def __init__(self,item,index,cf):
        Node.__init__(self,item,index,cf)

class INode(ConnectableNode):
    def __init__(self,item,index,cf):
        ConnectableNode.__init__(self,item,index,cf)

    def leftUp(self,items):
        if len(items)==1 and isinstance(items[0],ConnectionShape):
            if items[0].output is None:
                items[0].setOutput(self.item,self.index)

    def move(self,x,y):
        self.cf.deselect()
        ci = ConnectionShape()
        self.cf.diagram.shapes.insert(0, ci)
        ci.setOutput(self.item,self.index)
        ci.x[0],ci.y[0] = self.item.getPort('input',self.index)
        self.cf.showOutputs()
        self.cf.select(ci)

    def draw(self,dc):
        x,y=self.item.getPort('input',self.index)
        self.moveto(x,y)
        PointShape.draw(self,dc)

class ONode(ConnectableNode):
    def __init__(self,item,index,cf):
        ConnectableNode.__init__(self,item,index,cf)

    def move(self,x,y):
        self.cf.deselect()
        ci = ConnectionShape()
        self.cf.diagram.shapes.insert(0, ci)
        ci.setInput(self.item,self.index)
        ci.x[1],ci.y[1] = self.item.getPort('output',self.index)
        self.cf.showInputs()
        self.cf.select(ci)

    def leftUp(self,items):
        if len(items)==1 and isinstance(items[0],ConnectionShape):
            if items[0].input is None:
                items[0].setInput(self.item,self.index)


    def draw(self,dc):
        x,y=self.item.getPort('output',self.index)
        self.moveto(x,y)
        PointShape.draw(self,dc)

# ----------------------------------------------------------------------------
class NagaraShapeSavedData:
    """Used to store data of NagaraShape for workflow saves and loads.
    """
    
    #---------------------------------------
    def __init__(self, shape):
        self.theId = id(shape)#.GetId()
        self.shapeclass = shape.GetClassName()  #__class__.__name__
        #self.theNodeConfiguration = aBoardNodeShape.theNodeConfiguration
        #self.theElements = aBoardNodeShape.theElements
        self.theX = shape.GetX()
        self.theY = shape.GetY()
        try :
            self.theLable = shape.get_label()
        except AttributeError as ate:
            print ate
            self.theLable = ''
        self.theLines = []
        for myLine in shape.GetLines():
            myLineID = id(myLine.GetTo())
            if not myLineID == self.theId:
                self.theLines.append(myLineID)
        if isinstance(shape,Linker):
            self.fromshape = id(shape.GetFrom())
            self.toshape = id(shape.GetTo())
            print 'from',self.fromshape,'to',self.toshape
    #---------------------------------------   
    def accept(self, aVisitor):
        if Visitable.accept(self, aVisitor) == False:
            return False
        myValue = aVisitor.visitBoardNodeShapeSavedData(self)
        if myValue == None:
            return True
        return myValue
#-----------------------------------------------------------------------------
class NagaraBlock(ogl.CompositeShape,Selectable,Connectable,Attributable):
    def __init__(self):
        ogl.CompositeShape.__init__(self)
        Attributable.__init__(self)
        
        self.properties = ['project',
                           'id',
                           'name',
                           'state',
                           'jms',
                           'location',
                           'expected_time',
                           'start_time',
                           'finish_time',
                           'available_request'
                           ]
        self.AddAttributes(['label',
                           'pen',
                           'fill',
                           'input',
                           'output'
                           ])
        self.label = 'Nagara Block'
        
    def OnLeftClick(self,x,y,keys=0,attachment=0):
        print self
        if isinstance(self,NagaraBlock) and keys==2: # Ctrl key
            d=wx.TextEntryDialog(None,'Shape Label',defaultValue=self.label,style=wx.OK)
            d.ShowModal()
            self.label = d.GetValue()
        
    def OnLeftDclick(self,x,y,keys=0,shape=None):
        print shape,'is double click'
        
    def Copy(self):
        
        return copy.deepcopy(self)
        
        
class DataShape(NagaraBlock):
    """ this is the composite data shape.
    """
    def __init__(self, canvas, name=''):
        NagaraBlock.__init__(self)
        self.canvas = canvas
        #self.attributes = ['lable','pen','fill','data','output']
        self.label = name
        self.pen = self.GetPen()
        self.fill = self.GetBrush()
        self.data = None
        self.input = None
        self.output = None
        self.SetCanvas(canvas)        
        
        self.shape1 = shape1 = ogl.RectangleShape(100, 60)
        shape1.AddText(self.label)
        self.AddChild(shape1)
        #shape2 = ogl.CircleShape(10)
        self.shape2 = shape2 = Connector(canvas, self)
        shape2.SetBrush(wx.GREEN_BRUSH)
        shape2.SetY(-35)
        self.AddChild(shape2)
        #shape2.SetDraggable(1)
        constraint = ogl.Constraint(ogl.CONSTRAINT_RIGHT_OF ,shape1, [shape2])
        self.AddConstraint(constraint)
        self.Recompute()
        shape1.SetSensitivityFilter(0)
        shape2.SetSensitivityFilter(5)
    def get_label(self):
        return self.label
    def set_label(self,label):
        self.label = label
        
    def _delete(self):
        self.Delete()
    def OnLeftClick(self,keys):
        print self
        if isinstance(self,NagaraBlock) and keys==2: # Ctrl key
            d=wx.TextEntryDialog(None,'Shape Label',defaultValue=self.label,style=wx.OK)
            d.ShowModal()
            self.label = d.GetValue()
        #if isinstance(self,DataShape):
        self.AddChild(self.shape2)
        self.canvas.Refresh(True)
    
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

    def Copy(self):
        
        return copy.deepcopy(self)
        

#----------------------------------------------------------------------
# Begin here make the shapes for TaskShape

class TaskShape(NagaraBlock):
    """
    This shape is Consists of three parts, InputSocketShape, Middleshape and OutputsocketShape.
    """
    def __init__(self, canvas,name =''):
        NagaraBlock.__init__(self)
        self.SetCanvas(canvas)
        self.canvas = canvas
        self.taskobject_name = name
        self.label = name
        self.pen = self.GetPen()
        self.fill = self.GetBrush()
        self.data = None
        self.input = None
        self.output = None

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
        middleshape.SetDraggable(False)
        inputshape1.SetDraggable(0)
        outputshape.SetDraggable(0)

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
        
    def get_label(self):
        return self.label
    def set_label(self,label):
        self.label = label
    

        
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
        print width, height
        
        while 30 > width and 70 > height :
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
        
    def Copy(self):
        
        return copy.deepcopy(self)
            
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
    def Copy(self):
        
        return copy.deepcopy(self)
class OutputSocketShape(ogl.DrawnShape):
    """this shape is one part of the TaskShape"""
    def __init__(self):
        ogl.DrawnShape.__init__(self)
    def Copy(self):
        
        return copy.deepcopy(self)    

# TaskShape is end here
#----------------------------------------------------------------------
class Linker(ogl.LineShape):
    """ the link line from datashape to taskshape.
    """
    def __init__(self,fromshape,toshape,*args,**cwdargs):
        ogl.LineShape.__init__(self)
       
        fromshape = fromshape
        toshape = toshape

        self.SetPen(wx.BLACK_PEN)
        self.SetBrush(wx.BLACK_BRUSH)
        self.AddArrow(ogl.ARROW_ARROW)
        self.MakeLineControlPoints(2)
        fromshape.AddLine(self, toshape)
        
        self.Show(True)
        #self.Show(True)
        
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
        self.canvas = canvas = shape.GetCanvas()
        dc = wx.ClientDC(self.canvas)
        canvas.PrepareDC(dc)
        sx,sy = self.canvas.CalcUnscrolledPosition(x, y)
        _shape,attachment =self.canvas.FindShape(sx,sy)
        if isinstance(self.canvas,TempCanvas):
            pass
        
        elif isinstance(shape, Selectable):
            canvas.select(shape=shape)
            """
            shape.OnLeftClick(keys)  
            canvas.Refresh(True)
            if shape.Selected():
                shape.Select(False, dc)
                canvas.selected_shapes.remove(shape)
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
                canvas.selected_shapes.append(shape)
    
                if toUnselect:
                    for s in toUnselect:
                        s.Select(False, dc)
                        canvas.selected_shapes.remove(s)
    
                    ##canvas.Redraw(dc)
                    canvas.Refresh(True) #Flase 
            """
        self.up_data_statusbar(shape)
    def OnBeginDragLeft(self,x,y,key=0,attachment=0):
        #self.canvas.Unbind(wx.EVT_MOTION)
        ogl.ShapeEvtHandler.OnBeginDragLeft(self, x, y, keys = 0, attachment = 0)
        shape = self.GetShape()
        sx,sy = self.canvas.CalcUnscrolledPosition(x, y)
        _shape,attachment = self.canvas.FindShape(x,y) 
        if isinstance(self.canvas,TempCanvas):
            self.canvas.GetParent().on_drag_start(shape)
        elif isinstance(self.canvas,FlowCanvas):
            self.canvas._isDragging(True)
                   
            print 'drag begin at',x,y
       
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
        if isinstance(_shape,TaskShape)& isinstance(shape,DataShape):
            print 'now task is start'
            print shape
            fromShape = shape
            toShape = _shape_p
            
            
            self.canvas.add_linker(fromShape,toShape)
            self.canvas._isDragging(False)
            self.canvas.Refresh(True)
            #shape.SetDraggable(True)
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
        print 'hello'
            
class FlowCanvas(ogl.ShapeCanvas):

    def __init__(self, parent,frame):
        ogl.ShapeCanvas.__init__(self, parent)
        ogl.OGLInitialize()
        maxWidth  = 1500
        maxHeight = 1500
        self.SetScrollbars(20, 20, maxWidth/20, maxHeight/20)
        self.SetBackgroundColour("LIGHT BLUE") 
        
        # diagram
        self.diagram = NagaraDiagram()
        self.SetDiagram(self.diagram)
        self.diagram.SetCanvas(self)

        # shapes        
        self.shapes = []  
        self.save_gdi = []
        self.lines = []
        self.nodes = []
        self.selected_shapes =[]
        self.isDragging = False
        
        # dc client
        self.dc = wx.ClientDC(self)
        self.PrepareDC(self.dc)

        rRectBrush = wx.Brush("GREEN", wx.SOLID)
        dsBrush = wx.Brush("white", wx.SOLID)
        
        self.Bind(wx.EVT_RIGHT_DOWN,self.on_right)
        self.Bind(wx.EVT_MOTION,self.on_motion)
        self.Bind(wx.EVT_KEY_DOWN,self.key_press)
        #self.Bind(wx.EVT_PAINT,self.on_paintevent)
        #self.Bind(wx.EVT_CHILD_FOCUS,self.on_motion)
        #self.Bind(wx.EVT_LEFT_DOWN,self.on_left)
        #self.Bind(wx.EVT_ENTER_WINDOW,self.on_motion)
        
        # destroy event
        #wx.EVT_WINDOW_DESTROY(self, self.OnDestroy)
        
        # rectangle for dragging
        self.theDragRect = None
        self.theDragRectWidth = 0
        self.theDragRectHeight = 0
        self.theIsOnGroupSelection = False
    def OnLeftClick(self,x,y,keys):
        """
        """
        
        for shape in self.shapes:
            if shape.Selected:
                shape.Select(False)
                self.Refresh(True)
    #---------------------------------------
    def OnBeginDragLeft(self, x, y, keys):
        """
        """
        
        self.theIsOnGroupSelection = False
        self.theDragRectWidth = 0.0
        self.theDragRectHeight = 0.0
        if self.theDragRect is not None :
            self.RemoveShape( self.theDragRect )
            self.theDragRect = None
            self.Refresh()
                
        self.theDragRect = ogl.RectangleShape( self.theDragRectWidth, self.theDragRectHeight)
        self.theDragRect.SetCentreResize(True)


        self.add_shape(self.theDragRect, x, y, wx.BLACK_DASHED_PEN, wx.TRANSPARENT_BRUSH, None)
        self.Refresh()        
    #---------------------------------------
    def OnDragLeft(self, draw, x, y, keys ):
        """
        """

        # Note : The drawing of the selection rectangle only supports selection
        # from left-to-right and top-to-bottom. Add to all directions in the future.

        myX = self.theDragRect.GetX() - self.theDragRectWidth / 2
        myY = self.theDragRect.GetY() - self.theDragRectHeight / 2

        self.theDragRectWidth = x - self.theDragRect.GetX() - self.theDragRectWidth / 2
        self.theDragRectHeight = y - self.theDragRect.GetY() - self.theDragRectHeight / 2

        self.theDragRect.SetX( myX + self.theDragRectWidth / 2 )
        self.theDragRect.SetY( myY + self.theDragRectHeight / 2 )

        if (self.theDragRectWidth > 0) or (self.theDragRectHeight < 0) :
            self.theDragRect.SetSize( self.theDragRectWidth, self.theDragRectHeight )
    
            myScrollX, myScrollY = self.GetViewStart()
            myClientX, myClientY = self.GetClientSize()
            myBorderX = myScrollX * 20 + myClientX
            myBorderY = myScrollY * 20 + myClientY
            
            myDoScroll = False
            if ( myX + self.theDragRectWidth ) >= ( myBorderX - 50 ) :
                myScrollX = myScrollX + 1
                myDoScroll = True
            if ( myY + self.theDragRectHeight ) >= ( myBorderY - 50 ) :
                myScrollY = myScrollY + 1
                myDoScroll = True
            if myDoScroll :
                self.Scroll(myScrollX, myScrollY)
            
            self.theWidth = self.theDragRectWidth
            self.theHeight = self.theDragRectHeight
            
            self.Refresh()
    #---------------------------------------
    def OnEndDragLeft(self, x, y, keys):
        """
        """
        
        # Select all shapes under the rectangle

        # Get min and max coordinates 
        
        myXmin = self.theDragRect.GetX()
        myYmin = self.theDragRect.GetY()
        myXmax = self.theDragRect.GetX() + self.theWidth
        myYmax = self.theDragRect.GetY() + self.theHeight

        # Remove the selection rectangle
        self.RemoveShape( self.theDragRect )
        self.theDragRect = None
        self.Refresh()

        # Select the shapes within the ranges
        dc = wx.ClientDC(self)
        self.PrepareDC(dc)
        myShapeList = self.GetDiagram().GetShapeList()
        #myShapeList = self.shapes
        mySelectedList = []

        for myShape in myShapeList:
            if myShape.Selected() :
                mySelectedList.append( myShape )

        for myShape in mySelectedList :
            myShape.Select(False, dc)

        #myShapeList = self.shapes
        myShapeList = self.GetDiagram().GetShapeList()
        for myShape in myShapeList:
            if (myShape.GetX() >= myXmin) and (myShape.GetX() <= myXmax) and \
               (myShape.GetY() >= myYmin) and (myShape.GetY() <= myYmax) :
                if not myShape.Selected() and not isinstance(myShape, ogl.ControlPoint ):
                    myShape.Select(True, dc)
                    self.selected_shapes.append(myShape)
                    self.theIsOnGroupSelection = True
        
        self.Redraw(dc)
    
    def _isDragging(self,dragging):
        self.isDragging = dragging
 
    def select(self,event=None,shape=None):
        canvas = self
        dc = wx.ClientDC(canvas)
        canvas.PrepareDC(dc)
      #  if item is None:
      #      return self.selected_shapes
        
      #  if isinstance(item,Node):
      #      del self.selectedShapes[:]
      #      self.selectedShapes.append(item) # items here is a single node
      #      return
                
      #  if not item in self.selectedShapes:
      #      self.selectedShapes.append(item)
      #      item.OnSelect(None)
      #      if isinstance(item,Connectable):            
      #          self.nodes.extend( [INode(item,n,self) for n in range(item.input)] )
      #          self.nodes.extend( [ONode(item,n,self) for n in range(item.output)] )
      #      if isinstance(item,Resizeable):            
      #          self.nodes.extend( [ResizeableNode(item,n,self) for n in range(len(item.x))] )
      #-----------------------------------        
        if shape is None:
            if self.selected_shapes:
                for s in self.selected_shapes:
                    s.Select(False,dc)
            return self.selected_shapes
        
        if shape.Selected():
            shape.Select(False, dc)
            if shape in canvas.selected_shapes:
                canvas.selected_shapes.remove(shape)
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
            canvas.selected_shapes.append(shape)

            if toUnselect:
                for s in toUnselect:
                    s.Select(False, dc)
                    canvas.selected_shapes.remove(s)

                ##canvas.Redraw(dc)
                canvas.Refresh(True) #Flase
        #if event:
        
    def make_popmenu(self,shape):
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
        item_show_property = popmenu.Append(ID_property,'Show Property')
        if isinstance(shape,Linker):
            item_show_property.Enable(False)
            
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
        
        fromshape.SetDraggable(True)
        
        self.evthandler = EvtHandler(canvas=self)
        self.evthandler.SetShape(line)
        self.evthandler.SetPreviousHandler(line.GetEventHandler())
        line.SetEventHandler(self.evthandler)
        # add line in list
        self.diagram.AddShape(line)
        self.shapes.append(line)
        fromshape._lines.append(line)
        toshape._lines.append(line)
        self.Refresh()
        return line

    def add_shape(self, shape, x=0, y=0, pen=wx.BLACK_PEN, brush=wx.WHITE_BRUSH, text=''):
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
        #return shape
        
    def delete_shape(self,shape):
        if shape._lines:
            print shape._lines
            #shape.RemoveLine(shape._lines[0])
        shape.Delete()
        if shape in self.selected_shapes:
            self.selected_shapes.remove(shape)
        self.shapes.remove(shape)
        
        self.Refresh()
    #---------------------------------------
    def removeSelectedShapes(self):
        shapeList = self.diagram.GetShapeList()
        toUnselect = []
        for s in shapeList:
            if s.Selected():
                toUnselect.append(s)
                if not isinstance(s, ogl.LineShape):
                    myLinesToRemove = s.GetLines()
                    print 'linelist',myLinesToRemove
                    # remove the line from fromshape,toshape,canvas.shapes[]
                    for line in myLinesToRemove:
                        #line.GetFrom()._lines.remove(line)
                        #line.GetTo()._lines.remove(line)
                        #self.shapes.remove(line)
                        line.Delete()
                    
                    #myNodeDataBase = NodeDataBase()
                    #if myNodeDataBase.theRootNode == s :
                    #    myNodeDataBase.theRootNode = None
                    self.RemoveShape(s)
                    self.shapes.remove(s)
                    s.Delete()
##                else :
##                    s.GetFrom().theElements.remove(s.GetTo().GetRegions()[0].GetText())
##                    s.GetTo().RemoveLine(s)
##                    s.GetFrom().RemoveLine(s)
##                    self.RemoveShape(s)
        self.Refresh()
                
        if toUnselect:
            for s in toUnselect:
                s.Select(False, self.dc)
                self.Redraw(self.dc)

    def on_delete_shape(self,event):
        """ event handler for delete shape.
        """
        try:
            #shape = [n for n in self.shapes if n.Selected()][0]
            #self.delete_shape(shape)
            pass
        except IndexError:
            print self.selected_shapes
        self.removeSelectedShapes()
        self.Refresh()    
        print self.shapes,len(self.shapes),'shapes still in shapeslist'
        print self.selected_shapes,len(self.selected_shapes)
    
    # request for event
    def on_show_property(self,event):
        print 'show the property'
        frame = wx.Frame(None,-1,title='property',size=(280,380))
        try:
            parent = self.GetParent().get_pane('PropertyView')
            print parent,'is parent '
            f = AttributeEditor(parent,-1,'propertys',self.selected_shape.GetParent())
            
        except:
            f = AttributeEditor(frame,-1,'propertys',self.selected_shape.GetParent())
        frame.Show(True)
    def key_press(self,event):
        key = event.GetKeyCode()
        # get the selected shape list
        shape = [n for n in self.shapes if n.Selected()]
        if key ==127:  # DELETE
            #self.diagram.shapes = [n for n in self.diagram.shapes if not n in self.select()]
            #for s in self.select():
            #    self.diagram.DeleteShape(s)
            #self.deselect() #remove nodes 
            #for shape in self.shapes:
            #    if shape.Selected():
            #        #self.shapes.remove(shape)
            #        self.on_delete_shape(event)
                    #shape.Delete()
            #if self.selected_shapes:
                #self.on_delete_shape(event)
            self.removeSelectedShapes()
            #else:
            #    dlg = wx.MessageDialog(None,'The [Delete] key is pressed, but No shape has selected!',style=wx.OK)
            #    dlg.ShowModal()
            #    print 'no shape had selected'
            print shape,"is deleted by press del key"
        elif key ==67 and event.ControlDown():  # COPY
            print 'why this print'
            del clipboard[:]
            for i in shape:
                clipboard.append(i)
                print i,'is add in clipboard',clipboard
        elif key ==86 and event.ControlDown():  # PASTE
            for i in clipboard:
                print i,' is pasted '
                self.add_shape(i.Copy())
        elif key == 9: # TAB
            if len(self.shapes)==0:
                return
            
            if shape:
                ind = self.shapes.index(shape[0])
                shape[0].Select(False)
                #if 
                self.selected_shapes.remove(shape[0])
                try:
                    self.shapes[ind+1].Select(True)
                    self.selected_shapes.append(self.shapes[ind+1])
                except:
                    self.shapes[0].Select(True)
                    self.selected_shapes.append(self.shapes[0])
            else:
                self.shapes[0].Select(True)
                self.selected_shapes.append(self.shapes[0])
        self.Refresh()
        
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
        
        # in ogl.CompositeShape, the shape which finded is the child shape
        # we can use the shape.GetParent() get the parent shape.
        shape, attachment = self.FindShape(sx, sy)  
        self.__selected_shape = shape
        print x,y,shape,'is on_right'
        print 'diagrm list',self.diagram._shapeList
        print 'canvas list',self.shapes
        self.__x = sx
        self.__y = sy           

        if shape:
            
            if shape.GetParent():
                # make the shape is selected
                shape.GetParent().Select(True) 
            else:
                shape.Select(True)
            # creat the popupmenu when right click on shape
            popmenu = self.make_popmenu(shape)
            
        else:
            # creat the popupmenu when right click on canvas
            popmenu2 = self.make_popmenu_2()
    
    def on_paintevent(self,event):
        dc = wx.PaintDC(self)
        self.PrepareDC(dc)
        dc.SetUserScale(1.0,1.0)
        dc.BeginDrawing()
        #for shape in self.diagram._shapeList:
        #    shape.SetCanvas(self)
        dc.EndDrawing()
        
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
                
                # import threading 
                # t = threading.Thread(target=shape.zoom, args=[])
                # t.start()
                self.Refresh()

        elif not isinstance(shape,InputSocketShape):
            try:
                if self.zoomed_shapes: # len(self.zoomed_shapes)!=0:
                    self.zoomed_shapes[0].set_default_size()
                    if self.zoomed_shapes[0].is_zoomed(): 
                        self.Refresh()
                    self.zoomed_shapes[0].enable_zoom(False)
                    del self.zoomed_shapes[self.zoomed_shapes.index(shape)]
                   
            except AttributeError as e:
                pass
            except ValueError as v:
                pass
        
        event.Skip(True)
            

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
        self.select()
        self.Refresh(True)
        event.Skip(True)

    def on_add_data(self,event):
        """ event handler for add data 
        """
        x = self.__x
        y = self.__y
        print 'add data'
        s = DataShape(self,'Data')
        #s = ogl.RectangleShape(100,200)
        self.add_shape(s, 
                x,y, wx.BLACK_PEN, wx.GREEN_BRUSH, ''
            )
        #self.diagram.AddShape(s)
        #s.Show(True)
        
                              
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
        taskshape = TaskShape(self,name = menu_label)
        self.add_shape(taskshape, 
                x,y, wx.BLACK_PEN, wx.WHITE_BRUSH, ''
            )
        datashape = DataShape(self,name='output')
        self.add_shape(datashape,x+200,y+50)
        self.add_linker(taskshape,datashape)
        self.Refresh()

class TempCanvas(ogl.ShapeCanvas):
    """ the templete canvas.(now it's not used)
    """
    def __init__(self, parent,frame):
        ogl.ShapeCanvas.__init__(self, parent)

        maxWidth  = 1500
        maxHeight = 1500
        self.SetScrollbars(20, 20, maxWidth/20, maxHeight/20)

        #self.log = log
        self.frame = frame
        self.SetBackgroundColour("LIGHT GREY") #wx.WHITE)
        self.diagram = ogl.Diagram()
        self.SetDiagram(self.diagram)
        self.diagram.SetCanvas(self)
        self.shapes = []
        self.save_gdi = []
        
    def add_shape(self, shape, x, y, pen=wx.BLACK_PEN, brush=wx.WHITE_BRUSH, text=''):
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

        evthandler = EvtHandler( self)
        evthandler.SetShape(shape)
        evthandler.SetPreviousHandler(shape.GetEventHandler())
        shape.SetEventHandler(evthandler)

        self.shapes.append(shape)
        return shape
    
    def OnBeginDragLeft(self, x, y, keys = 0):
        #self.frame.on_drag_start()
        pass
class TaskShapeDropTarget(wx.PyDropTarget):
    """ this is a customs class for drag the text from the tempcanvas.
    """
    def __init__(self, canvas):
        wx.PyDropTarget.__init__(self)
        #self.log = log
        self.canvas = canvas

        # specify the type of data we will accept
        self.data = wx.CustomDataObject('NagaraShape')
        print self.data.GetSize()
        
        #self.data = wx.TextDataObject()
        self.SetDataObject(self.data)
    
    def OnDrop(self, x, y):
        
        self.canvas.Refresh()
    def OnData(self, x, y, d):
        # copy the data from the drag source to our data object 
        if self.GetData():
            # unpickle the pickled data
            pickled_data = self.data.GetData()
            self.shapesinfo = pickle.loads(pickled_data)
            #self.text = self.data.GetText()
            name =self.shapesinfo
            sx,sy =self.canvas.CalcUnscrolledPosition(x, y)
            self.canvas.add_shape(TaskShape(self.canvas,name),sx,sy, wx.BLACK_PEN, wx.WHITE_BRUSH, '')
                
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
        
        self.SetTitle("Flow Work Canvas")
        self.SetSize((800,600))
        #self.SetBackgroundColour(wx.Colour(8, 197, 248))
        
        self.work_canvas = FlowCanvas(self,frame = self)

        self.temp_canvas = TempCanvas(self,self)

        #self.temp_canvas = wx.ListCtrl(self, -1, style=wx.LC_LIST)
        self.tasklist = ["Task1","Task2","Task3","Task4"]
    
        shape = TaskShape(self.temp_canvas, self.tasklist[0])
        x = shape._width/2
        y = shape._height/2
        self.temp_canvas.add_shape(shape,x,y)
        shape.SetDraggable(0)
        for t in self.tasklist[1:]:
            shape = TaskShape(self.temp_canvas,t)
            y += 150 
            self.temp_canvas.add_shape(shape,x,y)
            shape.SetDraggable(0)    
            
        """
        for i in range(len(self.tasklist)):        
            #self.temp_canvas.InsertStringItem(0,i)
            self.temp_canvas.InsertStringItem(i,self.tasklist[i])
            
        self.temp_canvas.Bind(wx.EVT_LIST_BEGIN_DRAG, self.on_drag_start)
        """

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
        save_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR, tsize)
        delete_bmp = wx.ArtProvider_GetBitmap(wx.ART_DELETE,wx.ART_TOOLBAR, tsize)

        toolbar.SetToolBitmapSize(tsize)
        
        
        toolbar.AddLabelTool(10, "New Date", new_bmp, shortHelp="Add new date", longHelp="Long help for 'New'")
        self.Bind(wx.EVT_TOOL, self.on_tool_click, id=10)
        #self.Bind(wx.EVT_TOOL_RCLICKED, self.OnToolRClick, id=10)

        #tb.AddSimpleTool(20, open_bmp, "Open", "Long help for 'Open'")
        toolbar.AddLabelTool(20, "Open", open_bmp, shortHelp="Open", longHelp="Long help for 'Open'")
        self.Bind(wx.EVT_TOOL, self.on_tool_click, id=20)
        #self.Bind(wx.EVT_TOOL_RCLICKED, self.OnToolRClick, id=20)

        toolbar.AddLabelTool(30, "Save", save_bmp, shortHelp="Save", longHelp="Long help for 'Save'")
        self.Bind(wx.EVT_TOOL, self.on_tool_click, id=30)
        
        toolbar.AddLabelTool(40, "Delete", delete_bmp, shortHelp="Delete", longHelp="Long help for 'Delete'")
        self.Bind(wx.EVT_TOOL, self.on_tool_click, id=40)
        
        # Final thing to do for a toolbar is call the Realize() method. This
        # causes it to render (more or less, that is).
        toolbar.Realize()
        
    def on_tool_click(self,event):
        import os,sys
        
        toolid = event.GetId()
        if toolid == 10:
            self.on_add_data(event)
            self.work_canvas.Refresh()
        elif toolid ==20:  # open file
            print 'open file'
            
            wildcard = "Nagara shape flie (*.nas)|*.nas|" \
                     "Python source (*.py)|*.py|"\
                     "Compiled Python (*.pyc)|*.pyc|" \
                     "SPAM files (*.spam)|*.spam|"    \
                     "Egg file (*.egg)|*.egg|"\
                     "All files (*.*)|*.*"
            dlg = wx.FileDialog(
                self, message="Choose a file",
                defaultDir=os.getcwd(), 
                defaultFile="",
                wildcard=wildcard,
                style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
                )
            if dlg.ShowModal() == wx.ID_OK:
                # remove the current shapes from diagram before load saved shapes.
                shapes = self.work_canvas.diagram._shapeList
                del shapes[:]
                paths = dlg.GetPaths()
                # unpickle the saved data from file.
                mfile = open(dlg.GetFilename())
                shapesinfo = pickle.load(mfile)
                print 'pickled data list is',shapesinfo
                # creat the new shape.
                newshapes = {}
                shapesinfolist = shapesinfo.values()
                
                for shapeinfo in shapesinfolist:
                    x= shapeinfo.theX
                    y = shapeinfo.theY
                    lable = shapeinfo.theLable
                    
                    shapeclass = shapeinfo.shapeclass
                    if shapeclass == 'DataShape' or shapeclass == 'TaskShape':   
                    
                        newshape = eval(shapeclass)(self.work_canvas,name=lable)
                        newshapes[shapeinfo.theId] = newshape
                        self.work_canvas.add_shape(newshape,x,y)
                    
                    elif shapeclass == 'Linker':
                        fromshape = newshapes[shapeinfo.fromshape]
                        toshape = newshapes[shapeinfo.toshape]
                        newshape = Linker(fromshape,toshape)
                        self.work_canvas.add_linker(fromshape,toshape)
                    elif shapeclass == 'InputSocketShape':
                        newshape = InputSocketShape()
                        newshapes[shapeinfo.theId] = newshape
                        self.work_canvas.diagram._shapeList.append(newshape) 
                    """
                    print 'the shapeclass is ',shapeclass
                    if shapeclass == 'DataShape':
                        print 'that ok'
                        self.work_canvas.add_shape(newshape,x,y)
                    elif shapeclass == 'TaskShape':
                        newshape = TaskShape(self.work_canvas,name=lable)
                        newshapes[shapeinfo.theId] = newshape
                        self.work_canvas.add_shape(newshape,x,y)
                    """
                    self.work_canvas.Refresh(True)
                print newshapes   
                mfile.close()
                
            dlg.Destroy()
        elif toolid ==30:  #save file
            print 'save file ======='
            dlg = wx.FileDialog(
                self, message="diagram file save as...", defaultDir=os.getcwd(), 
                defaultFile="", wildcard="Nagara shape file (*.nas)|*.nas", style=wx.SAVE)
            dlg.SetFilterIndex(2)
            if dlg.ShowModal() == wx.ID_OK:
                # creat the file to save the pickled shapes info.    
                fp = open(dlg.GetFilename(),'w')
                shapes = self.work_canvas.shapes
                shapesdia = self.work_canvas.diagram._shapeList
                print 'diagram shapelist',shapesdia
                print 'canvas shapelist',shapes 
                # creat the dict to save property of shapes 
                shd ={}
                for shape in shapesdia:
                    print 'shape is ',shape,id(shape),shape.GetId()
                    #attributes = shape.attributes
                    # save the shape attributes in SaveData class
                    val = NagaraShapeSavedData(shape)
                    print 'val is ',val
                    #shd[id(shape)] = attributes
                    shd[id(shape)] = val
                print 'shd is ',shd    
                pickle.dump(shd,fp)
                #self.work_canvas.diagram.saveFile('save_test.txt')
        elif toolid == 40: #delete all shape
            shapes = self.work_canvas.diagram._shapeList
            del shapes[:]
            del self.work_canvas.shapes[:]
            self.work_canvas.Refresh(True)
            
    def on_drag_start(self,shape):
        """ 
        """
        # creat the data
        self.data = wx.CustomDataObject('Nagarashape')
        
        # pickle the shape attributes
        dragshape = shape.label  # [s.label for s in self.temp_canvas.shapes]
        pickled_data = pickle.dumps(dragshape)
        self.data.SetData(pickled_data)

        #self.data = wx.TextDataObject(self.temp_canvas.GetItemText(event.GetIndex()))
        
        # creat the dropsource
        dropsource = wx.DropSource(self.temp_canvas)
        dropsource.SetData(self.data)
        dropsource.DoDragDrop(wx.Drag_CopyOnly)

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
        

#-------------------------------------------------------------------------------
class AttributeEditor(wx.Panel):
    def __init__(self, parent, ID, title,item):
        wx.Panel.__init__(self, parent, ID, 
                         wx.DefaultPosition, wx.Size(200, 450))
        self.item = item
        # Create a box sizer for self
        box = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(box)
        
        tID = wx.NewId()
        self.list = wx.ListCtrl(self, tID, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT)
        self.SetSize(self.GetSize())
 
        self.list.InsertColumn(0, "Attribute",width=100)
        self.list.InsertColumn(1, "Value",width=100)

        accept = wx.Button(self, wx.NewId(), "Accept",size=(40,20))

        for c in range(len(item.attributes)):
            self.list.InsertStringItem(c , "")
            self.list.SetStringItem(c, 0, str(item.attributes[c]))
            temp = str( eval("item." + str(item.attributes[c])))
            self.list.SetStringItem(c, 1, temp)
        
        self.text    = wx.TextCtrl(self,wx.NewId(), "", style=wx.TE_MULTILINE)
        
        box.Add(self.list, 1,wx.EXPAND) 
        box.Add(accept,0,wx.EXPAND) 
        box.Add(self.text, 1,wx.EXPAND) 

        wx.EVT_LIST_ITEM_SELECTED(self.list,tID, self.selectProp)
        wx.EVT_BUTTON(accept, accept.GetId(), self.acceptProp)
        
    def selectProp(self,event):
        idx=self.list.GetFocusedItem()
        prop = self.list.GetItem(idx,0).GetText()
        val = self.list.GetItem(idx,1).GetText()
        self.text.Clear()
        self.text.WriteText(val)
        
    def acceptProp(self,event):
        idx=self.list.GetFocusedItem()
        prop = self.list.GetItem(idx,0).GetText()
        lines = self.text.GetNumberOfLines()
        if lines ==1:
            exec 'self.item.' + prop +'='+self.text.GetValue()
        else:
            p=setattr(self.item,prop,self.text.GetValue())
            print prop
            
        self.list.SetStringItem(idx, 1, str(getattr(self.item,prop)))



if __name__ =='__main__':
    app = wx.PySimpleApp(False)
    wx.InitAllImageHandlers()
    ogl.OGLInitialize()
    frame = FlowFrame(None, -1, "")
    app.SetTopWindow(frame)
    frame.Show(True)
    app.MainLoop()
