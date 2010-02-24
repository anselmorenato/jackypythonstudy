#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura
#
# $Date: 2010-02-22 21:35:39 +0900 (月, 22 2 2010) $
# $Rev: 105 $
# $Author: ishikura $
#
import os, sys

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from utils.deco import nproperty
from core.model import *

class IOptimizeModel(Interface):

    optmethod = schema.Choice(
        title    = u"Optimize method",
        values   = ['sd', 'cg', 'sd+cg', 'nr'],
        default  = 'cg',
        required = True,)
    
    ncycle = schema.Int(
        title=u"The number of cycle for optimization",
        required = True,
        default = 1000,
        min=0, max=50000)

    ncycle_switch = schema.Int(
        title=u"Changing cycle number for sd + cg method.",
        required = True,
        default = 1000,
        min=0, max=50000)

    @invariant
    def validate_ncycle_switch(model):
        if model.optmethod=='sd+cg':
            if model.ncycle_switch >= model.ncycle:
                raise Invalid(model.ncycle, model.ncycle_switch)


class OptimizeModel(ModelBase):
    implements(IOptimizeModel)
    def __init__(self):
        ModelBase.__init__(self)



if __name__ == '__main__':
    m = OptimizeModel()
    print m.optmethod, m.ncycle, m.ncycle_switch
    m.optmethod = 'sd'
    m.ncycle = 500 
    m.ncycle_switch = 2000
    print m.optmethod, m.ncycle, m.ncycle_switch
    m.load( m.dump() )
    m.validateInvariants()
    m.optmethod = 'nr'
    # print m.optmethod, m.ncycle, m.ncycle_switch
