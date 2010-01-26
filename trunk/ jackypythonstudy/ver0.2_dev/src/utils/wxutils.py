#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura
#
# $Date: 2010-01-22 14:43:39 +0900 (金, 22 1 2010) $
# $Rev: 66 $
# $Author: ishikura $
#
import os, sys

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


class BindManager(object):

    binds = {}

    def __init__(self, use_log=True):
        self.binds[hash(self)] = set()
        self.__eventinfo_list = []
        self.__use_log = use_log

    def __call__(self, *dargs, **dkeys):
        def deco(func):
            self.binds[hash(self)].add(
                (func.func_name, dargs, ImmutableDict(dkeys))
                # (func, dargs, ImmutableDict(dkeys))
            )
            return func
        return deco

    def bindAll(self, obj, interactor):
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
                if not isinstance(keys['id'], str): continue
                keys['id'] = obj.getCtrlById(keys['id'])

            elif len(args) >= 1:
                if not isinstance(args[0], str): continue
                ctrl_name = args[0]
                control = obj.getCtrl(ctrl_name)
                args = list( args[1:] )

            else:
                pass

            control.Bind(
                event, getattr(interactor, func_name), *args, **keys)

    def log(self):
        # for func_name, args, keys in self.binds[hash(self)]:
            # print func_name, args
        for func, args, keys in self.binds[hash(self)]:
            print func.func_name, args

    # def get_eventinfo_list(self):
        # return self.__eventinfo_list

    # def get_info(self, handler):
        # evt_info = []
        # for info in self.__eventinfo_list:
            # if info['handler_name'] == handler:
                # evt_info.append( dict(
                    # class_name = info['class_name'],
                    # object_name = info['object_name'],
                    # event_name = info['event_name'],
                # ))
        # return evt_info
