# shapedrop.py

import wx
import wx.lib.ogl as ogl

import cPickle

class TaskShape(ogl.DrawnShape):
    def __init__(self, w=100, h=50, name= ''):
        ogl.RectangleShape.__init__(self, w, h)
        self.taskobject_name = name
        ogl.DrawnShape.__init__(self)
        #self.SetCanvas(canvas)
        
        self.SetDrawnPen(wx.Pen("#ff8030"))
        self.DrawLines([(25,-40),(30,-50),(30, -30),(30, -50),(35,-40)])
        
        self.CalculateSize()
        
        
class DrawnShape(ogl.DrawnShape):
    def __init__(self):
        ogl.DrawnShape.__init__(self)
                       
        self.SetDrawnPen(wx.Pen("#ff8030"))
        shape2 = self.DrawLines([(25,-40),(30,-50),(30, -30),(30, -50),(35,-40)])
        
        self.CalculateSize()
class TestShape(ogl.CompositeShape):
    def __init__(self, canvas):
        ogl.CompositeShape.__init__(self)

        self.SetCanvas(canvas)        
        
        shape1 = ogl.RectangleShape(100, 60)
        self.AddChild(shape1)
        shape2 = ogl.CircleShape(20)
        shape2.SetBrush(wx.GREEN_BRUSH)
        shape2.SetY(-35)
        #shape2.Select(select)
        self.AddChild(shape2)
        shape2.SetDraggable(0)
        constraint = ogl.Constraint(ogl.CONSTRAINT_RIGHT_OF ,shape1, [shape2])
        self.AddConstraint(constraint)
        self.Recompute()
        shape1.SetSensitivityFilter(0)
        
        #shape2.Bind(EvtHander)
        #EVT_(self, ID_ABOUT, self.OnAbout)
        #wx.EVT_KEY_DOWN(canvas.evthandler,self.on_delete_shape)
    def on_delete_shape(self,event):
        print "the delete key is pressed."
class WorkFlowCanvas(ogl.ShapeCanvas):
    def __init__(self, parent,frame):
        ogl.ShapeCanvas.__init__(self, parent)

        maxWidth  = 500
        maxHeight = 500
        self.SetScrollbars(20, 20, maxWidth/20, maxHeight/20)

        self.frame = frame
        #self.SetBackgroundColour("LIGHT BLUE") #wx.WHITE)
        self.diagram = ogl.Diagram()
        self.SetDiagram(self.diagram)
        self.diagram.SetCanvas(self)
        self.shapes = []
        
        rRectBrush = wx.Brush("GREEN", wx.SOLID)
        
        
        self.add_shape(
            TaskShape(100, 80,'Task1'), 
            200, 158, wx.Pen(wx.BLUE, 2), rRectBrush, "Task Shape1"
        )
        self.add_shape(
            TestShape(self),200,300,wx.BLACK_PEN,rRectBrush,'')
        
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
        #if text:
         #   for line in text.split('\n'):
          #      shape.AddText(line)
        #shape.AddText(shape.taskobject_name)
        #shape.SetShadowMode(ogl.SHADOW_RIGHT)
        self.diagram.AddShape(shape)
        shape.Show(True)
        
        self.evthandler = EvtHander( self.frame)
        self.evthandler.SetShape(shape)
        self.evthandler.SetPreviousHandler(shape.GetEventHandler())
        shape.SetEventHandler(self.evthandler)

        self.shapes.append(shape)
        return shape
    
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
        
        self.evthandler = EvtHander( self.frame)
        self.evthandler.SetShape(shape)
        #evthandler.SetPreviousHandler(shape.GetEventHandler())
        shape.SetEventHandler(self.evthandler)
        
        self.shapes.append(shape)
        return shape
    
class EvtHander(ogl.ShapeEvtHandler):
    def __init__(self, frame):
        ogl.ShapeEvtHandler.__init__(self)
        #self.log = log
        self.statbarFrame = frame
        self.shape = self.GetShape
        

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

        print shape
        #if shape ==TaskShape:
        print shape.GetChildren()


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
    def OnEndDragLeft(self, x, y, keys=0, attachment=0):
        shape = self.GetShape()
        ogl.ShapeEvtHandler.OnEndDragLeft(self, x, y, keys, attachment)

        if not shape.Selected():
            self.OnLeftClick(x, y, keys, attachment)
        
        self.up_data_statusbar(shape)

        # add the evt process begin here 

        message = str(('The shape',str(shape),'has End the  draged /n Please add the evt process in Method OnEndDragLeft'))
        dlg = wx.MessageDialog(None,message,'test',style = wx.OK|wx.ICON_INFORMATION)
    # dlg.ShowModal()
        #dlg.Destroy()
        #print message
        #print type(message)
        #self.statbarFrame.on_drag_start(self)
        

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
        shape = self.GetShape()
        #if shape == TaskShape(shape.GetCanvas()):
        print shape
    def on_end_dragright(self,x,y,keys = 0, attachment =0):
        pass
    
