#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura

# standard modules
import os, sys

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from utils.event import NagaraEvent

from interfaces.imanager_view import IManagerView
class ManagerView(IManagerView):
    def __init__(self):

        # define properties
        self.__is_auto = True

        # generate events
        self.__cancel_event = NagaraEvent()
        self.__convert_event = NagaraEvent()
        self.__delete_event = NagaraEvent()
        self.__receive_event = NagaraEvent()
        self.__rename_event = NagaraEvent()
        self.__request_event = NagaraEvent()
        self.__rerun_event = NagaraEvent()
        self.__run_event = NagaraEvent()
        self.__select_event = NagaraEvent()
        self.__send_event = NagaraEvent()
        self.__set_auto_event = NagaraEvent()
        self.__stop_event = NagaraEvent()
        self.__submit_event = NagaraEvent()
        self.__sync_event = NagaraEvent()
        self.__update_event = NagaraEvent()

    # events
    @property
    def cancel_event(self):
        return self.__cancel_event

    @property
    def convert_event(self):
        return self.__convert_event

    @property
    def delete_event(self):
        return self.__delete_event

    @property
    def receive_event(self):
        return self.__receive_event

    @property
    def rename_event(self):
        return self.__rename_event

    @property
    def request_event(self):
        return self.__request_event

    @property
    def rerun_event(self):
        return self.__rerun_event

    @property
    def run_event(self):
        return self.__run_event

    @property
    def select_event(self):
        return self.__select_event

    @property
    def send_event(self):
        return self.__send_event

    @property
    def set_auto_event(self):
        return self.__set_auto_event

    @property
    def stop_event(self):
        return self.__stop_event

    @property
    def submit_event(self):
        return self.__submit_event

    @property
    def sync_event(self):
        return self.__sync_event

    @property
    def update_event(self):
        return self.__update_event

    # enables
    def enable_auto(self, enable=True):
        self.__auto = enable
    def is_auto(self):
        return self.__is_auto

    # methods
    def append(self):
        pass

    def update_all(self):
        pass

    def get_selected_jobid_list(self):
        pass

    def get_jobname(self):
        pass

    def popup_jobmenu(self):
        pass

