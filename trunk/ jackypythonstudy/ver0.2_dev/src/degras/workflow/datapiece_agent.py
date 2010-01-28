#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura
#
# $Date: 2010-01-28 15:12:24 +0900 (木, 28 1 2010) $
# $Rev: 72 $
# $Author: ma $
#
import os, sys


from datapiece_view       import DataPieceView
from datapiece_presenter  import DataPiecePresenter
from datapiece_interactor import DataPieceInteractor

class DataPiece(object):

    def __init__(self, model, model_view=None):

        self.model = model
        self.model_view = model_view
        self.__view = DataPieceView()
        self.__presenter = DataPiecePresenter(model, self.view, model_view)
        interacter = DataPieceInteractor(view, presenter)
        
    def get_view(self):
        return self.__view
    
    def __getattr__(self, attr):
        if attr.endswith('_event') and hasattr(self.__presenter):
            return getattr(self.__presenter, attr)



