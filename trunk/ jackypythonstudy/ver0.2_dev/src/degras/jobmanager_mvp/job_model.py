#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura
#
# $Date$
# $Rev$
# $Author$
#

# standard modules
import os, sys

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from utils.event import NagaraEvent, EventBindManager
from core.exception import NagaraException

class NotUsedRequestError(NagaraException): pass

from interfaces.ijob_model import IJobModel
class JobModel(IJobModel):

    binder = EventBindManager()

    def __init__(self, job):

        self.__job = job

        # define properties
        self.__is_selected = False

        # generate events
        self.__delete_event = NagaraEvent()
        self.__init_event = NagaraEvent()
        self.__state_changed_event = NagaraEvent()
        self.__update_event = NagaraEvent()

        # define_request()
        self.__define_request()

        self.binder.bind_all(self)

    # properties
    @property
    def expected_time(self):
        return self.__job.expected_time

    @property
    def finish_time(self):
        return self.__job.finish_time

    @property
    def id(self):
        return self.__job.id

    @property
    def jms(self):
        return self.__job.jms

    @property
    def location(self):
        return self.__job.location

    @property
    def name(self):
        return self.__job.name

    @property
    def project(self):
        return self.__job.project

    @property
    def start_time(self):
        return self.__job.start_time

    @property
    def elasped_time(self):
        return self.__job.elasped_time


    # events
    @property
    def delete_event(self):
        return self.__delete_event

    @property
    def init_event(self):
        return self.__init_event

    @property
    def state_changed_event(self):
        return self.__state_changed_event

    @property
    def update_event(self):
        return self.__update_event

    # enables
    def is_selected(self):
        return self.__is_selected

    def enable_selected(self, enable=True):
        self.__is_selected = enable

    # methods
    def init(self):
        self.init_event.fire()

    def get_available_request_dict(self):
        return self.__request_dict

    def __define_request(self):
        self.__request_dict = {}
        ava_req_list = self.__job.get_available_request()
        all_req_list = self.__job.get_all_request()
        for req in all_req_list:
            self.__request_dict[req] = True if req in ava_req_list else False

    def get_state(self):
        return self.__job.state

    def request_submit(self):
        print self.__request_dict
        if self.__request_dict['request_submit']:
            self.__job.request_submit()
        else:
            raise NotUsedRequestError('request_submit')

    def request_convert(self):
        print self.__request_dict
        if self.__request_dict['request_convert']:
            self.__job.request_convert()
        else:
            raise NotUsedRequestError('request_convert')

    def request_send(self):
        if self.__request_dict['request_send']:
            self.__job.request_send()
        else:
            raise NotUsedRequestError('request_send')

    def request_run(self):
        if self.__request_dict['request_run']:
            self.__job.request_run()
        else:
            raise NotUsedRequestError('request_run')

    def request_stop(self):
        if self.__request_dict['request_stop']:
            self.__job.request_stop()
        else:
            raise NotUsedRequestError('request_stop')

    def request_rerun(self):
        if self.__request_dict['request_rerun']:
            self.__job.request_rerun()
        else:
            raise NotUsedRequestError('request_rerun')

    def request_cancel(self):
        if self.__request_dict['request_cancel']:
            self.__job.request_cancel()
        else:
            raise NotUsedRequestError('request_cancel')

    def request_delete(self):
        if self.__request_dict['request_delete']:
            self.__job.request_delete()
        else:
            raise NotUsedRequestError('request_delete')

    def request_receive(self):
        if self.__request_dict['request_receive']:
            self.__job.request_receive()
        else:
            raise NotUsedRequestError('request_receive')

    def request_sync(self):
        if self.__request_dict['request_sync']:
            self.__job.request_sync()
        else:
            raise NotUsedRequestError('request_sync')

    def is_auto(self):
        return self.__job.is_auto()

    def enable_auto(self, enable):
        self.__job.enable_auto(enable)

    # listeners
    @binder('__job.state_event')
    def change_state(self, msg):
        self.__define_request()
        self.state_changed_event.fire()

    @binder('__job.update_event')
    def update_in_job(self, msg):
        self.update_event.fire(msg)
