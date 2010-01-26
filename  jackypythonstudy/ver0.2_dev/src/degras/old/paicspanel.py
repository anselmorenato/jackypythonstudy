#! /usr/bin/env python
# _*_ coding: utf-8 _*_
# Copyright (C)  2009 Takakazu Ishikuraimport wx

from __future__ import with_statement 
import os, sys
import wx
import wx.xrc as xrc
import paics

from paicsview_xrc import xrcPAICSView

# xrcfile = 'paicsview.xrc'
class PaicsPanel(xrcPAICSView):
    def __init__(self, parent, id, name, log=None):
        xrcPAICSView.__init__(self, parent)
        self.__log = log
        self.name = name
        self.__cache = {}
        self.__ctrls = {}
        self.__input  = None
        self.__output = None

        # self.initView(parent)
        self.initConfigs()
        self.initBind()

    def log(self, message):
        if self.__log: self.__log.write(message)

    def initView(self, parent):
        pass

    def initConfigs(self):

        # initialize
        # self.__output = self.__cache['paics_log_file']
        self.__cache = paics.Paics.opts_default
        self.__ctrls['paics_input_file'] = xrc.XRCCTRL(self, 'paics_input_file')
        self.showConfigs()

        # other ctrls


    def initBind(self):
        self.bindButton(self.onRunPaics, 'run_PAICS')
        self.bindButton(self.onRunPaicsView, 'run_PaicsView')

        btn = xrc.XRCCTRL(self, 'view_log')
        self.Bind(wx.EVT_BUTTON, self.onShowOutput, btn)

    def saveConfigs(self):
        """Save the configs to cache."""
        self.__cache['paics_input_file'] = self.__ctrls['paics_input_file'].GetPath()

    def showConfigs(self):
        """Show the configs."""
        self.__ctrls['paics_input_file'].SetPath( self.__cache['paics_input_file']
        )

    def getConfigs(self):
        """Return the paics configs."""
        self.saveConfigs()
        return self.__cache

    def bindButton(self, function, xrc_id):
        self.Bind(wx.EVT_BUTTON, function, id=xrc.XRCID(xrc_id))

    def onRunPaicsView(self, event):
        self.saveConfigs()
        PaicsView_exe = self.cache['select_PaicsView_exe']
        #print PaicsView_exe
        #os.system("c:\\home\\ishi\\program\\PaicsView\\main_win.exe")
        os.system(PaicsView_exe)

    def onRunPaics(self, event):
        import paics
        # print 'before', paics.Paics.opts_default
        # cache = paics.Paics.opts_default.copy()
        self.saveConfigs()
        # print 'after', paics.Paics.opts_default
        # print cache
        #print ''

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
            proj, configs=remote_configs, name='paics-test',
            host='hpcs', log=self.__log
        )
        proj.appendTask(task)
        self.log('set paics task\n')

        # job manager system
        import jms
        task.setJMS('Single')
        # task.setJMS(jms.LSF())
        print task.getJMS().getType()
        self.log('set job system manager: Single\n')

        import paics
        cmd = paics.Paics(task, log=self.__log)
        # envs = {'PAICS_ROOT': '/home/ishi/paics/paics-20081214'}
        # cmd.setEnvs( 
        # cmd.setPath( envs['PAICS_ROOT']+'/'+'main.exe' )
        cmd.setConfigs(self.__cache)
        cmd.setInputByFiles(paics_input_file=self.__cache['paics_input_file'])
        self.log('create the paics object.\n')


        import connection
        conn = connection.Connection(
            username=recos['user'], host=recos['host'], password=recos['passwd']
        )
        task.setConnection(conn)
        self.log('connect the channel to remote hosts\n')
        if not task.remote.isNone():
            task.delete()
            self.log('cleaned task: ' + task.getName() + '\n')

        self.log('create the local directory.\n')
        task.setCommand(cmd)
        task.setupLocal()
        self.log('setup paics job in local task directory\n')

        task.setupRemote()
        self.log('setup remote job directory\n')
        print task.remote.getState()

        # run
        self.log('running paics job on remote host\n')
        task.run()

        # done
        self.log('done the calculation\n')

        # get outputs
        self.task = task

    def onShowOutput(self, event):
        import outputview
        dlg = outputview.OutputDlg()
        rpath = self.task.remote.getPath()
        remote_output_fn = rpath + '/' + 'paics.log'
        lpath = self.task.local.getPath()
        local_output_fn = os.path.join(lpath, 'paics.log')

        self.task.getConnection().get(remote_output_fn, local_output_fn)
        self.task.getConnection().close()

        local_file = open(local_output_fn, 'r')

        dlg.write(local_file.read())
        dlg.show()
        return True

#-------------------------------------------------------------------------------

def main():
    import nagaratest
    app = nagaratest.FrameTest()
    log = app.log
    frame = app.frame

    dlg = wx.Dialog(None, -1, title='Paics Dialog', size=(390, 340))
    PaicsPanel(dlg, -1, 'paics', log=log)
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


