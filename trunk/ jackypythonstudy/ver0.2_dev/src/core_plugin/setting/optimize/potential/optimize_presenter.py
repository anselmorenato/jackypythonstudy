#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura
#
# $Date: 2010-02-22 21:35:39 +0900 (月, 22 2 2010) $
# $Rev: 105 $
# $Author: ishikura $
#
import os, sys

class OptimizePresenter(object):

    def __init__(self, view, model=None):
        self.view  = view
        self.model = model
        self.updateView()

    def selectMethod(self):
         if self.view.optmethod == 'sd+cg':
             self.view.enable('ID_ncycle_switch_text' , True)
             self.view.enable('ID_ncycle_switch'      , True)
         else:
             self.view.enable('ID_ncycle_switch_text' , False)
             self.view.enable('ID_ncycle_switch'      , False)

    def updateModel(self, attrname):
        value = getattr(self.view, attrname)
        setattr(self.model, attrname, value)
        print 'attrname, value', attrname, getattr(self.model, attrname)

    def updateView(self):
        self.view.optmethod     = self.model.optmethod
        self.view.ncycle        = self.model.ncycle
        self.view.ncycle_switch = self.model.ncycle_switch
        self.selectMethod()

    def close(self):
        self.model.varidateInvariants()

