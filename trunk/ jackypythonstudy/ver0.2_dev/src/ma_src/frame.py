#! /usr/bin/env python
# _*_ coding: utf-8 _*_
# Copyright (C)  2009 Takakazu Ishikura

import os, sys
import wx
import wx.aui
from wx.xrc import XRCCTRL, XRCID
import systemview
import logview
import molview
import connection
import copyright
import setglobalpanel

# from frame_xrc import xrcFrame, xrcMenuBar
from menubar_xrc import xrcMenuBar

#-------------------------------------------------------------------------------

class Frame(wx.Frame):

    """
    The top GUI frame of Nagara.
    """

    def __init__(self, id=-1, title='', pos=wx.DefaultPosition,
                 size=wx.DefaultSize, 
                 style=wx.DEFAULT_FRAME_STYLE|wx.SUNKEN_BORDER|wx.CLIP_CHILDREN,
                 configs={}):
        """Constructor."""
        wx.Frame.__init__(self, None, id, title, pos, size, style)

        # self.res = None
        self.configs = configs if configs else {}

        # initialize views
        self.initView()
        self.initMenuBar()
        self.initStatusBar()
        
        self.CentreOnScreen(True)
        self.Show(True)

        # molview
        self.molview_frame = wx.Frame(self, -1, title='Molecule View Dlg', size=(450, 450))
        self.molview=molview.myGLCanvas(self.molview_frame)
        self.molview_frame.Show()

    def initView(self, configs=None):
        """Initialize the frame to manage each pane."""
        # tell FrameManager to manage this frame
        self._auimgr = wx.aui.AuiManager()
        self._auimgr.SetManagedWindow(self)
        self._aui_perspectives = []
        self._panels = {}
        
        # set frame icon
        self.setIcon()

        self.SetMinSize(wx.Size(1024,768))

        # add a bunch of panes

        # project view
        self._panels['ProjectView'] = wx.Panel(self, -1)
        # self._panels['ProjectView'] = projectview.ProjectView(self, configs)
        self._auimgr.AddPane(
            # projectview.ProjectView(self, configs)
            self._panels['ProjectView'],
            wx.aui.AuiPaneInfo().
            Name('ProjectView').Caption('Project').Right().Layer(0).
            CloseButton(True).MaximizeButton(True).
            MinSize(wx.Size(200,100))
        )
        #setting view
        
        # system view
        self._panels['SystemView'] = systemview.SystemView(
            self, 1, wx.DefaultPosition, (-1,-1), style=wx.SUNKEN_BORDER
        )
        self._auimgr.AddPane(
            self._panels['SystemView'],
            wx.aui.AuiPaneInfo().
            Name('SystemView').Caption('Biosystem Tree').
            Left().Layer(1).Position(0).
            CloseButton(True).MaximizeButton(True).
            MinSize(wx.Size(200,100))
        )

        # log view
        self._panels['LogView'] = logview.LogView(self)
        self._auimgr.AddPane(
            self._panels['LogView'],
            wx.aui.AuiPaneInfo().
            Name('LogView').Caption('Log Console').
            Bottom().Layer(0).
            CloseButton(True).MaximizeButton(True).
            MinSize(wx.Size(200,100))
        )

        self._auimgr.Update()

    def initStatusBar(self, configs=None):
        """Initialize the status bar."""
        self.statusbar = self.CreateStatusBar()

    def initMenuBar(self, configs=None):
        # self.menubar = self.res.LoadMenuBar('MenuBar')
        self.menubar = xrcMenuBar()
        self.SetMenuBar(self.menubar)
        self.bindMenuItem()

    def initViewOther(self, parent):
        self.console_tab.AddPage(self.log_panel, 'Log View')

    def initBind(self): pass

    def initStatusBar(self):
        # self.status = self.res.LoadStatusBar
        pass

    def bindMenuItem(self):
        bind = self.Bind
        bind(wx.EVT_MENU, self.onAboutBox, id=XRCID("About"))
        bind(wx.EVT_MENU, self.onOpenMoleculeDlg, id=XRCID("OpenMolecule"))
        bind(wx.EVT_MENU, self.onExit, id=XRCID("Exit"))
        bind(wx.EVT_MENU, self.onDebug, id=XRCID("Debug"))
        bind(wx.EVT_MENU, self.onConfigDlg, id=XRCID('ConfigRemote'))
        bind(wx.EVT_MENU, self.onShowConfigDlg, id=XRCID('ShowConfigs'))
        # amber, marvin, paics
        bind(wx.EVT_MENU, self.onPaicsDlg, id=XRCID('RunPaics'))
        bind(wx.EVT_MENU, self.onMarvinDlg, id=XRCID('RunMarvin'))
        bind(wx.EVT_MENU, self.onAmberDlg, id=XRCID('RunAmber'))
        bind(wx.EVT_MENU, self.onProjectDlg, id=XRCID('RunProjectDlg'))
        bind(wx.EVT_MENU, self.onRemoteRootDlg, id=XRCID('RunRemoteRootDlg'))

    def setIcon(self):
        """Set the icon to frame."""
        icon = wx.Icon('nagara.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

    def onConfigDlg(self, event):
        dlg = ConfigDlg(None, "simpledialog.py")
        dlg.ShowModal()
        dlg.Destroy()
        return True

    def getLog(self):
        return self._panels['LogView']

    def log(self, message):
        self._panels['LogView'].write(message)

    def onMoleculeViewDlg(self, event):
        frame = wx.Frame(self, -1, title='Molecule View Dlg', size=(450, 450))
        self.molview=molview.myGLCanvas(frame)
        frame.Show()
        return True

    def onAmberDlg(self, event):
        import amberpanel
        dlg = wx.Dialog(None, -1, title='Amber Dialog', size=(480, 570))
        amberpanel.AmberPanel(dlg, -1, 'amber', log=self.getLog())
        dlg.ShowModal()
        dlg.Destroy()
        return True

    def onPaicsDlg(self, event):
        import paicspanel
        dlg = wx.Dialog(None, -1, title='Paics Dialog', size=(390, 340))
        paicspanel.PaicsPanel(dlg, -1, 'paics', log=self.getLog())
        dlg.ShowModal()
        dlg.Destroy()
        return True

    def onMarvinDlg(self, event):
        import marvinpanel
        dlg = wx.Dialog(None, -1, title='Marvin Dialog', size=(562, 500))
        marvinpanel.MarvinPanel(dlg, -1, 'marvin', log=self.getLog())
        dlg.ShowModal()
        dlg.Destroy()
        return True

    def onProjectDlg(self, event):
        # In this case we include a "New directory" button. 
        dlg = wx.DirDialog(self, "Choose a nagara project directory:",
                          style=wx.DD_DEFAULT_STYLE
                           #| wx.DD_DIR_MUST_EXIST
                           #| wx.DD_CHANGE_DIR
                           )

        if dlg.ShowModal() == wx.ID_OK:
            self.configs['project_root'] = dlg.GetPath()
            project = wx.GetApp().getCurPrj()
            project.setRoot(dlg.GetPath())
            self.log('set the project directory: '+ str(dlg.GetPath()))

        dlg.Destroy()

    def onRemoteRootDlg(self, event):
        dlg = wx.TextEntryDialog(
                self, 'Put a remote working directory.',
                'RemoteRootDlg', '/home/ishikura/Nagara/projects')

        dlg.SetValue('/home/ishikura/Nagara/projects')

        if dlg.ShowModal() == wx.ID_OK:
            configs = wx.GetApp().getConfigs()
            configs['remote_root'] = dlg.GetValue()

        dlg.Destroy()

    def onShowConfig(self, event):
        self.setting.ShowModal()
        
    def onShowConfigDlg(self, event):
        import setglobalpanel
        #self._auimgr = wx.aui.AuiManager()
        #self._auimgr.SetManagedWindow(self)
        #self._aui_perspectives = []
        #self._panels = {}
        self._panels['SettingView'] = setglobalpanel.SetGlobalPanel(self,-1)
        self._auimgr.AddPane(
            # projectview.ProjectView(self, configs)
            self._panels['SettingView'],
            wx.aui.AuiPaneInfo().
            Name('SettingView').Caption('Setting').Center().Layer(1).
            CloseButton(True).MaximizeButton(True).
            MinSize(wx.Size(500,500))
        )
        
        # self._panels['ProjectView'] = projectview.ProjectView(self, configs)
        
        '''
        dlg = wx.Dialog(None, -1, title='Amber Dialog',size=(600,500))
        # paicspanel.MarvinPanel(dlg, -1, 'marvin', log=self.getLog())
        setglobalpanel.SetGlobalPanel(dlg,-1)
        dlg.ShowModal()
        #dlg.SetSize(dlg.GetBestSize())
        dlg.Destroy()
        '''
        
    def onOpenMoleculeDlg(self, event):
        """Show the open molecule dialog and get a molecule."""
        dirpath = "C:\Home_Ishikura\docs\Nagara\src\user-dir"
        message = ""
        extension = "|".join(
            ["Protein Data Bank File ( *.pdb )|*.pdb",
             "Sybyl Mol2 File ( *.mol2 )|*.mol2"]
        )

        dialog = wx.FileDialog(
            self, "Please choose pdb file",
            defaultDir=dirpath, wildcard=extension
        )
        answer = dialog.ShowModal()

        # filename = dialog.GetFilename()
        filename  = dialog.GetPath()
        dirpath = dialog.GetDirectory()
        dialog.Destroy()
        
        # read the pdb file and store to the system
        import molformat
        # self.nagara.system = molformat.PDB(filename).read()
        system = molformat.PDB(filename).read()
        project = wx.GetApp().getCurPrj()
        project.appendSystem(system)
        systemview = self._panels['SystemView']
        systemview.loadSystem(system)
        if __debug__:
            for atom in system.getAtoms():
                self.getLog().write(atom.getAtmNum())

        crd = system.getCrds()
        ans = [ atom.getAtmNum() for atom in system.getAtoms() ]

        if self.molview:
            self.molview.SetMolecule(ans, crd)
            chk = self.molview.DisableDraw()
            self.molview.SetAtomDefault()
            self.molview.SetBondDefault()
            self.molview.ViewReset()
            self.molview.EnableDraw(chk)

        # for res in system.getGroups('Residues'):
        #     print(res.id, res.name)
        #     for atom in res.getAtoms():
        #         print(atom.id, atom.name)

        # molformat.PDB('user-dir/test.pdb').write(system)

        # frame = MyFrame(None, -1, "ProjectFrame")
        # frame.systemview.loadSystem(system)


    def onAboutBox(self, event):
        """Show the dialog of About information."""
        import copyright as c
        info = wx.AboutDialogInfo()

        info.SetIcon(wx.Icon('nagara.ico', wx.BITMAP_TYPE_ICO))
        info.SetName(c.NAME)
        info.SetVersion(c.VERSION)
        info.SetDescription(c.DESCRIPTION)
        info.SetCopyright(c.COPYRIGHT)
        info.SetWebSite(c.WEBSITE)
        # info.SetLicence(c.LICENCE)
        for d in c.DEVELOPERS:
            info.AddDeveloper(d)
        # info.AddDocWriter('jan bodnar')
        # info.AddArtist('The Tango crew')
        # info.AddTranslator('jan bodnar')
        wx.AboutBox(info)

    def OnClose(self, event):
        """Close the frame."""
        self._auimgr.UnInit()
        del self._auimgr
        self.Destroy()

    def onExit(self, event):
        """Exit the frame."""
        #self.molview.OnClose(event)
        self.OnClose(event)

    def onDebug(self, event):
        """Show debugging informations."""
        self.getLog().write(self.configs)
 
    def onCloseRemote(self, event):
        self.closeRemote()

    # try code
    def init_bind(self):
        self.nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.paics_panel.bind(self.on_run_paics, 'run_PAICS')

    def myprint(self, mes, prompt=True):
        self.getLog().printLog(mes, prompt)

    def OnPageChanged(self, event):
        i = event.GetSelection()
        self.myprint('current book is %d\n' % i, prompt=True)
        self.get_configs()
        event.Skip()

    def on_run_paics(self, event):
        self.on_run_paics()

    def run_paics(self):

        self.get_configs()

        self.myprint('now setting...\n')
        conf_remote = self.configs['remote']
        conf_paics  = self.configs['paics']

        # normalization for remote
        host = conf_remote['host']
        user = conf_remote['user']
        passwd = conf_remote['passwd']
        if not passwd:
            sys.exit(1)
        NAGARA_ROOT = conf_remote['NAGARA_ROOT']
        PROJECT_ROOT = conf_remote['PROJECT_ROOT']
        project_name = conf_remote['project_name']
        # normalization for paics
        input_fn = conf_paics['input_file']
        input_contents = open(input_fn, 'r').read()
        PAICS_ROOT = conf_paics['PAICS_root']
        nproc = conf_paics['nproc']
        project_dir = '/'.join([PROJECT_ROOT, project_name])

        # start the session
        self.myprint('open ssh connection...\n')
        socket = ssh.Connection(host, password=passwd)
        self.myprint('1')
        output = socket.execute('ls')
        self.myprint('2')
        for i in output:
            self.myprint(i)

        paics_proc = paics.Paics(socket)
        paics_proc.setup(PAICS_ROOT, project_dir, input_contents)
        self.myprint('3')
        self.myprint('run paics...\n')
        output = paics_proc.run(lsf=False)
        self.myprint('4')
        for o in output:
            self.myprint(o, prompt=False)

    def getConfigs(self):
        """Get the configures about the frame."""
        if self.configs is None:
            self.configs = {}
        self.configs['remote'] = self.config_panel.get_configs()
        self.configs['paics'] = self.paics_panel.get_configs()

        self.projectview = wx.Panel(self.rightnb, -1)
        #self.projectview = projectview.ProjectView(self, configs)
        #self.amber_panel = amber.AmberPanel(self.nb, -1, 'amber panel')
        self.rightnb.AddPage(self.projectview, 'Project Tree')
        # self.myprint(str(self.configs['paics']))

#-------------------------------------------------------------------------------

class FrameAppearance(object): pass


class ConfigDlg(wx.Dialog):

    def __init__(self, parent, title='Global configure'):
        wx.Dialog.__init__(self, parent, -1, title=title, size=(350,400))

        # self.nb = wx.Notebook(self, -1, style=wx.NB_TOP)

        # self.cg = ConfigGlobal(self.nb, -1)
        # self.cg = wx.Panel(self.nb, -1, 'Global configure')
        # self.nb.AddPage(self.cg, 'Global configure')

        import configremote as cr
        self.cr = cr.ConfigRemote(self)
        # self.nb.AddPage(self.cr, 'Remote configure')



################################################################################

def main():
    logfile =  "_error.log"
    app = wx.App(redirect=False, filename=logfile)
    frame = Frame()

    frame.Show()

    try:
        app.MainLoop()
    except:
        app.RedirectStdio()

if __name__ == '__main__':
    main()
