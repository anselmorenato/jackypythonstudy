#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Biao Ma and Takakazu Ishikura

# standard modules
import os, sys
import wx

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from utils.event import NagaraEvent
from core.exception import NagaraException


from interfaces.ilocation_view import ILocationView
class LocationView(ILocationView, wx.Dialog):
    def __init__(self):
        # wx.Dialog.__init__(self, parent, id, title, size=(250, 210))
        wx.Dialog.__init__(self, None, -1, 
                           'Location Configure', size=(400, 400))

        # create config notebook
        self.__create_config_notebook()

        # create ok and cancel button
        btn_sizer = self.__create_buttons()

        # do layout
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.__config_nb , 1 , wx.EXPAND      , 5)
        main_sizer.Add(btn_sizer        , 0 , wx.ALIGN_RIGHT , 5)
        #main_sizer.Fit(self)
        self.SetSizer(main_sizer)
        

        # generate events
        self.__close_event  = NagaraEvent()
        self.__ok_event     = NagaraEvent()
        self.__cancel_event = NagaraEvent()
        self.__update_event = NagaraEvent()

    def __create_config_notebook(self):
        config_nb = wx.Notebook(
            self, -1, size=(21,21), style=wx.BK_DEFAULT)
        self.__config_nb = config_nb

        loc_page = LocationConfigPanel(self)
        ssh_page = SSHConfigPanel(self)
        cmd_page = CommandManagerPanel(self)
        jms_page = JMSManagerPanel(self)

        config_nb.AddPage(loc_page, "Location" ) 
        config_nb.AddPage(ssh_page, "ssh"      ) 
        config_nb.AddPage(cmd_page, "Command"  ) 
        config_nb.AddPage(jms_page, "JMS"      ) 

        #self.nb.SetSelection(min(selection,self.nb.GetPageCount()-1))
        # the selection must smaller than pagecount.
        self.CenterOnParent()
        self.SetMinSize((420,400))

        # bind
        return config_nb

    def __create_buttons(self):

        # create view
        ok_btn     = wx.Button(self , wx.ID_OK     , "Ok"     ) 
        cancel_btn = wx.Button(self , wx.ID_CANCEL , "Cancel" ) 

        # sizer
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add(ok_btn     , 0 , wx.ALIGN_RIGHT , 5 ) 
        btn_sizer.Add(cancel_btn , 0 , wx.ALIGN_RIGHT , 5 ) 

        # bind
        ok_btn.Bind(    wx.EVT_BUTTON , self.on_ok     ) 
        cancel_btn.Bind(wx.EVT_BUTTON , self.on_cancel ) 
        return btn_sizer

    def on_ok(self, event):
        self.ok_event.fire()

    def on_cancel(self, event):
        self.cancel_event.fire()

    def on_close(self, event):
        self.close_event.fire()

    def set_title(self, label):
        self.SetTitle(label + ' location configure')

    def get_notebook(self):
        return self.__config_nb

    # events
    @property
    def ok_event(self):
        return self.__ok_event

    @property
    def cancel_event(self):
        return self.__cancel_event

    @property
    def close_event(self):
        return self.__close_event

    @property
    def update_event(self):
        return self.__update_event

    # getset: name
    def get_name(self):
        loc_page = self.__config_nb.GetPage(0)
        return loc_page.name
    def set_name(self, name):
        loc_page = self.__config_nb.GetPage(0)
        loc_page.name = name
        self.set_title(name)
    name = property(get_name, set_name)

    # getset: workdir
    def get_workdir(self):
        loc_page = self.__config_nb.GetPage(0)
        return loc_page.workdir
    def set_workdir(self, workdir):
        loc_page = self.__config_nb.GetPage(0)
        loc_page.workdir = workdir
    workdir = property(get_workdir, set_workdir)

    # getset: shell
    def get_shell(self):
        loc_page = self.__config_nb.GetPage(0)
        return loc_page.shell
    def set_shell(self, shell):
        loc_page = self.__config_nb.GetPage(0)
        loc_page.shell = shell
    shell = property(get_shell, set_shell)

    # getset: init_file
    def get_init_file(self):
        loc_page = self.__config_nb.GetPage(0)
        return loc_page.init_file
    def set_init_file(self, init_file):
        loc_page = self.__config_nb.GetPage(0)
        loc_page.init_file = init_file
    init_file = property(get_init_file, set_init_file)

    # getset: mpi
    def get_mpi(self):
        loc_page = self.__config_nb.GetPage(0)
        return loc_page.mpi
    def set_mpi(self, mpi):
        loc_page = self.__config_nb.GetPage(0)
        loc_page.mpi = mpi
    mpi = property(get_mpi, set_mpi)

    def get_env_dict(self):
        loc_page = self.__config_nb.GetPage(0)
        return loc_page.env_dict
    def set_env_dict(self, env_dict):
        loc_page = self.__config_nb.GetPage(0)
        loc_page.env_dict = env_dict
    env_dict = property(get_env_dict, set_env_dict)

    # getset: ssh_address
    def get_ssh_address(self):
        ssh_page = self.__config_nb.GetPage(1)
        return ssh_page.address
    def set_ssh_address(self, address):
        ssh_page = self.__config_nb.GetPage(1)
        ssh_page.address = address
    ssh_address = property(get_ssh_address, set_ssh_address)

    # getset: ssh_username
    def get_ssh_username(self):
        ssh_page = self.__config_nb.GetPage(1)
        return ssh_page.username
    def set_ssh_username(self, username):
        ssh_page = self.__config_nb.GetPage(1)
        ssh_page.username = username
    ssh_username = property(get_ssh_username, set_ssh_username)

    # getset: ssh_password
    def get_ssh_password(self):
        ssh_page = self.__config_nb.GetPage(1)
        return ssh_page.password
    def set_ssh_password(self, password):
        ssh_page = self.__config_nb.GetPage(1)
        ssh_page.password = password
    ssh_password = property(get_ssh_password, set_ssh_password)

    # getset: ssh_port
    def get_ssh_port(self):
        ssh_page = self.__config_nb.GetPage(1)
        return ssh_page.port
    def set_ssh_port(self, port):
        ssh_page = self.__config_nb.GetPage(1)
        ssh_page.port = port
    ssh_port = property(get_ssh_port, set_ssh_port)

    # getset: command_dict
    def get_command_dict(self):
        cmd_page = self.__config_nb.GetPage(2)
        return cmd_page.command_dict
    def set_command_dict(self, cmd_dict):
        cmd_page = self.__config_nb.GetPage(2)
        cmd_page.command_dict = cmd_dict
    command_dict = property(get_command_dict, set_command_dict)

    # getset: jms_dict
    def get_jms_dict(self):
        jms_page = self.__config_nb.GetPage(3)
        return jms_page.jms_dict
    def set_jms_dict(self, jms_dict):
        jms_page = self.__config_nb.GetPage(3)
        jms_page.jms_dict = jms_dict
    jms_dict = property(get_jms_dict, set_jms_dict)

    # getset: jms_default
    def get_jms_default(self):
        jms_page = self.__config_nb.GetPage(3)
        return jms_page.jms_default
    def set_jms_default(self, jmsname):
        jms_page = self.__config_nb.GetPage(3)
        jms_page.jmsname = jmsname
    jms_default = property(get_jms_default, set_jms_default)

    # methods
    def show(self):
        self.ShowModal()

    def close(self):
        self.Close(True)