class TaskShapeDropTarget(wx.PyDropTarget):
    
    def __init__(self, canvas):
        wx.PyDropTarget.__init__(self)
        #self.log = log
        self.canvas = canvas
        self.data = wx.TextDataObject()
        self.SetDataObject(self.data)
        
    def On_DropText(self, x, y, data):
        try:
            self.canvas.InsertStringItem(-1,'drag end')
            #self.canvas.add_shape(TaskShape(100,50,380,158), wx.BLACK_PEN, wx.WHITE_BRUSH, '')
        except:
            print 'error'
        
        # some virtual methods that track the progress of the drag
    def OnEnter(self,x,y,data):
        print 'drag start'


    def OnLeave(self):
        pass

    def OnDrop(self, x, y):
        
        self.canvas.Refresh()
    def OnDragOver(self, x, y, d):
        #self.log.WriteText("OnDragOver: %d, %d, %d\n" % (x, y, d))

        # The value returned here tells the source what kind of visual
        # feedback to give.  For example, if wxDragCopy is returned then
        # only the copy cursor will be shown, even if the source allows
        # moves.  You can use the passed in (x,y) to determine what kind
        # of feedback to give.  In this case we return the suggested value
        # which is based on whether the Ctrl key is pressed.
        return d



    # Called when OnDrop returns True.  We need to get the data and
    # do something with it.
    def OnData(self, x, y, d):
        

        # copy the data from the drag source to our data object
        if self.GetData():
            # convert it back to a list of lines and give it to the viewer
            self.text = self.data.GetText()
            
        self.canvas.add_shape(TaskShape(100,50,self.text),x,y, wx.BLACK_PEN, wx.WHITE_BRUSH, '')
            
        # what is returned signals the source what to do
        # with the original data (move, copy, etc.)  In this
        # case we just return the suggested value given to us.
        return d  
        


class FlowFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        wx.Frame.__init__(self, *args, **kwds)
        #panel = wx.Panel(self)
        tasklist = ["Task1","Task2","Task3","Task4"]
        self.StatusBar = wx.StatusBar(self)
        self.toolbar = self.make_toolbar()
        splitter1 = wx.SplitterWindow(self, -1, style=wx.SP_3D)
        splitter2 = wx.SplitterWindow(splitter1, -1, style=wx.SP_3D)
        #log = open('log.log')

        self.SetTitle("OGL TEST")
        self.SetSize((800,600))
        self.SetBackgroundColour(wx.NamedColour('white'))
        
        self.work_canvas = WorkFlowCanvas(splitter1,self)
        #self.temp_canvas = TempCanvas(splitter2,self)
        
        self.temp_canvas = wx.ListCtrl(splitter2, -1, style=wx.LC_LIST)
        print len(tasklist)
        for i in range(len(tasklist)):        
            #self.temp_canvas.InsertStringItem(0,i)
            self.temp_canvas.InsertStringItem(i,tasklist[i])
            print i
        splitter1.SplitVertically(self.work_canvas, splitter2)
        splitter2.Initialize(self.temp_canvas)
        self.Center()
        
        # create the droptaaget
        self.shapetaget = TaskShapeDropTarget(self.work_canvas)
        self.work_canvas.SetDropTarget(self.shapetaget)
        
        self.temp_canvas.Bind(wx.EVT_LIST_BEGIN_DRAG, self.on_drag_start)
        
        #self.work_canvas.evthandler.GetShape().Bind(wx.EVT_KEY_DOWN,self.on_delete_shape)
        #wx.EVT_KEY_DOWN(wx.WXK_DELETE,self.on_delete_shape)
        
    def on_delete_shape(self,event):
        print "the delete key is pressed."
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
        #self.Bind(wx.EVT_TOOL, self.OnToolClick, id=10)
        #self.Bind(wx.EVT_TOOL_RCLICKED, self.OnToolRClick, id=10)

        #tb.AddSimpleTool(20, open_bmp, "Open", "Long help for 'Open'")
        toolbar.AddLabelTool(20, "Open", open_bmp, shortHelp="Open", longHelp="Long help for 'Open'")
        #self.Bind(wx.EVT_TOOL, self.OnToolClick, id=20)
        #self.Bind(wx.EVT_TOOL_RCLICKED, self.OnToolRClick, id=20)

        
        # Final thing to do for a toolbar is call the Realize() method. This
        # causes it to render (more or less, that is).
        toolbar.Realize()
    def on_drag_start(self,event):
        try:
            # create our own data format and use it in a custom data object
            self.data = wx.TextDataObject(self.temp_canvas.GetItemText(event.GetIndex()))
            print self.data
            # pickle the shape list
            #shape_pickle = cPickle.dumps(FlowCanvas)
            #except:
                #cPickle.PicklingError()
            #self.data.SetData(self.canvas.shapes)
            #self.data.SetData(self.data)
            #print shape_pickle
            #print self.data
            #creat the data source
            dropsource = wx.DropSource(self)
            dropsource.SetData(self.data)
            #dropsource.DoDragDrop(wx.Drag_CopyOnly)
            dropsource.DoDragDrop(True)
        except:
            print 'here has error'
app = wx.PySimpleApp(False)
wx.InitAllImageHandlers()
ogl.OGLInitialize()
frame = FlowFrame(None, -1, "")
app.SetTopWindow(frame)
frame.Show(True)
app.MainLoop()