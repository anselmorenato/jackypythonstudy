#! /opt/python2.6/bin/python
#  -*- encoding: utf-8 -*-
# Copyright (C)  2009 Takakazu Ishikura

# standard modules
import os, sys
from abc import ABCMeta, abstractmethod, abstractproperty

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from utils.event import NagaraEvent


class IAlbumModel():
    __metaclass__ =  ABCMeta

    # events
    @abstractproperty
    def change_event(self): pass

    @abstractproperty
    def update_event(self): pass

    # properties with setter
    @abstractmethod
    def get_artist(self): pass
    @abstractmethod
    def set_artist(self, artist): pass
    artist = abstractproperty(get_artist, set_artist)

    @abstractmethod
    def get_classic(self): pass
    @abstractmethod
    def set_classic(self, classic): pass
    is_classic = abstractproperty(get_classic, set_classic)

    @abstractmethod
    def get_composer(self): pass
    @abstractmethod
    def set_composer(self, composer): pass
    composer = abstractproperty(get_composer, set_composer)

    @abstractmethod
    def get_genre(self): pass
    @abstractmethod
    def set_genre(self, genre): pass
    genre = abstractproperty(get_genre, set_genre)

    @abstractmethod
    def get_title(self): pass
    @abstractmethod
    def set_title(self, title): pass
    title = abstractproperty(get_title, set_title)

    @abstractmethod
    def get_year(self): pass
    @abstractmethod
    def set_year(self, year): pass
    year = abstractproperty(get_year, set_year)

    # enables
    @abstractmethod
    def enable_apply(self): pass
    @abstractmethod
    def disable_apply(self): pass
    @abstractmethod
    def is_apply_enabled(self): pass

    @abstractmethod
    def enable_cancel(self): pass
    @abstractmethod
    def disable_cancel(self): pass
    @abstractmethod
    def is_cancel_enabled(self): pass


class AlbumModel(IAlbumModel):
    def __init__(self):

        # define properties
        self._artist = 'artist'
        self._classic = True
        self._composer = 'composer'
        self._genre = 'anime'
        self._title = 'title'
        self._year = 1996
        self._apply = True
        self._cancel = True

        # generate events
        self._change_event = NagaraEvent()
        self._update_event = NagaraEvent()

    # events
    @property
    def change_event(self):
        return self._change_event

    @property
    def update_event(self):
        return self._update_event

    # properties with setter
    def get_artist(self):
        return self._artist
    def set_artist(self, artist):
        self._artist = artist
    artist = property(get_artist, set_artist)

    def get_classic(self):
        return self._classic
    def set_classic(self, classic):
        self._classic = classic
    is_classic = property(get_classic, set_classic)

    def get_composer(self):
        return self._composer
    def set_composer(self, composer):
        self._composer = composer
    composer = property(get_composer, set_composer)

    def get_genre(self):
        return self._genre
    def set_genre(self, genre):
        self._genre = genre
    genre = property(get_genre, set_genre)

    def get_title(self):
        return self._title
    def set_title(self, title):
        self._title = title
    title = property(get_title, set_title)

    def get_year(self):
        return self._year
    def set_year(self, year):
        self._year = year
    year = property(get_year, set_year)

    # enables
    def enable_apply(self):
        self._apply = True
    def disable_apply(self):
        self._apply = False
    def is_apply_enabled(self):
        return self._apply

    def enable_cancel(self):
        self._cancel = True
    def disable_cancel(self):
        self._cancel = False
    def is_cancel_enabled(self):
        return self._cancel

    # send events
    def _send_change(self, event):
        self.change_event.fire()

    def _send_update(self, event):
        self.update_event.fire()