#===============================================================================
class LocationConfigPanel(wx.Panel):

    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent.get_notebook() ,-1)
        self.__parent = parent
        # create the controls
        form_sizer = self.__create_panel()
        self.__env_list = EnvironmentConfigPanel(self)

        # do layout
        # main_sizer = wx.StaticBoxSizer(
        #     wx.StaticBox(self, -1, 'Location General Setting'),
        #     orient=wx.VERTICAL)
        text = wx.StaticText(self, -1, 'General location setting')
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(text            , 0 , wx.ALIGN_CENTRE|wx.ALL , 5)
        main_sizer.Add(form_sizer      , 0 , wx.EXPAND|wx.ALL     , 5)
        main_sizer.Add(self.__env_list , 0 , wx.EXPAND|wx.ALL     , 5)
        self.SetSizer(main_sizer)

    def __create_panel(self):

        # view
        name_text     = wx.StaticText(self, -1, "Config Name:")
        name_form     = wx.TextCtrl(self, -1, "")
        workdir_text  = wx.StaticText(self, -1, "Working Directory:")
        workdir_form  = wx.TextCtrl(self, -1, "")
        shell_text    = wx.StaticText(self, -1, "Shell:")
        shell_form    = wx.TextCtrl(self, -1, "")
        initfile_text = wx.StaticText(self, -1, "Init File:")
        initfile_form = wx.TextCtrl(self, -1, "")
        mpi_text      = wx.StaticText(self, -1, "MPI Command:")
        mpi_form      = wx.TextCtrl(self, -1, "")

        self.__name     = name_form
        self.__workdir  = workdir_form
        self.__shell    = shell_form
        self.__initfile = initfile_form
        self.__mpi      = mpi_form

        # bind
        name_form.Bind(wx.EVT_TEXT, self.on_name_changed)

        # sizer
        form_sizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        form_sizer.Add(name_text     , 0 , wx.FIXED_MINSIZE )
        form_sizer.Add(name_form     , 0 , wx.EXPAND        )
        form_sizer.Add(workdir_text  , 0 , wx.FIXED_MINSIZE )
        form_sizer.Add(workdir_form  , 0 , wx.EXPAND        )
        form_sizer.Add(shell_text    , 0 , wx.FIXED_MINSIZE )
        form_sizer.Add(shell_form    , 0 , wx.EXPAND        )
        form_sizer.Add(initfile_text , 0 , wx.FIXED_MINSIZE )
        form_sizer.Add(initfile_form , 0 , wx.EXPAND        )
        form_sizer.Add(mpi_text      , 0 , wx.FIXED_MINSIZE )
        form_sizer.Add(mpi_form      , 0 , wx.EXPAND        )
        #fsizer.AddGrowableRow(1)
        form_sizer.AddGrowableCol(1)
        return form_sizer

    def on_name_changed(self, event):
        name = self.__name.GetValue()
        self.__parent.set_title(name)

    # getset name 
    def get_name(self):
        return self.__name.GetValue()
    def set_name(self, name):
        self.__name.SetValue(name)
    name = property(get_name, set_name)

    # getset workdir 
    def get_workdir(self):
        return self.__workdir.GetValue()
    def set_workdir(self, workdir):
        self.__workdir.SetValue(workdir)
    workdir = property(get_workdir, set_workdir)

    # getset shell 
    def get_shell(self):
        return self.__workdir.GetValue()
    def set_shell(self, shell):
        self.__workdir.SetValue(shell)
    shell = property(get_shell, set_shell)

    # getset initfile 
    def get_initfile(self):
        return self.__initfile.GetValue()
    def set_initfile(self, initfile):
        self.__initfile.SetValue(initfile)
    initfile = property(get_initfile, set_initfile)

    # getset mpi 
    def get_mpi(self):
        return self.__mpi.GetValue()
    def set_mpi(self, mpi):
        self.__mpi.SetValue(mpi)
    mpi = property(get_mpi, set_mpi)

    # getset env_dict
    def get_env_dict(self):
        return self.__env_list.env_dict
    def set_env_dict(self, env_dict):
        self.__env_list.env_dict = env_dict
    env_dict = property(get_env_dict, set_env_dict)

