#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura

# standard modules
import os, sys

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from utils.event import NagaraEvent

from interfaces.imanager_model import IManagerModel
class ManagerModel(IManagerModel):
    def __init__(self):

        # define properties

        # generate events
        self.__created_event = NagaraEvent()
        self.__delete_event = NagaraEvent()
        self.__init_event = NagaraEvent()
        self.__update_event = NagaraEvent()

    # events
    @property
    def created_event(self):
        return self.__created_event

    @property
    def delete_event(self):
        return self.__delete_event

    @property
    def init_event(self):
        return self.__init_event

    @property
    def update_event(self):
        return self.__update_event

    # methods
    def get_newjobview(self):
        pass

    def get_job_dict(self):
        pass

    def get_jobview(self):
        pass

    def set_selected_jobid_list(self):
        pass

    def delete(self):
        pass

