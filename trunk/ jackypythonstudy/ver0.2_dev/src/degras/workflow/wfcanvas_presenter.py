# _*_ coding: utf-8 _*_
# Copyright (C)  2010 Biao Ma
#
# $Date: 2010-01-26 15:36:28 +0900 (火, 26 1 2010) $
# $Rev: 69 $
# $Author: ma $
#
# standard modules
import os,sys


from datapiece_agent import DataPiece
from taskpiece_agent import TaskPiece

class WorkFlowCanvasPresenter(object):

    def __init__(self, model=None, view=None):
        self.model = model
        self.view = view
    # operations
    def append_task(self):
        task = self.model.appendTask(taskobject='Energy')
        tpiece = TaskPiece(task)
        self.__tasklist.append(tpiece)
        self.view.appendTask( tpiece.get_view() )

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
                    
