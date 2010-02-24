#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura
#
# $Date: 2010-02-16 20:48:33 +0900 (火, 16 2 2010) $
# $Rev: 90 $
# $Author: ishikura $
#

# standard modules
import os, sys

# zope modules
from zope.interface        import Interface, providedBy, implements, Attribute
from zope.interface        import Invalid, invariant
from zope.interface.verify import verifyObject, verifyClass
from zope import schema


class NotFoundInterfaceError(Exception): pass
class NotFoundAttributeError(Exception): pass

class ModelBase(object):
    """
    The ModelBase has that verify whether the given object satisfy
    the spec of the defined interface or not ,and validate the set attribute
    by validate method of the field.

    Setup

    >>> def constraint(string):
    ...     return True if len(string) <= 10 else False

    >>> class ITest(Interface):
    ...     test1 = schema.TextLine(
    ...         title=u"the test string",
    ...         default=u'hogehoge',
    ...         constraint=constraint)
    ...
    ...     i = schema.Int(
    ...         title=u"i value",
    ...         default=100)
    ...
    ...     j = schema.Int(
    ...         title=u"j value",
    ...         default=50)
    ...         
    ...     @invariant
    ...     def validateInt(test):
    ...         if test.i < test.j:
    ...             mes = 'i = {0}, j = {1}'.format(test.i, test.j)
    ...             raise Invalid(mes)
    ...

    When not implemented, 

    >>> class Test1(ModelBase):
    ...     # implements(ITest)
    ...     pass

    >>> t = Test1()
    Traceback (most recent call last):
        ...
    NotFoundInterfaceError: The class: 'Test1' have not any interfaces.

    When implemented, 

    >>> class Test2(ModelBase):
    ...    implements(ITest)
    ...
    ...    def hello(self):
    ...        print 'hello'

    >>> t = Test2()
    >>> t.test1
    u'hogehoge'

    when ascii string

    >>> t.test1 = "string"
    Traceback (most recent call last):
        ...
    WrongType: ('string', <type 'unicode'>, 'test1')

    >>> t.test1 = u"long logn string"
    Traceback (most recent call last):
        ...
    ConstraintNotSatisfied: long logn string

    >>> t.test1
    u'hogehoge'

    >>> t.i = 5
    >>> t.i
    5

    >>> t.j = 10
    >>> t.j
    10

    >>> t.validateInvariants()
    Traceback (most recent call last):
        ...
    Invalid: i = 5, j = 10


    list testmod

    >>> a = range(0, 100)
    >>> a # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    [0, 1, ..., 98, 99]

    """

    def __init__(self):
        interface_list = self.__getAndvalidateInterface()
        # print self.__class__.__name__
        self.__setDefault(interface_list)
        for inter in interface_list:
            verifyObject(inter, self)

    def __setattr__(self, attrname, value):
        # if not attrname.startswith('_'+self.__class__.__name__):
        self.__validate(attrname, value)
        self.__dict__[attrname] = value

    def dump(self, model_dict=None):
        """Decode from ModelBase object to dict object."""
        self.validateInvariants()

        interface_list = self.__getAndvalidateInterface()
        if model_dict is None:
            model_dict = {}

        for inter in interface_list:
            attrname_list = schema.getFieldNames(inter)
            for an in attrname_list:
                value = getattr(self, an)
                if issubclass(value.__class__, ModelBase):
                    model_dict[an] = {}
                    value.dump(model_dict[an])
                else:
                    model_dict[an] = value
        return model_dict

    def load(self, model_dict):
        """Encode from dict object to ModelBase object."""
        for attrname, value in model_dict.items():

            if hasattr(self, attrname):
                if isinstance(value, dict):
                    model_obj = getattr(self, attrname)
                    model_obj.load(value)
                else:
                    setattr(self, attrname, value)
            else:
                mes = ("\nThe attribute: {attrname} could'nt be found "
                       "in class: {clsname}"
                )
                raise NotFoundAttributeError(mes.format(
                    clsname=self.__class__.__name__, attrname=attrname))

        self.validateInvariants()
        return True

    def validateInvariants(self):
        interface_list = self.__getAndvalidateInterface()
        for inter in interface_list:
            inter.validateInvariants(self)

    def __getAndvalidateInterface(self):
        interface_list = list(providedBy(self))
        if interface_list == []:
            clsname = self.__class__.__name__
            mes = "The class: '{0}' have not any interfaces.".format(clsname)
            raise NotFoundInterfaceError(mes)
        return interface_list

    def __validate(self, attrname, value):
        interface_list = self.__getAndvalidateInterface()
        for inter in interface_list:
            if inter.get(attrname):
                inter.get(attrname).validate(value)
                break
        else:
            raise AttributeError("Not found interface attribute: "+attrname)

    def __setDefault(self, interface_list):
        for inter in interface_list:
            for attrname, field in schema.getFields(inter).items():

                # check whether self object has the given attribute.
                if hasattr(self, attrname): continue

                # if self object has the given attribute, interface default
                # value will be set.
                if field.default is not None:
                    self.__dict__[attrname] = field.default
                    # setattr(self, attrname, field.default)

def test():
    import doctest
    doctest.testmod()

def test2():

    def prop(fun):
        return property(**fun())
    
    def constraint(val):
        return True if len(val)<=10 else False

    class ISubTest(Interface):
        """
        """
        i = schema.Int(
            title=u"integer i",
            default=1)
            
        j = schema.Int(
            title=u"integer j",
            default=2)

        @invariant
        def validateInt(sub):
            if sub.i < sub.j:
                mes = "i >= j must be, but i:{0}, j:{1}".format(sub.i, sub.j)
                raise Invalid(mes)


    class ITest(Interface):
        """
        """
        teststring = schema.TextLine(
            title=u"the test string",
            default=u'hogehoge',
            constraint=constraint)

        testobject = schema.Object(
            title=u"Sub Test",
            schema=ISubTest)


    class Test(ModelBase):
        implements(ITest)

        def __init__(self):
            self.testobject = SubTest()
            ModelBase.__init__(self)

        # the property can't use

        # @prop
        # def teststring():
        #     def fget(self):
        #         try:
        #             return self.__teststring
        #         except AttributeError:
        #             self.__teststring = u"555"
        #             return self.__teststring
        #     def fset(self, teststring):
        #         self.__teststring = teststring
        #     return locals()


    class SubTest(ModelBase):
        implements(ISubTest)
        def __init__(self):
            ModelBase.__init__(self)

        
    t = Test()
    print t.teststring
    t.testobject.i = 150
    print t.testobject.i

    save_dict = t.dump()
    config = dict(
        teststring=u'buta',
        testobject=dict(i=25, j=23, method='cg'),
    )
    t.load(config)


if __name__ == '__main__':
    test2()

