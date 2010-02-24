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

        from method import MethodSetting
        # from potential.potential_agent import PotentialSetting

        if self.model:
            method_agent = MethodSetting(
                self.view.getContainer(), self.model.method)
        else:
            method_agent = MethodSetting(self.view.getContainer())

        # if potential:
            # potential_model = model.potential

        # potentail_aagent = PotentialSetting(potential_model)

        # print method_agent.getView()
        self.view.appendView( method_agent.getView(), 'Method')
        # self.appendView( potential_agent.getView() )


    def close(self):
        self.model.varidateInvariants()

