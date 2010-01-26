#! /opt/python2.6/bin/python
#  -*- encoding: utf-8 -*-
import os, sys
# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from utils.event import EventBindManager

class B(object):

    binder = EventBindManager()

    def __init__(self, mmm):
        self.__mmm = mmm
        self.binder.bind_all(self)

    @binder('__mmm.event_1')
    def handler1(self, msg):
        print 5555, msg

if __name__ == '__main__':
    import test_sender
    c = test_sender.C()
    b = B(c)
    c.event_1.fire()

