#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura
#
# $Date$
# $Rev$
# $Author$
#
import os, sys
import inspect

nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from event import NagaraEvent
from zope.interface import providedBy
from zope.schema import getFieldNames


class EventCatcher(object):
    def __init__(self, event):
        self.__event     = event
        self.__pre_count = 0
        self.__cur_count = 0
        self.__msg_list  = []

        assert self.isEvent(), (
            "Object: {0} isn't NagaraEvent."
        ).format(self.__event.__class__.__name__)

        self.__event.bind(self.__catch)

    @property
    def count(self):
        return self.__cur_count

    def trigger(self, msg=None):
        self.__event.fire(msg)

    def isEvent(self):
        return isinstance(self.__event, NagaraEvent)

    def isCatched(self):
        return self.__pre_count+1 == self.__cur_count
    is_catched = isCatched

    def getMessage(self):
        return self.__msg_list[-1]

    def __catch(self, msg):
        self.__pre_count = self.__cur_count
        self.__cur_count += 1
        self.__msg_list.append(msg)
        print('event count: {0}, {1}'.format(self.__cur_count, msg))


def assertCatchEvent(event_catcher, msg=None):
    # assert that NagaraEvent was catched
    assert event_catcher.isCatched(), "NagaraEvent don't got."

    # assert message for NagaraEvent
    if msg:
        exp_msg = msg
        assert exp_msg == event_catcher.getMessage(), (
            "Received message is invalid:\n"
            "  | expected = {0} : {1} ,\n"
            "  |  but got = {2} : {3} ."
        ).format(
            exp_msg, type(exp_msg),
            event_catcher.getMessage(), type(event_catcher.getMessage())
        )


def assertCatchExc(exc_type, fun, *args, **kwds):
    #obj = fun.im_self
    #method = fun.__name__ 

    ## check whether object has method or not.
    #assert hasattr(obj, method), (
        #"Object: {0}\n"
        #"           doesn't have attribute '{1}'."
        #.format(obj, method)
    #)

    try:
        fun(*args, **kwds)
    except exc_type:
        pass
    else:
        assert False, (
            "Exception is invalid:\n"
            "  | expected = {0} ,\n"
            "  |  but could'nt get.").format(exc_type)



def assertNotCatchExc(exc_type, fun, *args, **kwds):
    #obj = fun.im_self
    #method = fun.__name__ 

    ## check whether object has method or not.
    #assert hasattr(obj, method), (
        #"Object: {0}\n"
        #"           doesn't have attribute '{1}'."
        #.format(obj, method)
    #)

    try:
        fun(*args, **kwds)
    except exc_type:
        assert False, (
            "Exception is invalid:\n"
            "  | expected = {0} ,\n"
            "  |  but could'nt get.").format(exc_type)

# def catch_exc_byp(exc_type, obj, method_str):
#     prop = getattr(obj.__class__, method_str)
#     flag = inspect.isdatadescriptor(prop)
# 
#     try:
#         getattr(obj, method_str)
#     except exc_type:
#         pass
#     else:
#         assert False, (
#             "Exception is invalid:\n",
#             "    expected = <{0}>,\n",
#             "     but could'nt get.",).format(exc_type)
#         ret = False

def assertMethod(obj, method, ret=None, args=[], kwds={}):
    # check whether object has method or not.
    expected_ret = ret
    assert hasattr(obj, method), (
        "Object: {0}\n"
        "           doesn't have attribute '{1}'."
        .format(obj, method)
    )

    if not ret:
        return None

    fun = getattr(obj, method)
    ## check whether object has valid arguments and keywords.
    ##     for python version >= 3.0, use inspect.getfullargspec.
    #(fargs, fvarargs, fvarkwds, fdefaults) = inspect.getargspec(fun)
    try:
        ret = fun(*args, **kwds)
    except TypeError as e:
        assert False, e

    # check whether object return valid value
    assert expected_ret == ret, (
        "Return value is invalid:\n"
        "  | expected = {0} : {1} ,\n"
        "  |  but got = {2} : {3} .").format(
            expected_ret, type(expected_ret),
            ret, type(ret)
        )

assert_catch_event = assertCatchEvent
assert_catch_exc = assertCatchExc
assert_not_catch_exc = assertNotCatchExc
assert_method = assertMethod

def set_bodypath(filename):
    current_path = os.path.dirname( filename )
    abspath = os.path.abspath(os.path.join(current_path, '..' ))
    sys.path.append( abspath )

def getProperties(obj):
    """Get properties from obj with Interface."""
    interfaces = list(providedBy(obj))
    if interfaces == []:
        clsname = obj.__class__.__name__
        mes = "The class: '{0}' have not any interfaces.".format(clsname)
        raise NotFoundInterfaceError(mes)

    properties = []
    for inter in interfaces:
        properties.extend( getFieldNames(inter) )
    return properties



