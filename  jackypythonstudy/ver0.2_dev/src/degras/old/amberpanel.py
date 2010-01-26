#! /usr/bin/env python
# _*_ coding: utf-8 _*_
# Copyright (C)  2009 Takakazu Ishikura

from __future__ import with_statement 
import os, sys
import wx
import wx.xrc as xrc
import amber

from amberview_xrc import xrcAmberView

#-------------------------------------------------------------------------------

class AmberPanel(xrcAmberView):
    def __init__(self, parent, id, name, log=None):
        xrcAmberView.__init__(self, parent)
        self.__log = log
        self.name = name
        self.__cache = {}
        self.__ctrls = {}
        self.__inputs = {}
        self.__outputs= {}

        # self.initView(parent)
        self.initConfig()
        self.initBind()

    def log(self, message):
        if self.__log: self.__log.write(message)

    def initView(self, parent):
        pass

    def initConfig(self):

        # initialize
        self.__cache = amber.Amber.opts_default

        # ctrl definitions
        self.__ctrls = dict(
            input_file      = xrc.XRCCTRL(self, 'input_file'),
            log_file        = xrc.XRCCTRL(self, 'log_file'),
            prmtop_file     = xrc.XRCCTRL(self, 'prmtop_file'),
            ip_restart_file = xrc.XRCCTRL(self, 'ip_restart_file'),
            op_restart_file = xrc.XRCCTRL(self, 'op_restart_file'),
            crds_file       = xrc.XRCCTRL(self, 'crds_file'),
            vels_file       = xrc.XRCCTRL(self, 'vels_file'),
            enes_file       = xrc.XRCCTRL(self, 'enes_file'),
        )

        self.__other_ctrls = dict(
            log_file_dialog   = xrc.XRCCTRL(self, 'log_file_dialog'),
            op_restart_dialog = xrc.XRCCTRL(self, 'op_restart_dialog'),
            crds_file_dialog  = xrc.XRCCTRL(self, 'crds_file_dialog'),
            vels_file_dialog  = xrc.XRCCTRL(self, 'vels_file_dialog'),
            enes_file_dialog  = xrc.XRCCTRL(self, 'enes_file_dialog'),
            run_amber         = xrc.XRCCTRL(self, 'run_amber'),
            run_guage         = xrc.XRCCTRL(self, 'run_guage'),
            save_output       = xrc.XRCCTRL(self, 'save_output'),
            run_remote_config = xrc.XRCCTRL(self, 'run_remote_config'),
            view_log_file     = xrc.XRCCTRL(self, 'show_log_file')
        )

        self.showConfigs()

    def bindButton(self, function, xrc_id):
        self.Bind(wx.EVT_BUTTON, function, id=xrc.XRCID(xrc_id))

    def initBind(self):
        # show remote config dialog
        self.bindButton(self.onRemoteConfigDlg, 'run_remote_config')
        # run amber
        self.bindButton(self.onRunAmber, 'run_amber')
        # save outputs
        self.bindButton(self.onSaveDialog, 'log_file_dialog')
        self.bindButton(self.onSaveDialog, 'op_restart_dialog')
        self.bindButton(self.onSaveDialog, 'crds_file_dialog')
        self.bindButton(self.onSaveDialog, 'vels_file_dialog')
        self.bindButton(self.onSaveDialog, 'enes_file_dialog')
        # show output log
        self.bindButton(self.onShowOutput, 'show_log_file')

    def showConfigs(self):
        """Show the configs."""
        ctrls = self.__ctrls
        cache = self.__cache
        # inputs
        ctrls['input_file'].SetPath( cache['input_file'] )
        ctrls['prmtop_file'].SetPath( cache['prmtop_file'] )
        ctrls['ip_restart_file'].SetPath( cache['ip_restart_file'] )
        # outputs
        ctrls['log_file'].SetValue( cache['log_file'] )
        ctrls['op_restart_file'].SetValue( cache['op_restart_file'] )
        ctrls['crds_file'].SetValue( cache['crds_file'] )
        ctrls['vels_file'].SetValue( cache['vels_file'] )
        ctrls['enes_file'].SetValue( cache['enes_file'] )

    def saveConfigs(self):
        """Save the configs to cache."""
        ctrls = self.__ctrls
        cache = self.__cache
        # inputs
        # cache['input_file'] = ctrls['input_file'].GetTextCtrlValue()
        cache['input_file'] = ctrls['input_file'].GetTextCtrlValue()
        cache['prmtop_file'] = ctrls['prmtop_file'].GetTextCtrlValue()
        cache['ip_restart_file'] = \
                ctrls['ip_restart_file'].GetTextCtrlValue()
        # outputs
        cache['log_file'] = ctrls['log_file'].GetValue()
        cache['op_restart_file'] = ctrls['op_restart_file'].GetValue()
        cache['crds_file'] = ctrls['crds_file'].GetValue()
        cache['vels_file'] = ctrls['vels_file'].GetValue()
        cache['enes_file'] = ctrls['enes_file'].GetValue()

    def logConfig(self): pass

    def onRemoteConfigDlg(self): pass

    def onShowLog(self): pass

    def onRunAmber(self, event):
        self.saveConfigs()

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
                        path = '/home/hpcs/ceid-opt/bin/marvin',
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

        import project
        try:
            proj = wx.GetApp().getCurPrj()
        except AttributeError:
            proj = project.Project(root=nagara_root, name='test proj')

        task = project.Task(
            proj, configs=remote_configs,
            name='amber-test', host='hpcs', log=self.__log
        )
        proj.appendTask(task)
        self.log('set amber task\n')

        # job manager system
        import jms
        # LSF
        # task.setJMS(jms.LSF())
        task.setJMS(jms.LSF(nproc=8))
        self.log('set job system manager: LSF\n')

        import amber
        cmd = amber.Amber(task, log=self.__log)
        cmd.setSettings(self.__cache)
        cmd.setInputFiles(**self.__cache)
        self.log('create the amber task object.\n')


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

        task.setupRemote()
        self.log('setup remote job directory\n')

        # run
        self.log('running amber job on remote host\n')
        task.run()

        # done
        self.log('done the calculation\n')

        # get output
        self.task = task

    def onSaveDialog(self, event):
        """Open the save dialog and save the file name to cache."""
        btn = event.GetEventObject()

        ctrls = self.__other_ctrls

        # check the trigger object
        # elif event.GetID() == XRCID('op_restart_dialog'):
        #     wildcard = 'Amber restart file (*.rst)|*.rst'
        #     ctrls = self.__ctrls['op_restart_file']
        if btn == ctrls['log_file_dialog']:
            wildcard = 'Amber log file (*.log)|*.log'
            ctrls = self.__ctrls['log_file']

        elif btn == ctrls['op_restart_dialog']:
            wildcard = 'Amber restart file (*.rst)|*.rst'
            ctrls = self.__ctrls['op_restart_file']

        elif btn == ctrls['crds_file_dialog']:
            wildcard = 'Amber trajectory file (*.mdcrd.gz)|*.mdcrd.gz'
            ctrls = self.__ctrls['crds_file']

        elif btn == ctrls['vels_file_dialog']:
            wildcard = 'Amber velocity file (*.mdvel.gz)|*.mdvel.gz'
            ctrls = self.__ctrls['vels_file']

        elif btn == ctrls['enes_file_dialog']:
            wildcard = 'Amber energy file (*.ene)|*.ene'
            ctrls = self.__ctrls['enes_file']

        else:
            raise 'aaaaa'

        dlg = wx.FileDialog(
            self, message="Save file as ...", defaultDir=os.getcwd(), 
            defaultFile="", wildcard=wildcard, style=wx.SAVE
        )
        # default filter
        # dlg.SetFilterIndex(2)
        # show the dialog
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            # show the dialog
        ctrls.SetValue(path)
        dlg.Destroy()

    def onShowOutput(self, event):
        import outputview
        dlg = outputview.OutputDlg()
        rpath = self.task.remote.getPath()
        remote_output_fn = rpath + '/' + 'amber.log'
        lpath = self.task.local.getPath()
        local_output_fn = os.path.join(lpath, 'amber.log')

        self.task.getConnection().get(remote_output_fn, local_output_fn)
        self.task.getConnection().close()

        local_file = open(local_output_fn, 'r')

        dlg.write(local_file.read())
        local_file.close()
        dlg.show()
        return True

#-------------------------------------------------------------------------------

def main():
    import nagaratest
    app = nagaratest.FrameTest()
    log = app.log
    frame = app.frame

    dlg = wx.Dialog(None, -1, title='Amber Dialog', size=(480, 570))
    # paicspanel.MarvinPanel(dlg, -1, 'marvin', log=self.getLog())
    AmberPanel(dlg, -1, 'amber', log=log)
    dlg.ShowModal()
    dlg.Destroy()

    # app.MainLoop()

    try:
        app.MainLoop()
    except:
        app.RedirectStdio()


if __name__ == '__main__':
    main()
    module = __file__.split('.')[0]
    print 


