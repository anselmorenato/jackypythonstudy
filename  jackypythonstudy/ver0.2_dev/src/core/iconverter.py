#  -*- encoding: utf-8 -*-
# Copyright (C)  2009 Takakazu Ishikura
import os, sys

from abc import abstractmethod, abstractproperty, ABCMeta

# Nagara Modules
from exception import NagaraException


class INDOConverter():
    """
    Class to treat the conversion from a Nagara Data Object to a format or
    from a format to a Nagara Data Object.
    """
    __metaclass__ =  ABCMeta

    def __init__(self):
        """Constructor."""


class MoleculeFormatException(NagaraException): pass
class InvalidFormatException(NagaraException): pass


class MoleculeFileTypeError(MoleculeFormatException):
    def __init__(self, suffix):
        MoleculeFormatException.__init__(self)
        assert isinstance(suffix, str), 'suffix type : ' + type(suffix)
        self.suffix = suffix
        self.message = 'Suffix name *.%s is not supported' % suffix

    def __repr__(self):
        return message

class MolFormatFile(object):
    def __init__(self, filename=None):
        self.filename = filename
        self.system = None

    def __str__(self):
        pass

    def __repr__(self):
        pass

    # def __enter__(self):
    #     raise NotImplementation

    # def __exit__(self):
    #     raise NotImplementation

    def __toSystem(self):
        raise NotImplementation

    def __fromSystem(self):
        raise NotImplementation

    def read(self):
        raise NotImplementation

    def write(self, system):
        raise NotImplementation

class IChecker:
    __metaclass__ = ABCMeta

    @abstractmethod
    def check(self): pass

class IParser(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def set_file_dict(self, file_dict): pass

    @abstractmethod
    def get_ndo(self): pass


class IFormatter(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def set_ndo(self, ndo): pass

    @abstractmethod
    def get_file_dict(self): pass


class SuffixChecker(object):
    pass

class IConverterCommand(object):

    @abstractmethod
    def set_input_dict(self, format_filename_dict): pass
    
    @abstractmethod
    def set_output_dict(self, format_filename_dict): pass

    @abstractmethod
    def run_convert(self): pass


if __name__ == '__main__':
    pass
