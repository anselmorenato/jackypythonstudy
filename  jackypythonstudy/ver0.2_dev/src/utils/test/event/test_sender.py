#! /opt/python2.6/bin/python
#  -*- encoding: utf-8 -*-
import os, sys
# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from utils.event import NagaraEvent

class C(object):
    def __init__(self):
        self.__event_1 = NagaraEvent()

    @property
    def event_1(self):
        return self.__event_1


