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

from method import IMethodModel, MethodModel
# from potential.potential_model import IPotentialModel

class IOptimizeModel(Interface):

    method = schema.Object(
        title    = u"Optimize method" , 
        schema   = IMethodModel       , 
        readonly = True               , 
        required = True)

    # potential = schema.Object(
        # title = u"Potential",
        # schema = IPotentialModel,
        # required = True)


class OptimizeModel(ModelBase):
    implements(IOptimizeModel)
    def __init__(self):
        self.method = MethodModel()
        ModelBase.__init__(self)


if __name__ == '__main__':
    o = OptimizeModel()
    print o.method.optmethod
    print o.dump()
    m = o.method
    print m.optmethod, m.ncycle, m.ncycle_switch
    # m.optmethod = 'sd'
    # m.ncycle = 500 
    # m.ncycle_switch = 2000
    # print m.optmethod, m.ncycle, m.ncycle_switch
    # m.load( m.dump() )
    # m.validateInvariants()
    # m.optmethod = 'nr'
    # # print m.optmethod, m.ncycle, m.ncycle_switch
