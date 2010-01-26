#  -*- encoding: utf-8 -*-
import os, sys
from decorator import decorator

class Singleton(object):
    def __new__(cls, *args, **kwds):
        tmp_instance = None

        if not hasattr(cls, "_instance_dict"):
            cls._instance_dict = {}
            cls._instance_dict[hash(cls)] = super(
                Singleton, cls).__new__(cls, *args, **kwds)
            tmp_instance = cls._instance_dict[hash(cls)]

        elif not cls._instance_dict.get( hash(cls) ):
            cls._instance_dict[hash(cls)] = super(
                Singleton, cls).__new__(cls, *args, **kwds)
            tmp_instance = cls._instance_dict[hash(cls)]

        else:
            tmp_instance = cls._instance_dict[hash(cls)]

        return tmp_instance


class Null(object):

    def __new__(cls, *args, **kwds):
        if '_inst' not in vars(cls):
            cls._inst = super(Null, cls).__new__(cls, *args, **kwds)
        return cls._inst

    def __init__(self, *args, **kwds): pass
    def __call__(self, *args, **kwds): return self
    def __repr__(self): return 'Null()'
    def __nonzero__(self): return False
    def __getattr__(self, name): return self
    def __setattr__(self, name, value): return self
    def __delattr__(self, name): return self


@decorator
def default_request(fun, *args, **kwds):
    fun.default_req = 1
    return fun(*args, **kwds)

class State(object):
    def __init__(self):
        pass

    def get_available_request(self):
        """Return available request in this state."""
        for request in self.__dict__:
            if not request.__dict__.get('default_req'):
                yield request.__name__, True
            else:
                yield request.__name__, False

if __name__ == '__main__':
    s1 = Singleton()
    print s1
    s2 = Singleton()
    print s2
    print 80*'-'

    print 'test task object'

    from abc import *
    class TaskObject(Singleton):
        pass
    class Energy(TaskObject): pass
    class Optimize(TaskObject): pass

    t = TaskObject()
    print t

    e1 = Energy()
    e2 = Energy()
    print e1
    print e2

    o1 = Optimize()
    o2 = Optimize()
    print o1
    print o2

    # print 80*'-'
    # s11 = sbase()
    # print s11
    # s12 = sbase()
    # print s12
