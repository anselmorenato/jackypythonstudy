#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura
#
# $Date$
# $Rev$
# $Author$
#
# standard modules
import os, sys
from nose.tools import *

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from utils.test_helper import *
sys.path.append( '../' )

set_bodypath(__file__)


from locationmanager_model import LocationManagerModel, ConfigNotFoundError, ConfigNotSelectedError
class TestNoLocation:

    def setup(self):
        class LocationShower:
            def __init__(self): pass

        self.model = LocationManagerModel()
        shower     = LocationShower()
        self.model.install(shower)

    def teardown(self):
        self.model = None

    def test_init(self):
        assert_equal( len(self.model.get_location_list()) , 0)

    def test_create(self):
        name = 'new location'
        self.model.create(name)
        assert_equal( len(self.model.get_location_list()), 1)
        expected = set([name])
        assert_equal( set( self.model.get_location_list() ), expected)

    def test_delete(self):
        assert_catch_exc(ConfigNotFoundError, self.model.delete)

    def test_edit(self):
        assert_catch_exc(ConfigNotFoundError, self.model.edit)

    def test_copy(self):
        assert_catch_exc(ConfigNotFoundError, self.model.copy)

    def test_set_current(self):
        location = 'loation name'
        assert_catch_exc(ConfigNotFoundError, self.model.set_current, location)

    def test_set_current(self):
        loc = 0
        assert_catch_exc(ConfigNotFoundError, self.model.set_current, loc)

    def test_set_default(self):
        location = 'location name'
        assert_catch_exc(ConfigNotFoundError,
                         self.model.set_default, location)

    def test_get_config(self):
        config_dict = self.model.get_config_dict()
        assert_equal(config_dict, {})

    def test_set_config(self):
        config = 'aaa'
        assert_catch_exc(ConfigNotFoundError, self.model.set_config, config)

    def test_get_location_list(self):
        assert_equal( self.model.get_location_list(), [] )

    #def test_destroy(self):
        #assert True


class TestOneLocation:

    def setup(self):
        class LocationShower:
            def __init__(self): pass

        self.model = LocationManagerModel()
        shower     = LocationShower()
        self.model.install(shower)

        self.model.create('test location')

        self.key_list = [
            'name', 'address', 'workdir',
            'ssh', 'environment', 'init_file', 'mpi_command', 'jms', 'commands'
        ]

    def with_selected(self):
        self.model.set_current( 'test location' )

    def test_init(self):
        assert_false( self.model.get_current() )
        assert_equal( len(self.model.get_location_list()), 1 )
        config = self.model.get_config_dict()

        self.with_selected()
        assert_true( self.model.get_current(), 'test location')

        #assert_equal( config.get('test location'), True)

    def test_create(self):
        name = 'second location'
        self.model.create(name)
        assert_equal( len(self.model.get_location_list()), 2 )
        expected = set(['test location', name])
        assert_equal( set( self.model.get_location_list() ), expected)
        assert_false( self.model.get_current() )

    def test_delete(self):
        assert_catch_exc(ConfigNotSelectedError, self.model.delete)

        self.with_selected()
        self.model.delete()
        assert_equal( len(self.model.get_location_list()), 0 )

    def test_edit(self):
        assert_catch_exc(ConfigNotSelectedError, self.model.edit)

        self.with_selected()
        ecatcher = EventCatcher(self.model.edit_event)
        self.model.edit()
        assert_catch_event(ecatcher)

    def test_copy(self):
        assert_catch_exc(ConfigNotSelectedError, self.model.delete)

        self.with_selected()
        self.model.copy()
        assert_equal( len(self.model.get_location_list()), 2 )
        assert_false( self.model.get_current() )

    def test_set_name(self):
        locname = 'changed location'
        assert_catch_exc(ConfigNotSelectedError, self.model.set_name, locname)

        self.with_selected()
        old_locname = self.model.get_current()
        self.model.set_name( locname )
        assert_equal( self.model.get_current(), locname )
        assert old_locname not in self.model.get_location_list()

    def test_set_default(self):
        # invalid
        loc = 'invalid locaiton'
        assert_catch_exc(ConfigNotFoundError, self.model.set_default, loc)
        # valid
        loc = 'test location'
        self.model.set_default(loc)
        assert_equal( self.model.get_default(), loc )

    def test_set_current(self):
        # invalid
        loc = 'invalid locaiton'
        assert_catch_exc(ConfigNotFoundError, self.model.set_current, loc)
        # valid
        loc = 'test location'
        self.model.set_current( loc )
        assert_equal( self.model.get_current() , loc)
 
    def test_get_config_dict(self):
        config = self.model.get_config_dict()['test location']
        ret_keyset = set( config.keys() )
        assert_equal( ret_keyset, set(self.key_list) )
 
    def test_set_config(self):
        assert_catch_exc(ConfigNotSelectedError, self.model.set_config, 'cog')

        self.with_selected()
        config = dict(
             name        = 'new loc'               , 
             address     = '133.66.117.139'        , 
             workdir     = '/home/ishikura/Nagara' , 
             ssh         = {}                      , 
             environment = ''                      , 
             init_file   = '/etc/profile.local'    , 
             mpi_command = 'mpijob mpirun'         , 
             jms         = ''                      , 
             commands    = ''                      , 
        )
        config['ssh']['address']  = 'hpcs.med.nagaoya-u.ac.jp'
        config['ssh']['username'] = 'ishikura'
        config['ssh']['password'] = '********'
        config['ssh']['port']     = 22
        self.model.set_config(config)
        new_config = self.model.get_config_dict()['new loc']
        assert_equal(self.model.get_location_list(), ['new loc'] )
        assert_equal( new_config, config )

    def test_get_location_list(self):
        assert_equal( self.model.get_location_list(), ['test location'] )

    #def test_destroy(self):
        #pass

