#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura
#
# $Date: 2010-02-16 20:50:23 +0900 (火, 16 2 2010) $
# $Rev: 92 $
# $Author: ishikura $
#
import os, sys

from nose.tools import *

nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from utils.test_helper import *
sys.path.append('../')
from setting import OptimizeConverter



class TestAmberOptimize:

    def setUp(self):
        self.settings = dict(
            taskobject    = 'optimize' , 
            method        = 'sd+cg'    , 
            ncycle        = 100        , 
            ncycle_switch = 50         , 
        )
        pass

    def tearDown(self):
        pass

    def testInit(self):
        pass

    def test_ncyc(self):
        cvt = OptimizeConverter(dict(
            method = 'sd',
            ncycle = 100
        ))
        # assert_equal(cvt.getOptions(), 
        



