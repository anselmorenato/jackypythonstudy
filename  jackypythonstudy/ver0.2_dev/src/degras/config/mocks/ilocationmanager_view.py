#  -*- encoding: utf-8 -*-
# Copyright (C)  2009 Takakazu Ishikura

# standard modules
import os, sys
from abc import ABCMeta, abstractmethod, abstractproperty

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from utils.event import NagaraEvent


class ILocationManagerView():
    __metaclass__ =  ABCMeta

    # events
    @abstractproperty
    def close_event(self): pass

    @abstractproperty
    def copy_event(self): pass

    @abstractproperty
    def create_event(self): pass

    @abstractproperty
    def delete_event(self): pass

    @abstractproperty
    def edit_event(self): pass

    @abstractproperty
    def rename_event(self): pass

    @abstractproperty
    def select_event(self): pass

    @abstractproperty
    def set_default_event(self): pass

    # methods
    @abstractmethod
    def close(self): pass

    @abstractmethod
    def get_current(self): pass

    @abstractmethod
    def get_default(self): pass

    @abstractmethod
    def get_name(self): pass

    @abstractmethod
    def init(self): pass

    @abstractmethod
    def rename(self): pass

    @abstractmethod
    def set_location_list(self): pass

    @abstractmethod
    def show_config(self): pass

