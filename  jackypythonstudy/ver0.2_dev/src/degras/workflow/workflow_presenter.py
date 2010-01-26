#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura
#
# $Date: 2010-01-26 15:36:28 +0900 (火, 26 1 2010) $
# $Rev: 69 $
# $Author: ma $
#
import os, sys


from datapiece_agent import DataPiece
from taskpiece_agent import TaskPiece

class WorkFlowPresenter(object):

    def __init__(self, model, view, interactor,view_model=None):

        self.model = model
        self.view  = view
        interactor.__init_()
    # operations
    def append_task(self):
        task = self.model.append_task(taskobject='Energy')
        tp = TaskPiece(task)
        self.__tasklist.append(tp)
        self.view.append_piece( tp.get_view() )

    def append_data(self):
        data = self.model.append_data(type='system', format='pdb')
        dp = DataPiece(task)
        self.__datalist.append(dp)
        self.view.append_data( dp.get_view() )

    def connect(self):
        pass

    def disconnect(self):
        pass

    def delete(self):
        pass

    def selected(self, view):
        selfcted

        pass

    def add_selected(self):
        pass

    def activate(self):
        pass

    def popup(self):
        pass

    def connect(self, taskpiece):
        pass

    # popup requests
    def delete(self):
        pass

    def delete_model(self):
        pass

    def change_size(self):
        pass

