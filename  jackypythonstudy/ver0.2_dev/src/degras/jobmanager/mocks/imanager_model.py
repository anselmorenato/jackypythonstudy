#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura

# standard modules
import os, sys
from abc import ABCMeta, abstractmethod, abstractproperty

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from utils.event import NagaraEvent


class IManagerModel():
    __metaclass__ =  ABCMeta

    # events
    @abstractproperty
    def created_event(self): pass

    @abstractproperty
    def delete_event(self): pass

    @abstractproperty
    def init_event(self): pass

    @abstractproperty
    def update_event(self): pass

    # methods
    @abstractmethod
    def delete(self): pass

    @abstractmethod
    def get_job_dict(self): pass

    @abstractmethod
    def get_jobview(self): pass

    @abstractmethod
    def get_newjobview(self): pass

    @abstractmethod
    def set_selected_jobid_list(self): pass