class TestMoreThanTwoLocation:

    def setup(self):
        class LocationShower:
            def __init__(self): pass

        self.model = LocationManagerModel()
        shower     = LocationShower()
        self.model.install(shower)

        self.model.create('first location')
        self.model.create('second location')

        self.key_list = [
            'name', 'address', 'workdir',
            'ssh', 'environment', 'init_file', 'mpi_command', 'jms', 'commands'
        ]

    def with_selected(self):
        self.model.set_current( 'first location' )

    def test_init(self):
        assert_false( self.model.get_current() )
        assert_equal( len(self.model.get_location_list()), 2 )
        config = self.model.get_config_dict()

        self.with_selected()
        assert_true( self.model.get_current(), 'first location')

        #assert_equal( config.get('test location'), True)

    def test_create(self):
        name = 'third location'
        self.model.create(name)
        assert_equal( len(self.model.get_location_list()), 3 )
        expected = set(['first location', 'second location', name])
        assert_equal( set( self.model.get_location_list() ), expected)
        assert_false( self.model.get_current() )

    def test_delete(self):
        assert_catch_exc(ConfigNotSelectedError, self.model.delete)

        self.with_selected()
        self.model.delete()
        assert_equal( len(self.model.get_location_list()), 1 )

    def test_edit(self):
        assert_catch_exc(ConfigNotSelectedError, self.model.edit)

        self.with_selected()
        ecatcher = EventCatcher(self.model.edit_event)
        self.model.edit()
        assert_catch_event(ecatcher)

    def test_copy(self):
        assert_catch_exc(ConfigNotSelectedError, self.model.delete)

        self.with_selected()
        self.model.copy()
        assert_equal( len(self.model.get_location_list()), 3 )
        assert_false( self.model.get_current() )

    def test_set_name(self):
        locname = 'changed location'
        assert_catch_exc(ConfigNotSelectedError, self.model.set_name, locname)

        self.with_selected()
        old_locname = self.model.get_current()
        self.model.set_name( locname )
        assert_equal( self.model.get_current(), locname )
        assert old_locname not in self.model.get_location_list()

    def test_set_default(self):
        # invalid
        loc = 'invalid locaiton'
        assert_catch_exc(ConfigNotFoundError, self.model.set_default, loc)
        # valid
        loc = 'second location'
        self.model.set_default(loc)
        assert_equal( self.model.get_default(), loc )

    def test_set_current(self):
        # invalid
        loc = 'invalid locaiton'
        assert_catch_exc(ConfigNotFoundError, self.model.set_current, loc)
        # valid
        loc = 'first location'
        self.model.set_current( loc )
        assert_equal( self.model.get_current() , loc)

        loc = 'second location'
        self.model.set_current( loc )
        assert_equal( self.model.get_current() , loc)
 
    def test_get_config_dict(self):
        config = self.model.get_config_dict()['first location']
        ret_keyset = set( config.keys() )
        assert_equal( ret_keyset, set(self.key_list) )

        config = self.model.get_config_dict()['second location']
        ret_keyset = set( config.keys() )
        assert_equal( ret_keyset, set(self.key_list) )
 
    def test_set_config(self):
        assert_catch_exc(ConfigNotSelectedError, self.model.set_config, 'cog')

        config = dict(
             name        = 'new loc'               , 
             address     = '133.66.117.139'        , 
             workdir     = '/home/ishikura/Nagara' , 
             ssh         = {}                      , 
             environment = ''                      , 
             init_file   = '/etc/profile.local'    , 
             mpi_command = 'mpijob mpirun'         , 
             jms         = ''                      , 
             commands    = ''                      , 
        )
        config['ssh']['address']  = 'hpcs.med.nagaoya-u.ac.jp'
        config['ssh']['username'] = 'ishikura'
        config['ssh']['password'] = '********'
        config['ssh']['port']     = 22

        self.with_selected()
        self.model.set_config(config)
        new_config = self.model.get_config_dict()['new loc']
        assert_equal(self.model.get_location_list(),
                     ['new loc', 'second location'] )
        assert_equal( new_config, config )

    def test_get_location_list(self):
        assert_equal( self.model.get_location_list(),
                     ['first location', 'second location'] )

    ##def test_destroy(self):
        ##pass


class TestConfigGivenLocation:

    def setup(self):
        from core.config import Config

        loc_config = Config().get_common()['location']

        class LocationShower:
            def __init__(self): pass

        self.model = LocationManagerModel(loc_config)
        shower     = LocationShower()
        self.model.install(shower)

        self.key_list = [
            'name', 'address', 'workdir',
            'ssh', 'environment', 'init_file', 'mpi_command', 'jms', 'commands'
        ]

        # default config
        self.location_list = self.model.get_location_list()
        self.config = self.model.get_config_dict()

    def teardown(self):
        self.model = None

    def test_init(self):
        assert_false( self.model.get_current() )
        expected_list = set(self.location_list)
        self.current = self.model.get_current()
        
        assert_equal( set( self.model.get_location_list() ), expected_list )

