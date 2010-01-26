# _*_ coding: utf-8 _*_
# Copyright (C)  2009 Takakazu Ishikura

import sys, os

# nagara modules
# nagara_path = os.environ['NAGARA_PATH']
# sys.path.append( os.path.join(nagara_path, 'src') )

sys.path.insert(0, os.path.join(sys.prefix, 'libs/PyOpenGL-3.0.0c1-py2.5.egg'))
sys.path.insert(0, os.path.join(sys.prefix, 'libs/setuptools-0.6c9-py2.5.egg'))
sys.path.insert(0, os.path.join(sys.prefix, 'libs/paramiko-1.7.4-py2.5.egg'))
import wx
from wx import xrc
from wx.lib.wordwrap import wordwrap
# import copyright

from utils.event import NagaraEvent
from core.exception import NagaraException
import degras.image as im

# import configs
# import project

# various settings
if hasattr(sys,"setdefaultencoding"):
    sys.setdefaultencoding("utf-8")

def main_is_frozen():
    return (hasattr(sys, "frozen") or # new py2exe
            hasattr(sys, "importers") or # old py2exe
            imp.is_frozen("__main__")) # tools/freeze

def get_main_dir():
    if main_is_frozen():
        return os.path.abspath(os.path.dirname(sys.executable))
    return os.path.abspath(os.path.dirname(sys.argv[0]))


#-------------------------------------------------------------------------------

class Nagara(wx.App):

    def OnInit(self, configs={}):
        """Constructor."""

        self.configs = configs if configs else {}

        # self.cur_prj = project.Project(root='', name='test project')
        # self.projects = [self.cur_prj]
                         
        self.init_view()
        # self.init_project()
        # self.init_molview()
        # self.init_workflow()

        # self.initMenu()
        self.initEverythingElse()
        return True

    def init_view(self):
        """Initilize the Frame."""

        # frame
        from degras.frame.frame_agent   import Frame
        frame = Frame()

        from degras.frame.menubar_agent import Menubar
        menubar = Menubar()
        frame.set_menubar( menubar.get_view() )

        # initialize
        frame.init()
        frame.show()


        # append work flow canvas
        from degras.workflow.wfcanvas_agent import WorkFlowCanvas
        workflow_panel = WorkFlowCanvas(frame)
        # workflow_panel = wx.Panel(frame.get_view(), -1)
        frame.append_pane(
            workflow_panel, wx.aui.AuiPaneInfo().Name('WorkFlowCanvas').
            Caption('Work Flow Canvas').Centre().Layer(0).CloseButton(False).
            MaximizeButton(True).MinSize(wx.Size(400,400))
        )

        # add system tree viewer
        systemview_panel = wx.Panel(frame.get_view(), -1)
        frame.append_pane(
            systemview_panel, wx.aui.AuiPaneInfo().Name('SystemView').
            Caption('System').Right().Layer(0).CloseButton(True).
            MaximizeButton(True).MinSize(wx.Size(200,100))
        )

        # # add log viewer
        # panel = wx.Panel(frame.get_view(), -1)
        # frame.append_pane(
            # panel, wx.aui.AuiPaneInfo().Name('LogView').
            # Caption('Log View').Bottom().Layer(0).CloseButton(False).
            # MaximizeButton(False).MinSize(wx.Size(200,100))
        # )

        # add job manager
        from degras.jobmanager.manager_agent import JobManager
        from degras.jobmanager.manager_model import ManagerModel
        jobmodel = ManagerModel()
        self.jobmanager = JobManager(frame, jobmodel)
        frame.append_pane(
            self.jobmanager.get_view(), wx.aui.AuiPaneInfo().Name('JobManager').
            Caption('Job Manager').Bottom().Layer(0).CloseButton(True).
            MaximizeButton(True).MinSize(wx.Size(200,100))
        )
        
        # add Project viewer
        project_panel = wx.Panel(frame.get_view(), -1)
        frame.append_pane(
            project_panel, wx.aui.AuiPaneInfo().Name('ProjectView').
            Caption('Project').Left().Layer(1).Position(0).
            CloseButton(True).MaximizeButton(True).MinSize(wx.Size(200,100))
        )

        # add property viewer
        property_panel = wx.Panel(frame.get_view(), -1)
        frame.append_pane(
            property_panel, wx.aui.AuiPaneInfo().Name('PropertyView').
            Caption('Property').Left().Layer(1).Position(1).
            CloseButton(True).MaximizeButton(True).MinSize(wx.Size(200,100))
        )

        # self.test_jobmodel()



    def test_jobmodel(self): 
        # create Job
        from degras.jobmanager.tests.jobmock import JobMock
        job = JobMock(1)
        
        self.jobmanager.append_job(job)
        #print model.get_job_dict()
        #managermodel.append(job)
        #managermodel.append(job)
        #managermodel.append(job)
        #managermodel.append(job)
        #managermodel.append(job)


        import time
        def append_job(interval, job):
            time.sleep(interval)
            self.jobmanager.append_job(job)
            time.sleep(interval)
            self.jobmanager.append_job(job)

        import threading
        t = threading.Thread(name=None, target=append_job, args=[3, job])
        t.start()


        # toolbar

    def init_projectmanager(self):
        pass

    def appendProject(self, project):
        """Append the project settings to the project list."""
        self.projects.append(project)
        self.cur_prj = project

    def getCurPrj(self):
        """Get the active project."""
        return self.cur_prj

    def getProjects(self):
        """Get the projects."""
        return self.projects

    def initEverythingElse(self):
        # sizer.Fit(self.frame)
        # sizer.SetSizeHints(self.frame)
        pass

    def runGrid(self, evt):
        pass

    def onExit(self, evt):
        connectcluster.close()
        if self.setting.getRemoteInfo().isActive:
            try:
                self.closeRemote()
            except:
                pass
        self.frame.Close()
        quit()

    def onErrorHandler(self, message):
        self.printLog("In ErrorHandlerFunc()")

        dlg = wx.MessageDialog(None, message, caption="Error!",
                style=wx.OK|wx.ICON_ERROR|wx.STAY_ON_TOP,
                pos=wx.DefaultPosition)
        ret = dlg.ShowModal()

    def printLog(self, message):
        pass

    def getCurPrj(self):
        """Return a reference to the current project."""
        return self.cur_prj

    def getConfigs(self):
        return self.configs
                

#   def onSettingRemote(self, evt):

#       self.remoteHost = 
#       self.remoteUser =

#   def initFrame(self):
#       pass

    def initMenu(self):
        pass

#   def initStatus(self):
#       pass

#   #   def runMakeGrid(self, config): #       pass 
#   def runMD(self):
#       pass

#   def runDocking(self, config):
#       pass

#   def runMinimize(self, config):
#       pass


    # def setIcon(self):
        # """Set the icon to frame."""
        # icon = wx.Icon('nagara.ico', wx.BITMAP_TYPE_ICO)
        # self.SetIcon(icon)


def main():
    # logfile = "_error.log"
    # app = Nagara(redirect=False, filename=logfile)
    app = Nagara(redirect=False)
    try:
        app.MainLoop()
    except:
        app.RedirectStdio()


if __name__ == '__main__':
    main()
