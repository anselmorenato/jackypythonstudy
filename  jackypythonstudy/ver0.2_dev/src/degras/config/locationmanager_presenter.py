#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Biao Ma and Takakazu Ishikura
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
from  core.exception import NagaraException
from  utils.event import  EventBindManager
from  core.log    import  Log


class LocationManagerPresenter(object):
    
    def __init__(self, view, loc_config=None):
        self.view = view

        if loc_config:
            self.loc_config = loc_config
            self.setLocationList()
        else:
            loc_config = {}
            self.view.enable('ID_edit_button', False)
            self.view.enable('ID_copy_button', False)
            self.view.enable('ID_del_button',  False)
        self.loc_config = loc_config

    def select(self):
        locname = self.view.getSelected()
        if locname:
            config = self.loc_config[locname]
            self.view.showConfig( config )

            # for view
            self.view.enable('ID_edit_button', True)
            self.view.enable('ID_copy_button', True)
            self.view.enable('ID_del_button',  True)
            ret = True
        else:
            ret = False
        return ret

    def popup(self):
        if self.view.getSelected():
            self.view.popupMenu()
            ret = True
        else:
            ret =  False
        return ret

    def create(self):
        ret = False
        with self.view.getNameDialog('new location') as dlg:
            locname = dlg.getName()
            self.checkName(locname)

            config = dict(
                name    = locname , 
                address = '' ,
                workdir = '' ,
                ssh = dict(
                    address  = '' , 
                    username = '' , 
                    password = '' , 
                    port     = '' , 
                ),
                environment = '' ,
                init_file   = '' ,
                mpi_command = '' ,
                jms         = {} , 
                commands    = {} ,
            )
            self.loc_config[locname] = config

            # fr view
            self.view.appendLocation(locname)
            self.view.appendDefault(locname)
            ret = True
        return ret

    def edit(self):
        locname = self.view.getSelected()

    def copy(self):
        curname = self.view.getSelected()
        if curname:
            with self.view.getNameDialog(curname) as dlg:
                newname = dlg.getName()
                self.checkName(newname)

                config = self.loc_config[curname]
                import copy
                self.loc_config[newname] = copy.deepcopy(config)
                self.loc_config[newname]['name'] = newname
                self.view.appendLocation(newname)
                self.view.appendToDefault(newname)

    def delete(self):
        locname = self.view.getSelected()
        if locname:
            del self.loc_config[locname]
            self.setLocationList()
            self.view.clearTreeView()

    def setDefault(self):
        self.loc_config['default'] = self.view.default

    def close(self):
        pass

    def setLocationList(self):
        self.view.clearList()
        self.view.clearDefault()
        for locname in self.loc_config.keys():
            if locname == 'default':
                self.view.default = self.loc_config['default']
            else:
                self.view.appendLocation(locname)
                self.view.appendDefault(locname)

    def checkName(self, locname):
        if locname in self.loc_config.keys():
            mes = 'The given name: {0} exists already.'.format(locname)

            from  degras.dialog.base import MessageDialog
            from core.exception import DialogCancelException
            with MessageDialog(mes, 'Information'): pass
            raise DialogCancelException()


if __name__ == '__main__':

    import wx
    app = wx.App(redirect=False)
    frame = wx.Frame(None, -1, 'Location Manager View')

    import locationmanager_view as v

    view = v.LocationManagerView(frame)
    frame.Show()
    from core.config import Config
    config = Config().get_common()['location']
    presen = LocationManagerPresenter(view, config)
    inter = v.LocationManagerInteractor(view, presen)

    

    # # print lmv.GetChildren()
    # print lmv.getCtrl('ID_new_button').GetName()
    # print list(lmv.getCtrlNames())

    # frame.Show()

    # config = dict(
        # name = 'hoge',
        # test = '',
        # fuga = '999',
        # ddd  = dict(
            # hoge1 = 'fuga1',
            # hoge2 = 'fuga2',
            # hoge3 = 'fuga3',
        # ),
        # test2 = 'test2',
    # )

    # config2 = dict(
        # name = 'name2',
        # test = 'unnunn',
        # fuga = '50',
        # ddd  = dict(
            # hoge1 = 'doc1',
            # hoge2 = 'doc2',
            # hoge3 = 'doc3',
        # ),
        # test2 = 'tttt2',
    # )

    # lmv.showConfig(config)
    # loclist = ['vlsn', 'hpcs', 'test loc']
    # lmv.setLocationList(loclist)


    # import time
    # import threading
    
    # def wait1(interval):
        # time.sleep(interval)
        # loclist = ['a', 'b', 'c loc']
        # lmv.setLocationList(loclist)

    # def wait2(interval):
        # time.sleep(interval)
        # lmv.setDefault('c loc')

    # def wait3(interval):
        # time.sleep(interval)
        # lmv.setDefault('c loc')
        # lmv.showConfig(config2)

    # t1 = threading.Thread(name=None, target=wait1, args=[1])
    # t2 = threading.Thread(name=None, target=wait2, args=[2])
    # t3 = threading.Thread(name=None, target=wait3, args=[3])

    # t1.start()
    # t2.start()
    # t3.start()


    app.MainLoop()
