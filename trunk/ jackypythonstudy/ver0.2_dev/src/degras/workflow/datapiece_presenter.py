#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura
#
# $Date: 2010-01-26 15:36:28 +0900 (火, 26 1 2010) $
# $Rev: 69 $
# $Author: ma $
#
import os, sys


class DataPiecePresenter(object):

    def __init__(self, model, view, view_model=None):

        self.model = model
        self.view = view

        self.connect_finish_event = NagaraEvent()

    def drag(self):
        pass

    def drop(self):
        pass

    def move(self, x, y, *args, **kwds):
        self.view.move(x, y)

    def selected(self):
        pass

    def connect_start(self):
        pass

    def connect_finish(self, x, y, *args, **kwds):
        self.connect_finish_event.fire(x, y)

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


    



