#  -*- encoding: utf-8 -*-
# Copyright (C)  2009 Takakazu Ishikura

# standard modules
import os, sys
from abc import ABCMeta, abstractmethod, abstractproperty

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from utils.event import NagaraEvent


class ILocationManagerModel():
    __metaclass__ =  ABCMeta

    # events
    @abstractproperty
    def init_event(self): pass

    @abstractproperty
    def select_event(self): pass

    @abstractproperty
    def update_event(self): pass

    # methods
    @abstractmethod
    def copy(self): pass

    @abstractmethod
    def create(self): pass

    @abstractmethod
    def delete(self): pass

    @abstractmethod
    def destroy(self): pass

    @abstractmethod
    def edit(self): pass

    @abstractmethod
    def get_config_dict(self): pass

    @abstractmethod
    def set_config(self): pass

    @abstractmethod
    def get_location_list(self): pass

    @abstractmethod
    def set_current(self): pass

    @abstractmethod
    def set_default(self): pass
