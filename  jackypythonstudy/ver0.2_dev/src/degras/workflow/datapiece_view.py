#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura
#
# $Date:  $
# $Rev:  $
# $Author: ma $
#

import os, sys
import wx
import wx.lib.ogl as ogl


class DataPieceView(ogl.CompositeShape):

    def __init__(self,canvas,name='New Data',x=40,y=30):
        ogl.CompositeShape.__init__(self)
        self.SetCanvas(canvas)        
        region = wx.Region()

        self.shape1 = ogl.RectangleShape(100, 60)
        self.shape1.AddText(name)

        self.shape2 = Connector(canvas, self)
        self.shape2.SetBrush(wx.GREEN_BRUSH)
        self.shape2.SetY(-35)
        
        self.AddChild(self.shape1)
        self.AddChild(self.shape2)

        constraint = ogl.Constraint(ogl.CONSTRAINT_RIGHT_OF ,self.shape1, [self.shape2])
        self.AddConstraint(constraint)
        self.Recompute()
        
        self.shape1.SetSensitivityFilter(0)
        self.shape2.SetSensitivityFilter(5)

        self.__name   = 'Data'
        self.__type   = 'Type'
        self.__format = 'format'

        self.__selected = False

    def is_selected(self):
        return self.__selected

    def set_selected(self, select):
        self.__selected = select
        
    def set_label(self,name):
        self.shape1.AddText(name)
        
    # property: name
    def get_name(self):
        return self.__name
    def set_name(self, name):
        self.__name = name
    name = property(get_name, set_name)

    # property: type
    def get_type(self):
        return self.__type
    def set_type(self, type):
        self.__type = type
    type = property(get_type, set_type)
    
    # property: format
    def get_format(self):
        return self.__format
    def set_format(self, format):
        self.__format = format
    format = property(get_format, set_format)
    
class Connector(ogl.CircleShape):
    
    def __init__(self, canvas, data_shape, size = 10):
        ogl.CircleShape.__init__(self, size)
        self.SetCanvas(canvas)
        self.SetDraggable(False)
        self.data_shape = data_shape
    
    def OnEndDragLeft(self, x, y, keys=0, attachment=0):
        sx,sy = self.GetCanvas().CalcUnscrolledPosition(x, y)
        _shape,attachment = self.GetCanvas().FindShape(x,y)
        print 'shape is ',_shape,'the type is',type(_shape)
        ogl.ShapeEvtHandler.OnEndDragLeft(self, x, y, keys, attachment)

        try:
            if isinstance(_shape,InputSocketShape):
            
                print 'now task is start'
                print self.data_shape
                fromShape = self.data_shape
                
                toShape = _shape
                self.GetCanvas().add_linker(fromShape,toShape)
        except NameError:
            pass
    
