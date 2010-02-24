#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura
#
# $Date: 2010-02-22 21:12:36 +0900 (月, 22 2 2010) $
# $Rev: 96 $
# $Author: ishikura $
#
# standard modules
import os, sys
from nose.tools import *

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from utils.test_helper import *
set_bodypath(__file__)


from core.project import Project
from core.task    import Task


def assertRequests(task, exclude_requests, state_name, event_catcher):
    
    if 'defineTaskObject' not in exclude_requests:
        task.defineTaskObject('optimize')
        assert_equal(task.state_name, state_name)
        assert_equal(event_catcher.isCatched(), False)

    if 'changeSocket' not in exclude_requests:
        task.changeSocket()
        assert_equal(task.state_name, state_name)
        assert_equal(event_catcher.isCatched(), False)

    if 'linkData' not in exclude_requests:
        task.linkData('hoge', 'fuga')
        assert_equal(task.state_name, state_name)
        assert_equal(event_catcher.isCatched(), False)

    if 'unlinkData' not in exclude_requests:
        task.unlinkData('fuga')
        assert_equal(task.state_name, state_name)
        assert_equal(event_catcher.isCatched(), False)

    if 'invokeConvert' not in exclude_requests:
        task.invokeConvert()
        assert_equal(task.state_name, state_name)
        assert_equal(event_catcher.isCatched(), False)

    if 'invokeSend' not in exclude_requests:
        task.invokeSend()
        assert_equal(task.state_name, state_name)
        assert_equal(event_catcher.isCatched(), False)

    if 'invokeSubmit' not in exclude_requests:
        task.invokeSubmit()
        assert_equal(task.state_name, state_name)
        assert_equal(event_catcher.isCatched(), False)

    if 'invokeStop' not in exclude_requests:
        task.invokeStop()
        assert_equal(task.state_name, state_name)
        assert_equal(event_catcher.isCatched(), False)

    if 'invokeAbort' not in exclude_requests:
        task.invokeAbort()
        assert_equal(task.state_name, state_name)
        assert_equal(event_catcher.isCatched(), False)

    if 'invokeReceive' not in exclude_requests:
        task.invokeReceive()
        assert_equal(task.state_name, state_name)
        assert_equal(event_catcher.isCatched(), False)

def assertProperties(task, properties={}):
    for prop, exp_value in properties.items():
        value = getattr(task, prop)
        assert_equal(value, exp_value)


class TestNoneObjectState:

    def setUp(self):
        p = Project(name='Test Project')
        self.task = Task(p)
        p.append_task(self.task)

        props = getProperties(self.task)
        self.props = [
            'project_name' , 'id'         , 'name'
            'description' , 'path'       , 'taskobject_name' , 
            'taskobject_help', 
            'command_name' , 'setting'    , 'config'          , 
            'config_view'  , 'state_name' , 
            'inputs'       , 'outputs'    , 
        ]

        self.methods = [
            'save' , 'load' , 'copy' , 'delete' , 'tail' ,
        ]

        self.requests = [
            'defineTaskObject' , 'invokeConvert' , 'invokeSend'  , 
            'invokeSubmit'     , 'invokeStop'    , 'invokeAbort' , 
            'invokeReceive'    , 
        ]
        self.event = self.task.getEvent('none_object')
        self.event = self.task.getEvent('init')

    def tearDown(self):
        pass

    def testInit(self):
        assert_equal(self.task.project_name    , 'Test Project' ) 
        assert_equal(self.task.id              , 1              ) 
        assert_equal(self.task.name            , 'task 1'       ) 
        assert_equal(self.task.description    , ''         ) 
        assert_equal(self.task.path            , 'path'         ) 
        assert_equal(self.task.state_name      , 'NoneObject'   ) 
        assert_equal(self.task.taskobject_name , 'None'         ) 
        assert_equal(self.task.taskobject_help , 'None'         ) 
        assert_equal(self.task.command_name    , None           ) 
        # assert_equal(self.task.setting,  None)
        # assert_equal(self.task.config,  None)
        # assert_equal(self.task.config_view,  None)
        # assert_equal(self.task.inputs,  None)

    def testSetProperies(self):
        task = self.task

        task.name = 'Test Task'
        assert_equal(task.name, 'Test Task')

        task.description = 'This is a task note'
        assert_equal(task.description, 'This is a task note')

    def testDefineTaskObject(self):
        self.task.defineTaskObject('optimize')
        assert_equal(self.task.state_name, 'Init')

    def testOtherRequests(self):
        ec = EventCatcher(self.task.getEvent('init'))
        assertRequests(self.task, ['defineTaskObject'], 'NoneObject', ec)
        assertProperties(self.task, {})

class TestInitState:

    pass

