#  -*- encoding: utf-8 -*-
# Copyright (C)  2009 Takakazu Ishikura
import os, sys

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from utils.event import NagaraEvent

from ilocationmanager_model import ILocationManagerModel
class LocationManagerModel(ILocationManagerModel):
    def __init__(self):

        # define properties

        # generate events
        self.__init_event = NagaraEvent()
        self.__select_event = NagaraEvent()
        self.__update_event = NagaraEvent()

    # events
    @property
    def init_event(self):
        return self.__init_event

    @property
    def select_event(self):
        return self.__select_event

    @property
    def update_event(self):
        return self.__update_event

    # methods
    def get_location_list(self):
        pass

    def destroy(self):
        pass

    def create(self):
        pass

    def edit(self):
        pass

    def delete(self):
        pass

    def copy(self):
        pass

    def set_name(self):
        pass

    def set_default(self):
        pass

    def set_current(self):
        pass

    def get_config(self):
        pass

