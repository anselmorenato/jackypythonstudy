#  -*- encoding: utf-8 -*-
# Copyright (C)  2009 Takakazu Ishikura
import os, sys

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from utils.event import NagaraEvent

from ilocationmanager_view import ILocationManagerView
class LocationManagerView(ILocationManagerView):
    def __init__(self):

        # define properties

        # generate events
        self.__close_event = NagaraEvent()
        self.__copy_event = NagaraEvent()
        self.__create_event = NagaraEvent()
        self.__delete_event = NagaraEvent()
        self.__edit_event = NagaraEvent()
        self.__rename_event = NagaraEvent()
        self.__select_event = NagaraEvent()
        self.__set_default_event = NagaraEvent()

    # events
    @property
    def close_event(self):
        return self.__close_event

    @property
    def copy_event(self):
        return self.__copy_event

    @property
    def create_event(self):
        return self.__create_event

    @property
    def delete_event(self):
        return self.__delete_event

    @property
    def edit_event(self):
        return self.__edit_event

    @property
    def rename_event(self):
        return self.__rename_event

    @property
    def select_event(self):
        return self.__select_event

    @property
    def set_default_event(self):
        return self.__set_default_event

    # methods
    def init(self):
        pass

    def set_location_list(self):
        pass

    def close(self):
        pass

    def rename(self):
        pass

    def get_name(self):
        pass

    def get_default(self):
        pass

    def get_current(self):
        pass

    def show_config(self):
        pass

