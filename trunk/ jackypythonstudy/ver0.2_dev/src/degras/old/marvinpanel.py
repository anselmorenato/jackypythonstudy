#! /usr/bin/env python
# _*_ coding: utf-8 _*_
# Copyright (C)  2009 Takakazu Ishikura

from __future__ import with_statement 
import os, sys
import wx
import wx.xrc as xrc
import marvin

from marvinview_xrc import xrcMarvinView, get_resources

#-------------------------------------------------------------------------------

class MarvinPanel(xrcMarvinView):
    def __init__(self, parent, id, name, log=None):
        xrcMarvinView.__init__(self, parent)
        self.__log = log
        self.name = name
        self.__cache = {}
        self.__ctrls = {}
        self.__input  = None
        self.__output = None


        # self.initView(parent)
        self.initSettings()
        self.initBind()

    def initView(self):
        # get_resources().AttachUnknownControl('id', ctrl, self)
        # self.Fit()
        pass

    def initSettings(self):

        # initialize
        input = marvin.Marvin.inputs
        output = marvin.Marvin.outputs
        self.__cache = marvin.Marvin.opts_default
        self.__ctrls = {}
        self.__input  = self.__cache['ip_crd_file']
        self.__output = self.__cache['op_crd_file']

        # input and output coordinate
        self.__ctrl_input  = xrc.XRCCTRL(self, 'ip_crd_file')
        self.__ctrl_output = xrc.XRCCTRL(self, 'op_crd_file')

        # settings
        self.__ctrls['restart']    = xrc.XRCCTRL(self, 'restart')
        self.__ctrls['ref_temp']   = xrc.XRCCTRL(self, 'ref_temp')
        self.__ctrls['step_size']  = xrc.XRCCTRL(self, 'step_size')
        self.__ctrls['numstep']    = xrc.XRCCTRL(self, 'numstep')
        self.__ctrls['print_freq'] = xrc.XRCCTRL(self, 'print_freq')
        self.__ctrls['print_info'] = xrc.XRCCTRL(self, 'print_info')
        self.__ctrls['res_mass']   = xrc.XRCCTRL(self, 'res_mass')

        self.showSettings()
        
        # other ctrls
        self.__ctrl_usefile  = xrc.XRCCTRL(self, 'use_file')
        self.__ctrl_usedata = xrc.XRCCTRL(self, 'use_data')

    def initBind(self):
        self.bindButton(self.onRunMarvin, 'run_marvin')
        self.Bind(wx.EVT_RADIOBUTTON, self.onToggleInput, self.__ctrl_usefile)
        self.Bind(wx.EVT_RADIOBUTTON, self.onToggleInput, self.__ctrl_usedata)

        btn = xrc.XRCCTRL(self, 'show_output')
        self.Bind(wx.EVT_BUTTON, self.onShowOutput, btn)

    def log(self, message):
        if self.__log: self.__log.write(message)

    def showSettings(self):
        """Show the settings."""
        for key, ctrl in self.__ctrls.items():
            ctrl.SetValue( self.__cache[key] )

        self.__ctrl_input.SetPath( self.__input )
        self.__ctrl_output.SetPath( self.__output)

    def saveSettings(self):
        """Save the configs to cache."""
        for key, ctrl in self.__ctrls.items():
            self.__cache[key] = ctrl.GetValue()

        self.__input  = self.__ctrl_input.GetPath()
        self.__output = self.__ctrl_output.GetPath()
        if __debug__:
            print self.__input
            print self.__output

    def getSettings(self):
        """Return the marvin settings."""
        self.saveSettings()
        return self.__cache

    def getSettingsIO(self):
        """Return the marvin input and output."""
        self.saveSettings()
        return self.__input, self.__output

    # try code
    def get_channel(self, conn):
        self.conn = conn

    def bindButton(self, function, xrc_id):
        self.Bind(wx.EVT_BUTTON, function, id=xrc.XRCID(xrc_id))

    def onRunMarvin(self, event):
        self.saveSettings()

        # local nagara root
        nagara_root = 'C:\\Home_Ishikura\\docs\\Nagara-ishikura\\test-projects'

        recos = {}
        # check the remote configs and connection
        if not recos:
            # setting connection
            import configremote
            with configremote.ConfigRemote(self) as dlg:
                recos = dlg.getConfigs()

        if not recos: return False

        # configs
        remote_configs = dict(
            local = dict(
                ssh = {},
                rootdir = 'C:\path\to\nagara-root',
                workdir = '',
                jms = ['Single', 'MultiProcess'],
                commands = {},
            ),
            hpcs = dict(
                ssh = dict(
                    address = '133.66.117.139',
                    user = 'ishikura',
                    passwd = '*********',
                    port = 22,
                ),
                rootdir = '/home/ishikura/Nagara/projects',
                workdir = '/home/ishikura/Nagara/projects',
                # jms = ['Single', 'MPI', 'LSF'], #Local
                jms = dict(
                    Single = dict(
                        envs = {},
                        path = {},
                    ),
                    MPI = dict(
                        envs = {},
                        path = {},
                    ),
                    LSF = dict(
                        envs = {},
                        path = {},
                        script = {},
                    ),
                ),
                commands = dict(
                    amber = dict(
                        envs = dict(AMBERHOME='/home/hpc/ceid-opt/amber10.eth'),
                        path = '/home/hpc/ceid-opt/amber10.eth/exe/sander.MPI',
                    ),
                    marvin = dict(
                        envs = {},
                        # path = '/home/hpcs/Nagara/app/bin/marvin',
                        path = '/home/hpc/ceid-opt/bin/marvin',
                    ),
                    paics = dict(
                        # envs = dict(PAICS_HOME='/home/ishi/paics/paics-20081214'),
                        # path = '/home/ishi/paics/paics-20081214/main.exe',
                        envs = dict(PAICS_HOME='/home/ishi/paics/paics-20081214'),
                        path = '/home/ishi/paics/paics-20081214/main.exe',
                    ),
                ),
            ),
            vlsn = dict(),
            rccs = dict(),
        )

        try:
            c = wx.GetApp().getConfigs()
            remote_configs['hpcs']['rootdir'] = c['remote_root']
            print 
        except AttributeError:
            pass

        # add code checking the connection later
        # import connection
        # conn = connection.Connection(
        #     remote_configs['host'], remote_configs['passwd']
        # )
        # t.setConnection(conn)

        import project
        try:
            proj = wx.GetApp().getCurPrj()
        except AttributeError:
            proj = project.Project(root=nagara_root, name='test proj')

        task = project.Task(
            proj, configs=remote_configs,
            name='marvin-test', host='hpcs',log=self.__log
        )
        proj.appendTask(task)
        self.log('set marvin task\n')

        # job manager system
        import jms
        # LSF
        # task.setJMS(jms.LSF())
        # Single
        task.setJMS('Single')
        self.log('set job system manager: Single\n')

        import marvin
        cmd = marvin.Marvin(task, log=self.__log)
        print "aaaaaa", self.__cache['ip_crd_file']
        cmd.setSettings(self.__cache)
        cmd.setInputByFiles(ip_crd_file=self.__input)
        self.log('create the marvin task object.\n')


        import connection
        conn = connection.Connection(
            username=recos['user'], host=recos['host'], password=recos['passwd']
        )
        task.setConnection(conn)
        self.log('connect the channel to remote host\n')

        if not task.remote.isNone():
            task.delete()
            self.log('cleaned task: ' + task.getName() + '\n')

        task.setCommand(cmd)
        task.setupLocal()
        self.log('setup marvin job in local task directory\n')

        # print task.getConnection().exist(remote_path)
        task.setupRemote()
        self.log('setup remote job directory\n')

        # run
        self.log('running marvin job on remote host\n')
        task.run()

        # done
        self.log('done the calculation\n')

        # get output
        self.task = task

    def onToggleInput(self, event):
        btn = event.GetEventObject()
        if btn == self.__ctrl_usefile:
            self.__ctrl_input.Enable()
            text = xrc.XRCCTRL(self, 'ip_crd_file_text')
            text.Enable()
        else:
            self.__ctrl_input.Disable()
            text = xrc.XRCCTRL(self, 'ip_crd_file_text')
            text.Disable()

    def onShowOutput(self, event):
        import outputview
        dlg = outputview.OutputDlg()
        rpath = self.task.remote.getPath()
        remote_output_fn = rpath + '/' + 'output.xyz'
        lpath = self.task.local.getPath()
        local_output_fn = os.path.join(lpath, 'output.xyz')

        self.task.getConnection().get(remote_output_fn, local_output_fn)
        self.task.getConnection().close()

        local_file = open(local_output_fn, 'r')

        dlg.write(local_file.read())
        local_file.close()
        dlg.show()
        return True