#===============================================================================
class SSHConfigPanel(wx.Panel):

    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent.get_notebook(), -1)

        # create forms
        form_sizer = self.__create_forms()

        # sizer
        # main_sizer = wx.StaticBoxSizer(
        #     wx.StaticBox(self, -1, 'Ssh Setting'), orient=wx.VERTICAL)
        text = wx.StaticText(self, -1, 'SSH Setting')
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(text       , 0 , wx.ALIGN_CENTRE|wx.ALL , 5)
        main_sizer.Add(form_sizer , 0 , wx.EXPAND|wx.ALL       , 5)
        main_sizer.Fit(self)
        self.SetSizer(main_sizer)

    def __create_forms(self):
        
        # controls
        host_text = wx.StaticText(self , -1 , "Host:")
        host_form = wx.TextCtrl(self   , -1 , "")
        user_text = wx.StaticText(self , -1 , "User:")
        user_form = wx.TextCtrl(self   , -1 , "")
        pass_text = wx.StaticText(self , -1 , "Password:")
        pass_form = wx.TextCtrl(self   , -1 , "", style=wx.PASSWORD)
        port_text = wx.StaticText(self , -1 , "Port:")
        port_form = wx.TextCtrl(self   , -1 , "")

        self.__host = host_form
        self.__user = user_form
        self.__pass = pass_form
        self.__port = port_form

        # bind
        # host_form.Bind(wx.EVT_KILL_FOCUS, self.on_unfocus)

        # sizer
        form_sizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        form_sizer.AddGrowableCol(1)
        form_sizer.Add(host_text , 0 , wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(host_form , 0 , wx.EXPAND)
        form_sizer.Add(user_text , 0 , wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(user_form , 0 , wx.EXPAND)
        form_sizer.Add(pass_text , 0 , wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(pass_form , 0 , wx.EXPAND)
        form_sizer.Add(port_text , 0 , wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(port_form , 0 , wx.EXPAND)
        return form_sizer

    # getset: address
    def get_address(self):
        return self.__host.GetValue()
    def set_address(self, address):
        self.__host.SetValue(address)
    address = property(get_address, set_address)

    # getset password
    def get_password(self):
        return self.__pass.GetValue()
    def set_password(self, password):
        self.__pass.SetValue(password)
    password = property(get_password, set_password)

    # getset port
    def get_port(self):
        try:
            ret = int(self.__port.GetValue())
        except ValueError:
            ret = 22
        return ret 
    def set_port(self, port):
        self.__port.SetValue( str(port) )
    port = property(get_port, set_port)

    # getset username
    def get_username(self):
        return self.__user.GetValue()
    def set_username(self, username):
        self.__user.SetValue(username)
    username = property(get_username, set_username)


#===============================================================================
class CommandManagerPanel(wx.Panel):

    """this is the panel of command setting """

    def __init__(self, parent):
        if hasattr(parent, 'get_notebook'):
            wx.Panel.__init__(self, parent.get_notebook())
        else:
            wx.Panel.__init__(self, parent)

        # create the tab edit buttons
        btn_sizer = self.__create_buttons()
        
        # create the forms
        self.__cmd_nb = self.__create_command_notebook()

        # main sizer
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(btn_sizer     , 0 , wx.ALIGN_RIGHT , 5)
        main_sizer.Add(self.__cmd_nb , 1 , wx.EXPAND      , 5)
        self.SetSizer(main_sizer)
        main_sizer.Fit(self)

    def __create_buttons(self):
        # make buttons
        append_btn = wx.BitmapButton(self, -1, size=(24,24))
        delete_btn = wx.BitmapButton(self, -1, size=(24,24))

        # bind
        append_btn.Bind( wx.EVT_BUTTON , self.on_append ) 
        delete_btn.Bind( wx.EVT_BUTTON , self.on_delete ) 

        # sizer
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add( append_btn , 0 , wx.EXPAND, 5 ) 
        btn_sizer.Add( delete_btn , 0 , wx.EXPAND, 5 ) 
        return btn_sizer

    def __create_command_notebook(self):
        cmd_notebook = wx.Notebook(
            self, -1, size=wx.DefaultSize, style=wx.BK_DEFAULT)
        return cmd_notebook

    def set_label_to_tab(self, label):
        sel = self.__cmd_nb.GetSelection()
        if sel >= 0:
            self.__cmd_nb.SetPageText(sel, label)

    def get_notebook(self):
        return self.__cmd_nb

    def get_command_dict(self):
        npage = self.__cmd_nb.GetPageCount()
        command_dict = {}
        for ipage in range(npage):
            page = self.__cmd_nb.GetPage(ipage)
            command_dict[page.name] = {}
            command_dict[page.name]['name']   = page.name
            command_dict[page.name]['path']   = page.path
            command_dict[page.name]['envs']   = page.envs
            command_dict[page.name]['enable'] = page.enable
        return command_dict

    def set_command_dict(self, command_dict):
        for cmd_name, cmd_config in command_dict.items():
            page = CommandConfigPanel(self)
            self.__cmd_nb.AddPage(page, cmd_name)
            page.name   = cmd_name
            page.path   = cmd_config['path']
            page.envs   = cmd_config['envs']
            page.enable = cmd_config['enable']

    command_dict = property(get_command_dict, set_command_dict)

    def on_append(self, event):
        cmd_panel = CommandConfigPanel(self)
        cmd_panel.enable = True
        self.__cmd_nb.AddPage(cmd_panel, 'command name')
        npage = self.__cmd_nb.GetPageCount()
        self.__cmd_nb.SetSelection( npage-1 )
        cmd_panel.name = 'command name'

    def on_delete(self, event):

        npage = self.__cmd_nb.GetPageCount()
        if npage >= 2:
            sel = self.__cmd_nb.GetSelection()

            dlg  = wx.MessageDialog(
                self,'Do you real want to remove this page?','The Page Remove',
                style = wx.OK|wx.CANCEL|wx.ICON_WARNING
            )

            answer = dlg.ShowModal()
            if answer == wx.ID_OK:
                page = self.__cmd_nb.GetPage(sel)
                self.__cmd_nb.RemovePage(sel)
                del page

        else:
            dlg  = wx.MessageDialog(
                self,'Because only one page,you can not remove this page!',
                'Error', style = wx.OK|wx.ICON_WARNING
            )
            dlg.ShowModal()
            dlg.Destroy()


#===============================================================================
class CommandConfigPanel(wx.Panel):
    """"""

    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent.get_notebook())
        self.__parent = parent

        # create view
        form_sizer = self.__create_forms()

        # sizer = wx.BoxSizer(wx.VERTICAL)
        # sizer.Add(
        self.__env_list = EnvironmentConfigPanel(self)

        # sizer
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(form_sizer      , 0 , wx.EXPAND|wx.ALL , 5)
        main_sizer.Add(self.__env_list , 0 , wx.EXPAND|wx.ALL , 5)
        self.SetSizer(main_sizer)
        # main_sizer.Fit(self)

    def __create_forms(self):
        # create view
        enable_check = wx.CheckBox(self, -1, "use this setting", (20, 10))
        name_text    = wx.StaticText(self, -1, "Name:")
        name_form    = wx.TextCtrl(self, -1, "")
        path_text    = wx.StaticText(self, -1, "Path:")
        path_form    = wx.TextCtrl(self, -1, "")
        self.__name      = name_form
        self.__name_text = name_text
        self.__path      = path_form
        self.__path_text = path_text
        self.__enable    = enable_check

        # bind
        name_form.Bind(wx.EVT_TEXT        , self.on_name_changed)
        enable_check.Bind(wx.EVT_CHECKBOX , self.on_enable_changed)

        # sizer
        form_sizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        form_sizer.AddGrowableCol(0)
        form_sizer.AddGrowableCol(1)
        form_sizer.Add(wx.StaticText(self, -1, ''), 1, wx.EXPAND)
        form_sizer.Add(enable_check,3, wx.ALIGN_LEFT)
        form_sizer.Add(name_text , 1 , wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(name_form , 3 , wx.EXPAND)
        form_sizer.Add(path_text , 1 , wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(path_form , 3 , wx.EXPAND)

        return form_sizer

    def on_name_changed(self, event):
        """This method is set the pagetext."""
        name = self.__name.GetValue()
        if len(self.__name.GetValue().strip()) >= 1:
            self.__parent.set_label_to_tab(name)

    def on_enable_changed(self, event):
        enable_check = event.GetEventObject()
        enable = enable_check.IsChecked()
        self.change_enable(enable)

    def change_enable(self, enable):
        self.__name.Enable(enable)
        self.__path.Enable(enable)
        self.__name_text.Enable(enable)
        self.__path_text.Enable(enable)
        self.__env_list.enable(enable)


    # getset name
    def get_name(self):
        return self.__name.GetValue()
    def set_name(self, name):
        self.__name.SetValue(name)
    name = property(get_name, set_name)

    # getset path
    def get_path(self):
        return self.__path.GetValue()
    def set_path(self, path):
        self.__path.SetValue(path)
    path = property(get_path, set_path)

    # getset enable
    def get_enable(self):
        return self.__enable.GetValue()
    def set_enable(self, enable):
        self.__enable.SetValue(enable)
        self.change_enable(enable)
    enable = property(get_enable, set_enable)

    # getset envs
    def get_envs(self):
        return self.__env_list.env_dict
    def set_envs(self, env_dict):
        self.__env_list.env_dict = env_dict
    envs = property(get_envs, set_envs)


#===============================================================================
class JMSManagerPanel(wx.Panel):

    """this is the panel of JMS setting """

    def __init__(self, parent):
        wx.Panel.__init__(self, parent.get_notebook())

        # create choice control for jms
        choice_sizer = self.__create_choice()

        # create the tab edit buttons
        btn_sizer = self.__create_buttons()
        
        # create the forms
        self.__jms_nb = self.__create_jms_notebook()

        # main sizer
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(choice_sizer  , 0 , wx.EXPAND      , 5)
        main_sizer.Add(btn_sizer     , 0 , wx.ALIGN_RIGHT , 5)
        main_sizer.Add(self.__jms_nb , 1 , wx.EXPAND      , 5)
        self.SetSizer(main_sizer)
        main_sizer.Fit(self)

    def __create_choice(self):
        text = wx.StaticText(self, -1, 'default: ')
        self.__choice = wx.Choice(self, -1, choices=[])

        # sizer
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(text, 0, wx.ALIGN_LEFT, 5)
        sizer.Add(self.__choice, 0, wx.ALIGN_LEFT, 5)
        return sizer

    def __create_buttons(self):
        # make buttons
        append_btn = wx.BitmapButton(self, -1, size=(24,24))
        delete_btn = wx.BitmapButton(self, -1, size=(24,24))

        # bind
        append_btn.Bind( wx.EVT_BUTTON , self.on_append ) 
        delete_btn.Bind( wx.EVT_BUTTON , self.on_delete ) 

        # sizer
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add( append_btn , 0 , wx.EXPAND, 5 ) 
        btn_sizer.Add( delete_btn , 0 , wx.EXPAND, 5 ) 
        return btn_sizer

    def __create_jms_notebook(self):
        jms_notebook = wx.Notebook(
            self, -1, size=wx.DefaultSize, style=wx.BK_DEFAULT)
        return jms_notebook

    def set_label_to_tab(self, label):
        sel = self.__jms_nb.GetSelection()
        if sel >= 0:
            self.__jms_nb.SetPageText(sel, label)
            if len(self.__choice.GetItems()) != 0:
                self.__choice.SetString(sel, label)

    def set_label_to_tab_for_init(self, label):
        sel = self.__jms_nb.GetPageCount()
        self.__jms_nb.SetPageText(sel-1, label)
        # if sel >= 0:
            # if len(self.__choice.GetItems()) != 0:
                # self.__choice.SetString(sel, label)

    def get_notebook(self):
        return self.__jms_nb

    def get_jms_dict(self):
        npage = self.__jms_nb.GetPageCount()
        jms_dict = {}
        for ipage in range(npage):
            page = self.__jms_nb.GetPage(ipage)
            jms_dict[page.name] = {}
            jms_dict[page.name]['name']   = page.name
            jms_dict[page.name]['path']   = page.path
            jms_dict[page.name]['envs']   = page.envs
            jms_dict[page.name]['enable'] = page.enable
        return jms_dict

    def set_jms_dict(self, jms_dict):
        for jms_name, jms_config in jms_dict.items():
            page = JMSConfigPanel(self)
            self.__jms_nb.AddPage(page, jms_name)
            page.name   = jms_name
            page.path   = jms_config['path']
            page.envs   = jms_config['envs']
            page.enable = jms_config['enable']
        self.update_choice()
    jms_dict = property(get_jms_dict, set_jms_dict)

    def get_jms_default(self):
        return self.__choice.GetStringSelection()
    def set_jms_default(self, jmsname):
        self.__choice.SetStringSelection( jmsname )
    jms_default = property(get_jms_default, set_jms_default)

    def update_choice(self):
        njmspage = self.__jms_nb.GetPageCount()
        for i in range(njmspage):
            page = self.__jms_nb.GetPage(i)
            self.__choice.Append( page.name )

    def on_append(self, event):
        jms_panel = JMSConfigPanel(self)

        self.__jms_nb.AddPage(jms_panel, 'jms name')
        npage = self.__jms_nb.GetPageCount()
        self.__jms_nb.SetSelection( npage-1 )
        
        # jmsname = self.__choice.GetStringSelection()
        self.__choice.Append('jms name')
        jms_panel.enable = True
        jms_panel.name = 'jms name'

    def on_delete(self, event):

        npage = self.__jms_nb.GetPageCount()
        if npage >= 2:
            sel = self.__jms_nb.GetSelection()

            dlg  = wx.MessageDialog(
                self,'Do you real want to remove this page?','The Page Remove',
                style = wx.OK|wx.CANCEL|wx.ICON_WARNING
            )

            answer = dlg.ShowModal()
            if answer == wx.ID_OK:
                page = self.__jms_nb.GetPage(sel)
                self.__jms_nb.RemovePage(sel)
                self.update_choice()
                del page

        else:
            dlg  = wx.MessageDialog(
                self,'Because only one page,you can not remove this page!',
                'Error', style = wx.OK|wx.ICON_WARNING
            )
            dlg.ShowModal()
            dlg.Destroy()


#===============================================================================
class JMSConfigPanel(wx.Panel):
    """"""

    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent.get_notebook())
        self.__parent = parent

        # create view
        form_sizer = self.__create_forms()

        # sizer = wx.BoxSizer(wx.VERTICAL)
        # sizer.Add(
        self.__env_list = EnvironmentConfigPanel(self)

        # sizer
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(form_sizer      , 0 , wx.EXPAND|wx.ALL , 5)
        main_sizer.Add(self.__env_list , 0 , wx.EXPAND|wx.ALL , 5)
        self.SetSizer(main_sizer)
        # main_sizer.Fit(self)

    def __create_forms(self):
        # create view
        enable_check = wx.CheckBox(self, -1, "use this setting", (20, 10))
        name_text    = wx.StaticText(self, -1, "Name:")
        name_form    = wx.TextCtrl(self, -1, "")
        path_text    = wx.StaticText(self, -1, "Path:")
        path_form    = wx.TextCtrl(self, -1, "")
        self.__name      = name_form
        self.__name_text = name_text
        self.__path      = path_form
        self.__path_text = path_text
        self.__enable    = enable_check

        # bind
        name_form.Bind(wx.EVT_TEXT        , self.on_name_changed)
        enable_check.Bind(wx.EVT_CHECKBOX , self.on_enable_changed)

        # sizer
        form_sizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        form_sizer.AddGrowableCol(0)
        form_sizer.AddGrowableCol(1)
        form_sizer.Add(wx.StaticText(self, -1, ''), 1, wx.EXPAND)
        form_sizer.Add(enable_check,3, wx.ALIGN_LEFT)
        form_sizer.Add(name_text , 1 , wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(name_form , 3 , wx.EXPAND)
        form_sizer.Add(path_text , 1 , wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(path_form , 3 , wx.EXPAND)

        return form_sizer

    def on_name_changed(self, event):
        """This method is set the pagetext."""
        name = self.__name.GetValue()
        if len(self.__name.GetValue().strip()) >= 1:
            self.__parent.set_label_to_tab(name)

    def on_enable_changed(self, event):
        enable_check = event.GetEventObject()
        enable = enable_check.IsChecked()
        self.change_enable(enable)

    def change_enable(self, enable):
        self.__name.Enable(enable)
        self.__path.Enable(enable)
        self.__name_text.Enable(enable)
        self.__path_text.Enable(enable)
        self.__env_list.enable(enable)


    # getset name
    def get_name(self):
        return self.__name.GetValue()
    def set_name(self, name):
        self.__name.SetValue(name)
        self.__parent.set_label_to_tab_for_init(name)
    name = property(get_name, set_name)

    # getset path
    def get_path(self):
        return self.__path.GetValue()
    def set_path(self, path):
        if path:
            self.__path.SetValue(path)
        else:
            self.__path.SetValue('')
    path = property(get_path, set_path)

    # getset enable
    def get_enable(self):
        return self.__enable.GetValue()
    def set_enable(self, enable):
        self.__enable.SetValue(enable)
        self.change_enable(enable)
    enable = property(get_enable, set_enable)

    # getset envs
    def get_envs(self):
        return self.__env_list.env_dict
    def set_envs(self, env_dict):
        self.__env_list.env_dict = env_dict
    envs = property(get_envs, set_envs)


#===============================================================================
class EnvironmentConfigPanel(wx.Panel):
    """"""

    def __init__(self,parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)

        # make environment list
        self.__env_list, list_sizer = self.__create_env_list()

        # make edit buttons
        btn_sizer = self.__create_buttons()
        
        # do layout
        text = wx.StaticText(self, -1, 'Environment')
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(text       , 0 , wx.ALIGN_LEFT|wx.ALL , 3)
        main_sizer.Add(list_sizer , 1 , wx.EXPAND|wx.ALL     , 5)
        main_sizer.Add(btn_sizer  , 0 , wx.ALIGN_LEFT|wx.ALL , 2)
        self.SetSizer(main_sizer)
        main_sizer.Fit(self)

    def __create_env_list(self):
        # create view
        env_list = wx.ListCtrl(self , -1 , style = wx.LC_REPORT)
        env_list.InsertColumn(0 , 'Variable' , width = 150) 
        env_list.InsertColumn(1 , 'Value'    , width = 200) 
        # env_list.SetColumnWidth(0, -1)
        # env_list.SetColumnWidth(1, -1)

        # bind
        #self.__env_list.Bind

        # sizer
        listsizer = wx.BoxSizer(wx.HORIZONTAL)
        listsizer.Add(env_list, 1, wx.EXPAND)
        return env_list, listsizer

    def __create_buttons(self):
        # make buttons
        append_btn = wx.BitmapButton(self, -1, size=(24,24))
        delete_btn = wx.BitmapButton(self, -1, size=(24,24))
        edit_btn   = wx.BitmapButton(self, -1, size=(24,24))
        # append_btn = wx.Button(self, -1, '+', size=(36,36))
        # delete_btn = wx.Button(self, -1, '-', size=(36,36))
        # edit_btn   = wx.Button(self, -1, 'E', size=(36,36))

        # sizer
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add( append_btn , 0 , wx.EXPAND     , 5 ) 
        btn_sizer.Add( delete_btn , 0 , wx.EXPAND     , 5 ) 
        btn_sizer.Add( edit_btn   , 0 , wx.ALIGN_LEFT , 5 ) 

        # bind
        self.Bind( wx.EVT_BUTTON , self.on_append , append_btn ) 
        self.Bind( wx.EVT_BUTTON , self.on_delete , delete_btn ) 
        self.Bind( wx.EVT_BUTTON , self.on_edit   , edit_btn   ) 

        return btn_sizer

    def on_append(self, event):
        pos = event.GetEventObject().GetScreenPosition()
        nitem = self.__env_list.GetItemCount()
        with EnvEditorDialog(pos=pos) as dlg:
            key, val = dlg.get_env()
            self.__env_list.InsertStringItem(nitem, key)
            self.__env_list.SetStringItem(nitem, 1, val)

    def on_delete(self, event):
        index = self.__env_list.GetFirstSelected()
        if index != -1:
            self.__env_list.DeleteItem(index)

    def on_edit(self, event):
        index = self.__env_list.GetFirstSelected()
        if index != -1:
            key_item = self.__env_list.GetItem(index, 0)
            val_item = self.__env_list.GetItem(index, 1)
            key_value = key_item.GetText()
            val_value = val_item.GetText()
            pos = event.GetEventObject().GetScreenPosition()

            with EnvEditorDialog(key=key_value, val=val_value, pos=pos) as dlg:
                key, val = dlg.get_env()
                self.__env_list.SetStringItem(index, 0, key)
                self.__env_list.SetStringItem(index, 1, val)

    def enable(self, enable):
        self.Enable(enable)

    # getset envs
    def get_envs(self):
        nitem = self.__env_list.GetItemCount()
        env_dict = {}
        for i in range(nitem):
            key_item = self.__env_list.GetItem(i, 0)
            val_item = self.__env_list.GetItem(i, 1)
            env_dict[key_item.GetText()] = val_item.GetText()
        return env_dict

    def set_envs(self, env_dict):
        if env_dict:
            index = 0
            for key, val in env_dict.items():
                self.__env_list.InsertStringItem(index, key)
                self.__env_list.SetStringItem(index, 1, str(val))
                index += 1

    env_dict = property(get_envs, set_envs)


########################################################################
class DialogCancelException(NagaraException): pass
class EnvEditorDialog(wx.Dialog):

    #----------------------------------------------------------------------
    def __init__(self, key='', val='', pos=(100,100)):
        wx.Dialog.__init__(self, None, -1, pos=pos, size=(300,107))

        # create form
        self.__key_form, self.__val_form, form_sizer = self.__create_forms()
        self.__key_form.SetValue( str(key) )
        self.__val_form.SetValue( str(val) )

        # create buttons
        btn_sizer = self.__create_buttons()

        # do layout
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(form_sizer , 0 , wx.EXPAND|wx.ALL , 5 ) 
        main_sizer.Add(btn_sizer  , 0 , wx.ALIGN_RIGHT   , 5 ) 
        self.SetSizer(main_sizer)
        self.SetAutoLayout(True)

    def __create_forms(self):
        # create view
        key_label = wx.StaticText(self, -1, "Variable:")
        key_form  = wx.TextCtrl(self, -1, "")
        val_label = wx.StaticText(self, -1, "Value:")
        val_form  = wx.TextCtrl(self, -1, "")

        # sizer
        #form_sizer = wx.StaticBoxSizer(
            #wx.StaticBox(self, -1, 'Environment Setting'), orient=wx.VERTICAL)
        form_sizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        form_sizer.Add(key_label, 1, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(key_form , 0, wx.EXPAND)
        form_sizer.Add(val_label, 1, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(val_form , 0, wx.EXPAND)
        #fsizer.AddGrowableRow(1)
        form_sizer.AddGrowableCol(1)
        form_sizer.AddGrowableCol(2)

        return key_form, val_form, form_sizer

    def __create_buttons(self):

        # create view
        ok_btn     = wx.Button(self , wx.ID_OK     , "Ok"     ) 
        cancel_btn = wx.Button(self , wx.ID_CANCEL , "Cancel" ) 

        # sizer
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add(ok_btn     , 0 , wx.ALIGN_RIGHT , 5 ) 
        btn_sizer.Add(cancel_btn , 0 , wx.ALIGN_RIGHT , 5 ) 

        # bind
        # ok_btn.Bind(    wx.EVT_BUTTON , self.on_ok     ) 
        # cancel_btn.Bind(wx.EVT_BUTTON , self.on_cancel ) 
        return btn_sizer

    def __enter__(self):
        self.__flag = self.ShowModal()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.Destroy()
        return True

    def get_env(self):
        if self.__flag == wx.ID_CANCEL:
            raise DialogCancelException()
        key = self.__key_form.GetValue()
        val = self.__val_form.GetValue()
        return key, val
        

def main():
    from core.config  import Config
    loc_config = Config().get_common()['location']['hpcs']


    app = wx.App()
    frame = wx.Frame(None, -1, 'test frame')
    view = LocationView(frame)
    frame.Show()
    app.MainLoop()



if __name__ == '__main__':
    from core.config  import Config
    loc_config = Config().get_common()['location']['hpcs']


    def on_dialog(event):
        lv = LocationView()

        lv.name = loc_config['name']
        lv.env_dict = loc_config['envs']
        lv.command_dict = loc_config['commands']

        jms_config = loc_config['jms']
        jms_config.pop('default')

        print jms_config

        lv.jms_dict = loc_config['jms']
        # for key, value in loc_config['commands'].items():
            # if isinstance(value, dict):
                # for k, v in value.items():
                    # print '   '+ k + ': ', v
            # else:
                # print key + ': ', value

        # print '*'*50
        # for key, value in lv.command_dict.items():
            # if isinstance(value, dict):
                # for k, v in value.items():
                    # print '   '+ k + ': ', v
            # else:
                # print key + ': ', value


        
        lv.show()
        # with EnvEditorDialog() as dlg:
            # print dlg.get_env()


    app = wx.App()
    frame = wx.Frame(None, -1, 'test frame')
    panel = wx.Panel(frame)
    btn = wx.Button(panel, -1, 'run dialog')
    btn.Bind(wx.EVT_BUTTON, on_dialog)
    frame.Show()
    app.MainLoop()
