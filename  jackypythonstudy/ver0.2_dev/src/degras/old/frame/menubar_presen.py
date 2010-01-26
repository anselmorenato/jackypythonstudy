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

class MenubarPresenter(object):
    
    binder = EventBindManager()    

    def __init__(self, model, view):
        self.model = model
        self.view = view
    
        self.binder.bind_all(self)

    @binder("model.init_event")
    def init_on_model(self, msg):
        self.__log_recieve('init_on_model')
        menu_list = self.model.get_menu_list()
        self.view.init_menubar(*menu_list)

    @binder("view.run_api_event")
    def run_api_on_view(self, msg):
        self.__log_recieve('run_api_on_view')
        item_id = msg 
        self.model.request_api(item_id)

    @binder("view.search_help_event")
    def search_help_on_view(self, msg):
        self.__log_recieve('run_api_on_view')
        help_word = msg
        self.model.set_help_word(help_word)

    @binder("view.recent_project_event")
    def recent_project_on_view(self, msg):
        self.__log_recieve('recent_project_on_view')
        project_id = msg
        self.model.set_project(project_id)

    @binder("view.recent_file_event")
    def recent_file_on_view(self, msg):
        self.__log_recieve('recent_file_on_view')
        file_id = msg
        self.model.set_file(file_id)

    @binder("model.update_menu_event")
    def update_menu_on_model(self, msg):
        self.__log_recieve('update_menu_on_model')
        menu_label = msg
        menu = self.model.get_menu(menu_label)
        self.view.update_menu(menu_label, menu)

    @binder("model.update_item_event")
    def update_item_on_model(self, msg):
        self.__log_recieve('update_item_on_model')
        item_id = msg
        item = self.model.get_item(item_id)
        self.view.update_menuitem(item_id, item)

    @binder("model.update_plugin_event")
    def update_plugin_on_model(self, msg):
        self.__log_recieve('update_plugin_on_model')

    def __log_recieve(self, listener_name):
        info_list = self.binder.get_info(listener_name)
        for info in info_list:
            obj = info['object_name']
            evt = info['event_name']
            cls = info['class_name']
            mes = 'Recieved {0} of {1}:{2} at {3}'
            Log( mes.format(evt, obj, cls, listener_name) )


def main():
    import wx
    logfile =  "_error.log"
    app = wx.App(redirect=False, filename=logfile)
    frame = wx.Frame(None, -1, "TestFrame")

    from menubar_view  import MenubarView
    from menubar_model import MenubarModel

    view = MenubarView(frame)
    model = MenubarModel()
    p = MenubarPresenter(model, view)
    model.init_event.fire()
    # frame.Bind(wx.EVT_MENU, view.on_menuitem)

    frame.SetMenuBar( view )
    frame.Show()

    try:
        app.MainLoop()
    except:
        app.RedirectStdio()

if __name__ == '__main__':
    main()
    pass