#-------------------------------------------------------------------------------

class Config(wx.Dialog):

    def __init__(self, parent, title='Global configure'):
        wx.Dialog.__init__(self, parent, -1, title=title, size=(350,400))

        # self.nb = wx.Notebook(self, -1, style=wx.NB_TOP)

        # self.cg = ConfigGlobal(self.nb, -1)
        # self.cg = wx.Panel(self.nb, -1, 'Global configure')
        # self.nb.AddPage(self.cg, 'Global configure')

        import configremote as cr
        self.cr = cr.ConfigRemote(self)
        # self.nb.AddPage(self.cr, 'Remote configure')

#-------------------------------------------------------------------------------

def main():
    import nagaratest
    app = nagaratest.FrameTest()
    log = app.log
    frame = app.frame

    dlg = wx.Dialog(None, -1, title='Marvin Dialog', size=(562, 500))
    # paicspanel.MarvinPanel(dlg, -1, 'marvin', log=self.getLog())
    MarvinPanel(dlg, -1, 'marvin', log=log)
    dlg.ShowModal()
    dlg.Destroy()

    app.MainLoop()

    # try:
    #     app.MainLoop()
    # except:
    #     app.RedirectStdio()

if __name__ == '__main__':
    main()
    module = __file__.split('.')[0]

