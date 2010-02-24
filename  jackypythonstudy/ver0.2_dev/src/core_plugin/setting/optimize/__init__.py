#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura
#
# $Date: 2010-02-22 21:35:39 +0900 (月, 22 2 2010) $
# $Rev: 105 $
# $Author: ishikura $
#


import optimize_agent
import optimize_model
import optimize_view
import method

agent_class_dict = {
    'optimize': optimize_agent.OptimizeSetting,
    'opt_method': method.MethodSetting
}

model_class_dict = {
    'optimize': optimize_model.OptimizeModel,
    'opt_method': method.MethodModel,
    # 'opt_potential': potential.PotentialSetting
}

view_class_dict = {
    'optimize': optimize_view.OptimizeView,
    'opt_method': method.MethodView,
}

