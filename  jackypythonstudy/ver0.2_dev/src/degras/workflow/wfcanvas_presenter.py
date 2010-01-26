# _*_ coding: utf-8 _*_
# Copyright (C)  2010 Biao Ma

# standard modules
import os,sys

class WorkFlowCanvasPresenter(object):

    def __init__(self, model=None, view=None):
        self.model = model
        self.view = view
        self.init()
    
    def init(self):
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
                    self.Refresh()
                    print shape,"is deleted by press del key"