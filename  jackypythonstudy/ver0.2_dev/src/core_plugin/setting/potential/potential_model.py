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

# class IPotential(Interface):
#     protein_ff = Choice(
#         title=u'force field',
#         values=['Amber_ff96', 'Amber_ff99SB', 'Amber_ff99', 'Amber_ff03'],
#         default='Amber_ff99SB',
#     )
#     pass


