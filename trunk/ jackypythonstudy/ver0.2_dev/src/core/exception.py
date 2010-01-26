#  -*- encoding: utf-8 -*-
import os, sys

from datetime import datetime

class NagaraException(Exception):

    def __init__(self, data=None, log_fn='log.txt'):
        BaseException.__init__(self)
        self.message = 'Nagara Exception'
        self.log_fn = log_fn
        self.date = datetime.now()
        self.__data = data

#    def __repr__(self):
#        return 'NagaraException'

    def __str__(self):
        if self.__data:
            return repr(self.__data)
        else:
            return ''

    def log(self):
        print self.__data

    def logerror(self):
        logfile = open(self.log_fn, 'a')
        logfile.write(str(self.date) + ' : ' + str(self))
        logfile.close()

    def get_data(self):
        return self.__data


class DialogCancelException(NagaraException): pass
