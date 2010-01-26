#  -*- encoding: utf-8 -*-
import os, sys


from exception import NagaraException

class DataLinkException(NagaraException): pass
class DataLinker(object):

    def __init__(self, data, task, socket_name):

        self.__data = data
        self.__task = task
        self.__socket_name = socket_name
        # check
        self.check_type()

    def check_type(self):
        data = self.__data
        task = self.__task
        sname = self.__socket_name

        if socket_name in task.inputs.keys():
            raise DataLinkException()

        if data.type != task.taskobject[sname]['type']:
            raise DataLinkException()

    def link(self):
        self.__task.inputs[self.__socket_name] = self.__data

