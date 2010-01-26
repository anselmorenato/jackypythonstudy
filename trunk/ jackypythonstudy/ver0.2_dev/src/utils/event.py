#  -*- encoding: utf-8 -*-

# standard modules
import os, sys
import functools

# pypi modules
from decorator import decorator
from pubsub    import pub

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )

from core.exception import NagaraException
from core.log  import Log

# Nagara Exception

class BindEventException(NagaraException): pass

def decorator_factory(deco_arg): # partial is functools.partial
    "decorator_factory(deco_arg) returns a one-parameter family of decorators"
    return partial(lambda df, param: decorator(partial(df, param)), deco_arg)

id = 0
class NagaraEvent(object):

    def __init__(self, data=None):
        global id
        id += 1
        self.__id = str(id)
        self.__data = data

    @property
    def id(self):
        return int(self.__id)

    def bind(self, handler):
        pub.subscribe(handler, self.__id)

    def fire(self, data=None):
        pub.sendMessage(self.__id, msg=data)

# def handler(nagara_event):
#     """Decorator to bind NagaraEvent and handler.
#     Example:
#         # in any class
#         @handler(event)
#         def handler_method(self):
#             ...
#     """
#     def wrapper(fun, *args, **kwds):
#         return fun(*args, **kwds)
#     try:
#         nagara_event.bind(fun)
#     except AttributeError: 
#         if issubclass(event_src.__class__, wx.EvtHandler):
#             raise 'cannot bind between event and handler'
#         else:
#             raise UnknownError()
#     return decorator(wrapper)


class ImmutableDict(dict):
    '''A hashable dict.'''

    def __init__(self,*args,**kwds):
        dict.__init__(self,*args,**kwds)
    def __setitem__(self,key,value):
        raise NotImplementedError, "dict is immutable"
    def __delitem__(self,key):
        raise NotImplementedError, "dict is immutable"
    def clear(self):
        raise NotImplementedError, "dict is immutable"
    def setdefault(self,k,default=None):
        raise NotImplementedError, "dict is immutable"
    def popitem(self):
        raise NotImplementedError, "dict is immutable"
    def update(self,other):
        raise NotImplementedError, "dict is immutable"
    def __hash__(self):
        return hash(tuple(self.iteritems()))


class EventBindManager:
    binds = {}
    def __init__(self, use_log=True):
        self.binds[hash(self)] = set()
        self.__eventinfo_list = []
        self.__use_log = use_log

    def __call__(self, *dargs, **dkwds):
        def deco(func):
            # store func and event
            self.binds[hash(self)].add(
                ( func.func_name, dargs, ImmutableDict(dkwds) )
            )
  #           if self.__use_log:
  #               for arg in args:
  #                   self.__log_info(func.func_name, arg)

            return func

        # Log('hoge')
        return deco

    #def __call__(self, *dargs, **dkwds):
        #def deco(func):
            ## store func and event
            #@functools.wraps(func)
            #def wrapper(*args, **kwds):
                ##if self.__use_log:
                ##    self.__log_receive(func.func_name)
                #f = func(*args, **kwds)
                #return f

            #self.binds[hash(self)].add(
                #( func.func_name, dargs, ImmutableDict(dkwds) )
            #)
  
            #return wrapper

        ## Log('hoge')
        #return deco

#     def __log_info(self, funcname, event_arg):
#         chain_list = arg.split('.')
# 
#         if len(chain_list) == 1:
#             obj, event = chain_list[-2], chain_list[-1]
#             mes = 'Received {0} of {1} at {2}'
#             Log( mes.format(event, obj, func.func_name) )
#         elif len(chain_list[-2] == 'self':
#             obj, event = chain_list[-2], chain_list[-1]
#             mes = 'Received {0} of {1} at {2}'
#             Log( mes.format(event, obj, func.func_name) )
#          else:
#             obj, event = chain_list[-2], chain_list[-1]
#             mes = 'Received {0} of {1} at {2}'
#             Log( mes.format(event, obj, func.func_name) )

    def __log_receive(self, listener_name):
        info_list = self.get_info(listener_name)
        for info in info_list:
            obj = info['object_name']
            evt = info['event_name']
            cls = info['class_name']
            mes = 'Recieved {0} of {1}:{2} at {3}'
            Log( mes.format(evt, obj, cls, listener_name) )

    def log(self):
        for func_name, args, keys in self.binds[hash(self)]:
            print func_name, args

    def bind_all(self, obj):
        top_obj_name = obj.__class__.__name__
        for func_name, args, keys in self.binds[hash(self)]:
            old_func_name = func_name
            if func_name.startswith('__'):
                func_name = '_{0}{1}'.format(top_obj_name, func_name)

            for arg in args:

                chain_list = arg.split('.')
                if chain_list[0] == 'self':
                    chain_list = chain_list[1:]

                pre_obj = None
                cur_obj = obj
                try:
                    for m in chain_list:
                        pre_obj = cur_obj
                        if m.startswith('__'):
                            m = '_{0}{1}'.format(top_obj_name, m)

                        cur_obj = getattr(pre_obj, m)
                except AttributeError as e:
                    mes = "'{0}' object has no attribute '{1}'".format(
                        cur_obj.__class__.__name__, m
                    )
                    raise BindEventException(mes)

                if not isinstance(cur_obj, NagaraEvent):
                    mes = "{0}:'{1}' object is not NagaraEvent.".format(
                        chain_list[-1], cur_obj.__class__.__name__
                    )
                    raise BindEventException(mes)

                # store event
                event_name = m

                cls_name = pre_obj.__class__.__name__
                if len(chain_list) >= 2:
                    obj_name = chain_list[-2]
                else:
                    obj_name = 'self'

                self.__eventinfo_list.append( dict(
                    handler_name = old_func_name,
                    class_name   = cls_name,
                    object_name  = obj_name,
                    event_name   = event_name
                ))

                # bind event
                cur_obj.bind( getattr(obj, func_name) )

    def get_eventinfo_list(self):
        return self.__eventinfo_list

    def get_info(self, handler):
        evt_info = []
        for info in self.__eventinfo_list:
            if info['handler_name'] == handler:
                evt_info.append( dict(
                    class_name = info['class_name'],
                    object_name = info['object_name'],
                    event_name = info['event_name'],
                ))
        return evt_info


if __name__ == '__main__':
    def listener1(msg, extra=None):
        print 'Function listener1 received', msg

    class A(object):

        binder = EventBindManager()

        def __init__(self):
            self.event1 = NagaraEvent()
            self.event2 = NagaraEvent()

            self.binder.log()
            self.binder.bind_all(self)
            print self.binder.get_info('handler1')
            for a in self.binder.get_eventinfo_list():
                print a

        @binder('event1', 'event2')
        def handler1(self, msg):
            print 5555, msg
#
#        @binder('event2')
#        def handler2(self, msg):
#            print 4444, msg
#
        def fire1(self):
            self.event1.fire()

        def fire2(self):
            self.event2.fire()


    class B(object):

        binder = EventBindManager()

        def __init__(self):
            self.__mmm = C()


            self.binder.bind_all(self)

        @binder('__mmm.event_aaa')
        def handler1(self, msg):
            print 5555, msg

#         @binder('event2')
#         def handler2(self, msg):
#             print 4444, msg


    class C(object):
        def __init__(self):
            self.__event_aaa = NagaraEvent()

        @property
        def event_aaa(self):
            return self.__event_aaa

        def fire(self):
            self.event_aaa.fire(self)
         

    event1 = NagaraEvent()
    event1.bind(listener1)
    event1.fire()

    a = A()

    a.fire1()
    a.fire2()


