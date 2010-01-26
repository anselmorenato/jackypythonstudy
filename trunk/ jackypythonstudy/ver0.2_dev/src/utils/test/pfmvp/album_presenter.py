#! /opt/python2.6/bin/python
#  -*- encoding: utf-8 -*-
# Copyright (C)  2009 Takakazu Ishikura

# standard modules
import os, sys

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from  utils.event import  EventBindManager
from  core.log    import  Log

class AlbumPresenter(object):

    
    binder = EventBindManager()    
    def __init__(self, model, view):
        self.__model = model
        self.view = view
    
        self.binder.bind_all(self)

    @binder("__model.change_event")
    def __change_on_model(self, msg):
        self._log_recieve('__change_on_model')

    @binder("__model.update_event")
    def update_on_model(self, msg):
        self._log_recieve('update_on_model')

    @binder("view.change_event")
    def change_on_view(self, msg):
        self._log_recieve('change_on_view')

    @binder("view.update_event")
    def update_on_view(self, msg):
        self._log_recieve('update_on_view')

    def _log_recieve(self, listener_name):
        info_list = self.binder.get_info(listener_name)
        for info in info_list:
            obj = info['object_name']
            evt = info['event_name']
            cls = info['class_name']
            mes = 'Recieved {0} of {1}:{2} at {3}'
            Log( mes.format(evt, obj, cls, listener_name) )

if __name__ == '__main__':
    from album_view import AlbumView
    from album_model import AlbumModel

    v = AlbumView()
    m = AlbumModel()

    p = AlbumPresenter(m, v)

    m.update_event.fire()
    v.change_event.fire()
    m.change_event.fire()


    from pubsub.utils import printTreeDocs
    printTreeDocs(extra="a")
    print '\nTopic tree listeners:'
    printTreeDocs(extra="L")


