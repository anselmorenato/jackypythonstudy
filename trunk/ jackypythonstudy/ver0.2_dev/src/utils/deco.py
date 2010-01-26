#  -*- encoding: utf-8 -*-
import os, sys
from decorator import decorator
import itertools
import threading


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


if __name__ == '__main__':
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
