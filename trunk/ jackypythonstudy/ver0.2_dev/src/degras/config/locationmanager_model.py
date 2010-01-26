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

class ConfigNotFoundError(NagaraException): pass
class NameDuplicatedError(NagaraException): pass
class ConfigNotSelectedError(NagaraException): pass


    def set_config(self, config):
        self.check_none()
        self.check_selected()
        newname = config['name']
        curname = self.get_current()
        if newname == curname:
            self.__config_dict[curname] = config
        else:
            self.__config_dict[curname] = config
            self.set_name( newname )

    def edit(self):
        self.check_none()
        self.check_selected()
        self.edit_event.fire()
        # config = show_and_get_config(
        #     self.__config_dict[self.__current_location] )

    def set_name(self, name):
        self.check_none()
        self.check_selected()
        if name in self.get_location_list():
            raise NameDuplicatedError()
        config = self.__config_dict.pop( self.get_current() )
        config['name'] = name
        self.__config_dict[name] = config
        self.__current_location = name

    def check_none(self):
        if not self.__config_dict:
            raise ConfigNotFoundError()

    def check_name(self, name):
        if name not in self.__config_dict.keys():
            raise ConfigNotFoundError(name)

    def check_selected(self):
        if not self.__current_location:
            raise ConfigNotSelectedError()

    def install(self, shower=None):
        if shower:
            self.__shower = shower
        else:
            self.__shower = LocationShower(self)


class LocationShower(object):

    binder = EventBindManager()

    def __init__(self, manager):

        self.manager = manager

        model     = LocationModel()
        view      = LocationView()
        presenter = LocationPresenter(model, view)
        self.location_model = model

        binder.binda_all(self)

    @binder('manager.edit_event')
    def show_dialog(self, msg):
        cur_loc = self.manager.get_current()
        config = self.manager.get_config_dict()[cur_loc]
        self.location_model.set_config( config )
        self.location_model.start()
        config = self.location_model.get_config()
        self.manager.set_config( config )

    #@binder('location_model.update_event')
    #def get_config_in_manager(self, msg):
    #    config = self.location_model.get_config()
    #    self.manager.set_config( config )

    #@binder('location_model.close_event')
    #def close_in_config_dialog(self, msg):
    #    config = self.location_model.get_config()
    #    self.manager.set_config( config )
    #    self.location_model.close()


# def show_config_dialog(config):
#     return config
# 
# def show_and_get_config(config):
#     model     = LocationModel()
#     view      = LocationView()
#     presenter = LocationPresenter(model, view)
#     model.set_config(config)
#     model.init()
#     return model.get_config()


if __name__ == '__main__':
    # from core.config import Config
    # config = Config().get_common()['location']
    # print config
    # a = LocationManagerModel(config)
    m = LocationManagerModel()

