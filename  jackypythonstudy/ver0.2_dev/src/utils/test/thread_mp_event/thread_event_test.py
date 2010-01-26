#! /opt/python2.6/bin/python
#  -*- encoding: utf-8 -*-

import os, sys

nagara_path = os.environ['NAGARA_PATH'] 
sys.path.append( os.path.join(nagara_path, 'src') )

from event import NagaraEvent
from threading import Thread


event1 = NagaraEvent()
def hoge(msg):
    print 'hoge', msg
def listener1(msg, extra=None):
    print 'Function listener1 received', msg

event1.bind(hoge)

def count(n, a):
    while n > 0:
        n -= 1
        print a
        event1.fire(n)

# count(100000)

t1 = Thread(target=count,args=(100000,'1desuyo'))
t1.start()
t2 = Thread(target=count,args=(100000,'2desuyo'))
t2.start()
t1.join()
t2.join()
