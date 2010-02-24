#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura
#
# $Date: 2010-02-16 20:47:02 +0900 (火, 16 2 2010) $
# $Rev: 89 $
# $Author: ishikura $
#
# standard modules
import os, sys

import wx.xrc as xrc

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from core.exception import NagaraException
from core.model import *
from utils import include

# Exceptions
class CtrlNotFoundError(NagaraException): pass


class IViewBase(Interface):

    def getCtrl(ctrl_name):
        """Return a control by ctrl id name."""

    def getCtrlById(ctrl_id):
        """Return a menu control by menu id."""

    def enable(ctrl_name, enable):
        """Set enable or disable of control by control id name."""

    def isEnabled(ctrl_name):
        """Return whether a control is enabled or not."""

    def show(ctrl_name, enable):
        """Enable the showable of control."""

    def isShown(ctrl_name):
        """Return whether a control is shown or not."""


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
    _i = 0

    def __init__(self, use_log=True):
        self.binds[hash(self)] = set()
        self.__eventinfo_list = []
        self.__use_log = use_log

    def __call__(self, *dargs, **dkeys):
        def deco(func):

            # # if function name is '_', then it will be named automatically.
            # if func.func_name == '_':
            #     self._i += 1
            #     self._fname = 'handler' + str(self._i)
            # else:
            #     self._fname = func.func_name


            self.binds[hash(self)].add(
                (func.func_name, dargs, ImmutableDict(dkeys)))

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


class ViewBase(object):
    implements(IViewBase)

    def __init__(self):

        # check XRC or hard coding
        self.__checkXRC()

        # verify that a child class implments IView and other interfaces.
        interface_list = self.__getAndvalidateInterface()
        for inter in interface_list:
            verifyObject(inter, self)

    def __checkXRC(self):
        for base_cls in  self.__class__.__bases__:
            cls_name = base_cls.__name__
            if cls_name.startswith('xrc'):
                include(self, XrcCtrlMixin)
                break
                
        else:
            include(self, CtrlMixin)

    def __getAndvalidateInterface(self):
        interface_list = list(providedBy(self))
        if interface_list == []:
            clsname = self.__class__.__name__
            mes = "The class: '{0}' have not any interfaces.".format(clsname)
            raise NotFoundInterfaceError(mes)
        return interface_list

    def enable(self, ctrl_id, enable=True):
        self.getCtrl(ctrl_id).Enable( enable )

    def isEnabled(self, ctrl_id):
        return self.getCtrl(ctrl_id).IsEnabled()

    def show(self, ctrl_id, enable=True):
        self.getCtrl(ctrl_id).Show(enable)

    def isShown(self, ctrl_id):
        return self.getCtrl(ctrl_id).IsShown()


class CtrlMixin:

    def __init__(self):
        self.__idctrl_dict = {}

    def getCtrl(self, ctrl_name):
        ctrl = self.FindWindowByName(ctrl_name)
        if not ctrl:
            raise CtrlNotFoundError(ctrl_name)
        return ctrl

    def getCtrlById(self, id_ctrl_name):
        id_ctrl = self.__idctrl_dict.get(id_ctrl_name)
        if not id_ctrl:
            raise CtrlNotFoundError(id_ctrl_name)
        return id_ctrl

    def setCtrlId(self, ctrl_id, menu):
        self.__idctrl_dict[ctrl_id] = menu

    def getCtrlNames(self):
        for ctrl in self.GetChildren():
            if ctrl.GetName().startswith('ID_'):
                yield ctrl.GetName()

        # for menuitem in self.__menu.GetMenuItems():
        #     print menuitem.GetLabel()

    def getCtrlIdList(self):
        return self.__idctrl_dict.keys()


class XrcCtrlMixin:

    def getCtrl(self, ctrl_name):
        return xrc.XRCCTRL(self, ctrl_name)

    def getCtrlById(self, ctrl_id):
        return xrc.XRCID(self, ctrl_id)

