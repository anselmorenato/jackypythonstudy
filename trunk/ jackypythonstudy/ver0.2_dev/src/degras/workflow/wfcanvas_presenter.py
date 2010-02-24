# _*_ coding: utf-8 _*_
# Copyright (C)  2010 Biao Ma
#
# $Date: 2010-01-26 15:36:28 +0900 (火, 26 1 2010) $
# $Rev: 69 $
# $Author: ma $
#
# standard modules
import os,sys
import wx
import wx.lib.ogl as ogl

import datapiece_view

class WorkFlowCanvasPresenter(object):

    def __init__(self, model=None, view=None):
        self.model = model
        self.view = view
    # operations
    def append_task(self):
        task = self.model.appendTask(taskobject='Energy')
        tpiece = TaskPiece(task)
        self.__tasklist.append(tpiece)
        self.view.appendPiece( tpiece.get_view() )

    def append_data(self):
        data = self.model.appendData(type='system', format='pdb')
        dpiece = DataPiece(data)
        self.__datalist.append(dpiece)
        self.view.appendData( dpiece.get_view() )

    def connect(self):
        pass
    def popup(self,event):
        """ create the popup menu."""
        # get the information from event
        x,y = event.GetPosition()
        sx, sy = self.view.CalcUnscrolledPosition(x, y)
        shape, attachment = self.view.FindShape(sx, sy)
        # right click at shape
        if shape:
            # creat the popupmenu when right click on shape
            popmenu = self.view.make_popmenu()
        # right click at canvas (not at shape)
        else:
            # creat the popupmenu when right click on canvas
            popmenu2 = self.view.make_popmenu_2()
        event.Skip(True)
    def add_shape(self, shape, x, y,pen=wx.BLACK_PEN, brush=wx.WHITE_BRUSH):
        """ creat the shape on canvas, and add the new shape in shapes list.
        """
        # Composites have to be moved for all children to get in place
        if isinstance(shape, ogl.CompositeShape):
            dc = wx.ClientDC(self.view)
            self.view.PrepareDC(dc)
            shape.Move(dc, x, y)
        else:
            shape.SetDraggable(True, True)
        
        #shape.AddText(shape.taskobject_name)
        shape.SetCanvas(self.view)
        shape.SetX(x)
        shape.SetY(y)
        if pen:    shape.SetPen(pen)
        if brush:  shape.SetBrush(brush)
        
        #shape.SetShadowMode(ogl.SHADOW_RIGHT)
        self.view.diagram.AddShape(shape)
        shape.Show(True)
        
        self.evthandler = EvtHandler(canvas= self.view)
        self.evthandler.SetShape(shape)
        self.evthandler.SetPreviousHandler(shape.GetEventHandler())
        shape.SetEventHandler(self.evthandler)
        self.view.shapes.append(shape)
        
        return shape

            
    def delete(self):
        for shape in self.view.shapes:
            if shape.Selected():
                shape.Delete()
                self.Refresh()
        print ' the selected shape is deleted.'
    
    def key_press(self,event):
        key = event.GetKeyCode()
        if key ==127:  # DELETE 
            for shape in self.view.shapes:
                if shape.Selected():
                    shape.Delete()
                    self.view.Refresh()
                    print shape,"is deleted by press del key"
                    
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
        #self.canvas.Unbind(wx.EVT_MOTION)
        shape = self.GetShape()
        sx,sy = self.canvas.CalcUnscrolledPosition(x, y)
        _shape,attachment = self.canvas.FindShape(x,y)        
        print 'drag begin at',x,y
        ogl.ShapeEvtHandler.OnBeginDragLeft(self, x, y, keys = 0, attachment = 0)
        if isinstance(_shape,wx.lib.ogl._basic.CircleShape):
            #x=old_x 
            #y=old_y
            print _shape
            #shape.SetDraggable(False)
                      
    
        
    def OnEndDragLeft(self, x, y, keys=0, attachment=0):
        
        shape = self.GetShape()  # This is the souce shape of dragged.  
        sx,sy = self.canvas.CalcUnscrolledPosition(x, y)
        _shape,attachment = self.canvas.FindShape(x,y)  # _shape is the shape at drop position. 
        print 'shape is ',_shape,'the type is',type(_shape)
        ogl.ShapeEvtHandler.OnEndDragLeft(self, x, y, keys, attachment)
        try:
            _shape_p = _shape.GetParent()
        except:
            _shape_p =_shape
        try:
            if isinstance(_shape,InputSocketShape)& isinstance(shape,DataShape):
                print 'now task is start'
                print shape
                fromShape = shape
                toShape = _shape
                self.canvas.add_linker(fromShape,toShape)
                shape.SetDraggable(True)
            self.up_data_statusbar(shape)
        except NameError:
            pass
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
        
        shape = self.GetShape()
        #canvas = shape.Getcanvas()
        self.canvas.diagram.RemoveShape(shape)
        self.canvas.Refresh()
        
        print shape ,'is deleted'
                    