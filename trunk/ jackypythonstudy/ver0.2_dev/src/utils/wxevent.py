#  -*- encoding: utf-8 -*-
import os, sys
import wx
from decorator import decorator

from pubsub import pub

class UnknownError: pass

def decorator_factory(deco_arg): # partial is functools.partial
    "decorator_factory(deco_arg) returns a one-parameter family of decorators"
    return partial(lambda df, param: decorator(partial(df, param)), deco_arg)

class NagaraEvent(wx.PyEvent):
    def __init__(self, event_handler, data=None):
        wx.PyEvent.__init__(self)
        self.__event_handler = event_handler
        self.SetEventType(wx.NewEventType())
        self.__data = data
        self.__binder = wx.PyEventBinder(self.get_event_type(), 1)

    # property: data
    def get_data(self):
        return self.__data
    def set_data(self, d):
        self.__data = d
    data = property(get_data, set_data)

    def bind(self, handler):
        self.__event_handler.Bind(self.__binder, handler)

    def get_event_handler(self):
        return self.__event_handler

    def get_event_type(self):
        return self.GetEventType()

    def fire(self):
        self.get_event_handler().ProcessEvent(self)


def fire(nagara_event):
    pf_event.get_event_handler().ProcessEvent(nagara_event)

def handler(nagara_event):
    """Decorator to bind Nagara_Event and handler.
    Example:
        # in any class
        @handler(event)
        def handler_method(self):
            ...
    """
    def wrapper(fun, *args, **kwds):
        return fun(*args, **kwds)
    try:
        nagara_event.bind(fun)
    except AttributeError: 
        if issubclass(event_src.__class__, wx.EvtHandler):
            raise 'cannot bind between event and handler'
        else:
            raise UnknownError()
    return decorator(wrapper)


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

class BindManager:
    binds = {}
    def __init__(self):
        self.binds[hash(self)] = set()

    def __call__(self, *args, **keys):
        def deco(func):
            self.binds[hash(self)].add((func.func_name, args, ImmutableDict(keys)))
            return func
        return deco

    def bindall(self, obj):
        for func_name, args, keys in self.binds[hash(self)]:
            keys = dict(keys)
            if keys.has_key('event'):
                event = keys['event']
                del keys['event']
            else:
                event = args[0]
                args = list(args[1:])
                control = obj
            if keys.has_key('id'):
                if isinstance(keys['id'], str):
                    keys['id'] = XRCID(keys['id'])
            if keys.has_key('control'):
                control = keys['control']
                if isinstance(control, str):
                    control = XRCCTRL(obj, control)
                del keys['control']
            control.Bind(event, getattr(obj, func_name), *args, **keys)

# def binder(evtbinder, *bindargs, **bindkwds):
#     
#     def wrapper(fun, *args, **kwds):
#         return fun(*args, **kwds)
#     self.bind
#     return decorator(wrapper)


