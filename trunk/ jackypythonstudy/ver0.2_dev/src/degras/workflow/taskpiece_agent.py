#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura
#
# $Date: 2010-01-28 15:12:24 +0900 (木, 28 1 2010) $
# $Rev: 0 $
# $Author: ma $
#
import os, sys


from taskpiece_view       import TaskPieceView
from taskpiece_presenter  import TaskPiecePresenter
from taskpiece_interactor import TaskPieceInteractor

class TaskPiece(object):

    def __init__(self, model, model_view=None):

        self.model = model
        self.model_view = model_view
        self.__view = TaskPieceView()
        self.__presenter = TaskPiecePresenter(model, self.view, model_view)
        interacter = TaskPieceInteractor(view, presenter)
        
    def get_view(self):
        return self.__view
    
    def __getattr__(self, attr):
        if attr.endswith('_event') and hasattr(self.__presenter):
            return getattr(self.__presenter, attr)



