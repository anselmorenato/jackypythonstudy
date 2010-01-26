#  -*- encoding: utf-8 -*-
import os, sys

class ConvertManager(object):

    def __init__(self):
        self.__options = []

    def __call__(self, fun):
        self.__options.append(fun.func_name)
        return fun

    def convert_all(self, obj):
        self.__new_options = {}

        for fun_name in self.__options:
            self.__new_options[fun_name] = getattr(obj, fun_name)()

    def get_converted_options(self):
        return self.__new_options


def main():
    pass

if __name__ == '__main__':
    main()


