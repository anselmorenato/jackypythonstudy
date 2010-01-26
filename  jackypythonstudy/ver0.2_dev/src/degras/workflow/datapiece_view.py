#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura
#
# $Date: 2010-01-20 13:50:28 +0900 (水, 20 1 2010) $
# $Rev: 52 $
# $Author: ishikura $
#

import os, sys


class DataPieceView(object):

    def __init__(self):
        self.__name   = 'Data'
        self.__type   = 'Type'
        self.__format = 'format'

        self.__selected = False

    def is_selected(self):
        return self.__selected

    def set_selected(self, select):
        self.__selected = select

    # property: name
    def get_name(self):
        return self.__name
    def set_name(self, name):
        self.__name = name
    name = property(get_name, set_name)

    # property: type
    def get_type(self):
        return self.__type
    def set_type(self, type):
        self.__type = type
    type = property(get_type, set_type)
    
    # property: format
    def get_format(self):
        return self.__format
    def set_format(self, format):
        self.__format = format
    format = property(get_format, set_format)
    
