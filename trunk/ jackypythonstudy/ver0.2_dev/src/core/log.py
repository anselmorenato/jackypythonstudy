#  -*- encoding: utf-8 -*-
import os, sys
import datetime

# if __name__ == '__main__':
#     sys.path.append('../')
# from utils.pattern   import Singleton

class Log(object):
    def __init__(self, message, timetype='short'):
        if timetype=='long':
            self.__prefix = self.get_long_time()
        elif timetype=='short':
            self.__prefix = self.get_short_time()
        else:
            self.__prefix = ''
            
        mes = self.__prefix + ' : ' + message
        print(mes)

    def get_long_time(self):
        date = datetime.datetime.today()
        now = date.strftime("%Y.%m%d.%H:%M:%S")
        return now

    def get_short_time(self):
        date = datetime.datetime.today()
        now = date.strftime("%m/%d %H:%M:%S")
        return now

if __name__ == '__main__':
    Log('aaa', timetype='long')
    Log('aaa')
