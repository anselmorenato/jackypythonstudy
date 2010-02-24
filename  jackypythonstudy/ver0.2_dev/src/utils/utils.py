#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura
#
# $Date: 2010-02-22 21:15:53 +0900 (月, 22 2 2010) $
# $Rev: 100 $
# $Author: ishikura $
#
# standard modules
import os, sys

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from core.exception import NagaraException


def include(self, cls, *args, **kwds):
    if cls not in self.__class__.__bases__:
        self.__class__.__bases__ += (cls,)
        if hasattr(cls, '__init__'):
            cls.__init__(self, *args, **kwds)


import itertools
import threading
from functools import wraps
from decorator import decorator

class NotFoundPropertyError(NagaraException): pass
def nproperty(func):
    """Decorator to easy use property.

    Usage:

    class A(object):
        def __init__(self):
            self.__x = None

        @nproperty
        def x():

            test_val_list = [] # use in get and set

            def get(self):
                print('Get property x.')
                return self.__x

            def set(self, x):
                print('Set property x: ', x, '.')
                self.__x = x

            def del_(self, x):
                del self.__x

            return locals()

    a = A()
    a.x = 5
    print a.x
    => 5
    getattr(a, 'x') => 5
    setattr(a, 'x', 9)
    print a.x
    => 9

    """
    attr_dict = func()
    prop_dict = {}
    for name, method in attr_dict.items():
        if name.startswith('get'):
            prop_dict['fget'] = method
            get_method = method
        elif name.startswith('set'):
            prop_dict['fset'] = method
        elif name.startswith('del'):
            prop_dict['fdel'] = method
        elif name.startswith('doc'):
            prop_dict['doc']  = method
        else:
            pass

    # check exception
    if not prop_dict:
        message = "Cound't found property attribute: {0}.".format(func.__name__)
        raise NotFoundPropertyError(message)

    return property(**prop_dict)


@decorator
def trace(f, *args, **kw):
    print "calling %s with args %s, %s" % (f.func_name, args, kw)
    return f(*args, **kw)


@decorator
def logging(fun, *args, **kwds):
    cn = self.__class__.__name__
    fn = fun.func_name
    mes = 'Recieved on {0} at {1}\n'.format(fn, cn)
    # self.log.write( mes )
    return fun(*args, **kwds)


# @sync(lock)
def synchronized(lock):
    def call(fun, *args, **kwds):
        with lock:
            result = fun(*args, **kwds)
        return result
    return decorator(call)


def on_success(result): # default implementation
    "Called on the result of the function"
    return result


def on_failure(exc_info): # default implementation
    "Called if the function fails"
    pass


def on_closing(): # default implementation
    "Called at the end, both in case of success and failure"
    pass


class Async(object):
    """
    A decorator converting blocking functions into asynchronous
    functions, by using threads or processes. Examples:

    async_with_threads =  Async(threading.Thread)
    async_with_processes =  Async(multiprocessing.Process)
    """

    def __init__(self, threadfactory):
        self.threadfactory = threadfactory

    def __call__(self, func, on_success=on_success,
                 on_failure=on_failure, on_closing=on_closing):
        # every decorated function has its own independent thread counter
        func.counter = itertools.count(1)
        func.on_success = on_success
        func.on_failure = on_failure
        func.on_closing = on_closing
        return decorator(self.call, func)

    def call(self, func, *args, **kw):
        def func_wrapper():
            try:
                result = func(*args, **kw)
            except:
                func.on_failure(sys.exc_info())
            else:
                return func.on_success(result)
            finally:
                func.on_closing()
        name = '%s-%s' % (func.__name__, func.counter.next())
        thread = self.threadfactory(None, func_wrapper, name)
        thread.start()
        return thread
threaded = Async(threading.Thread)
import multiprocessing
processed = Async(multiprocessing.Process)


def redirecting_stdout(new_stdout):
    def call(func, *args, **kw):
        save_stdout = sys.stdout
        sys.stdout = new_stdout
        try:
            result = func(*args, **kw)
        finally:
            sys.stdout = save_stdout
        return result
    return decorator(call)


def main_thread():
    lock = threading.RLock()

    n = 0


    # @race
    @threaded
    # @synchronized(lock)
    def aaa(hoge):
        global n
        n += 1
        return n


    import time
    class Worker(object):
        @threaded
        def run(self):
            i = 0
            while self.flag: 
                print i
                time.sleep(0.1)
                i += 1

    w1 = Worker()

    w1.run()
    time.sleep(2)
    w1.flag = False


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


def main_pattern():

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


def main_property():

    class A(object):

        @nproperty
        def x():

            def getX(self):
                print 'Get X property', self

            def setX(self, value):
                print 'Set X property', value, self

            return locals()

        # @nnproperty
        # def f(self):

        #     def getF(self):
        #         print 'Get F property', self

        #     def setF(self, value):
        #         print 'Set F property', value, self

        #     return locals()

        # def sety(self, y):
        #     self.__y = y
        pass

    # a = A()
    # print a.__class__.__dict__
    # a.x = 'Hello'
    # print a.f
    # print a.sety
    # print a.f



if __name__ == '__main__':
    # main_thread()
    main_property()
    main_pattern()


