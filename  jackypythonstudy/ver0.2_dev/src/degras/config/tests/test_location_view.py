#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura
#
# $Date: 2010-01-20 13:51:41 +0900 (水, 20 1 2010) $
# $Rev: 53 $
# $Author: ishikura $
#
# standard modules
import os, sys
from nose.tools import *
import wx

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from utils.test_helper import *
sys.path.append( '../' )

set_bodypath(__file__)


from location_view import LocationView
from core.config import Config
class TestLocationManagerView:

    def setup(self):
        self.app = wx.App()
        self.view = LocationView()
        self.config = Config().get_common()['location']['hpcs']

        self.expected_prop_list = [
            'name', 'workdir', 'shell', 'init_file', 'env_dict',
            'mpi', 'ssh_address', 'ssh_username', 'ssh_password', 'ssh_port',
            'command_dict', 'jms_dict', 'jms_default',
        ] 


    def teardown(self):
        wx.CallAfter(self.app.Exit)
        self.app.MainLoop()
        self.view   = None

    def test_name(self):
        self.view.name = self.config['name']
        assert_equal(self.view.name, self.config['name'])

    def test_workdir(self):
        self.view.workdir = self.config['workdir']
        assert_equal(self.view.workdir, self.config['workdir'])

    def test_shell(self):
        self.view.shell = self.config['shell']
        assert_equal(self.view.shell, self.config['shell'])

    def test_init_file(self):
        self.view.init_file = self.config['init_file']
        assert_equal(self.view.init_file, self.config['init_file'])

    def test_mpi(self):
        self.view.mpi = self.config['mpi']
        assert_equal(self.view.mpi, self.config['mpi'])

    def test_env_dict(self):
        self.view.env_dict = self.config['envs']
        assert_equal(self.view.env_dict, self.config['envs'])

    def test_ssh_address(self):
        self.view.ssh_address = self.config['ssh']['address']
        assert_equal(self.view.ssh_address, self.config['ssh']['address'])

    def test_ssh_username(self):
        self.view.ssh_username = self.config['ssh']['username']
        assert_equal(self.view.ssh_username, self.config['ssh']['username'])

    def test_ssh_password(self):
        self.view.ssh_password = self.config['ssh']['password']
        assert_equal(self.view.ssh_password, self.config['ssh']['password'])

    def test_ssh_port(self):
        self.view.ssh_port = self.config['ssh']['port']
        assert_equal(self.view.ssh_port, self.config['ssh']['port'])

    def test_command_dict(self):
        self.view.command_dict = self.config['commands']
        command_config = self.view.command_dict
        self.view.command_dict = command_config
        assert_equal(self.view.command_dict, command_config)

    def test_jms_dict(self):
        jms_config = self.config['jms']
        jms_config.pop('default')
        self.view.jms_dict = jms_config

        exp_jms_config = self.view.jms_dict
        self.view.jms_dict = jms_config
        assert_equal(self.view.jms_dict, exp_jms_config)
