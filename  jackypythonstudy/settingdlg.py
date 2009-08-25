import wx
import htlpanel

########################################################################
class SettingDialog(wx.Frame):
    """"""

    #----------------------------------------------------------------------
    def __init__(self,parent,id,selection):
        wx.Frame.__init__(self,parent,-1,'Setting Dialog',size=(-1,-1))

        panel = wx.Panel(self)
        #panel.SetBackgroundColour('white')
        nb = wx.Notebook(panel, id, size=(21,21), style=
                         wx.BK_DEFAULT
                         #wx.BK_TOP 
                         #wx.BK_BOTTOM
                         #wx.BK_LEFT
                         #wx.BK_RIGHT
                         # | wx.NB_MULTILINE
                         )

        win = SshSetPanel(nb)
        nb.AddPage(win, "SSH")

        win = PathSetPanel(nb)
        nb.AddPage(win, "Path")

        win = wx.Panel(nb)
        nb.AddPage(win,"Jims")

        win = wx.Panel(nb)
        nb.AddPage(win,"Command")

        nb.SetSelection(min(selection,nb.GetPageCount()-1)) # the selection must smaller than pagecount.
        self.CenterOnParent()
        self.SetMinSize((300,250))

        self.okBtn = wx.Button(panel, wx.ID_OK, "Ok")
        self.cancelBtn = wx.Button(panel, wx.ID_CANCEL, "Cancel")

        self.Bind(wx.EVT_BUTTON,self.OnOk,self.okBtn)
        self.Bind(wx.EVT_BUTTON,self.OnCanel,self.cancelBtn)

        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(self.okBtn,0,wx.ALIGN_RIGHT,5)
        sizer_2.Add(self.cancelBtn,0,wx.ALIGN_RIGHT,5)


        mainsizer = wx.BoxSizer(wx.VERTICAL)
        mainsizer.Add(nb,1,wx.EXPAND,5)
        mainsizer.Add(sizer_2,0,wx.ALIGN_RIGHT,5)

        panel.SetSizer(mainsizer)
        mainsizer.Fit(panel)
        mainsizer.SetSizeHints(panel)
    def OnOk(self,event):
        from modules import dict4ini as d4i
        rec = d4i.DictIni('remote_config.ini')
        
        rec.remote_configs = dict(
    # email = 'ishikura@gifu-u.ac.jp',
    local = dict(
        ssh = {},
        rootdir = 'C:\path\to\nagara-root',
        workdir = '',
        jms = dict(
            Single = dict(
                envs = {},
                path = {},
            ),
            MultiProcess = dict(
            ),
        ),
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
        workdir = '/work/ishikura',
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
                # envs = dict(AMBERHOME = '/home/hpc/opt/amber10.eth'),
                # path = '/home/hpcs/opt/amber10.eth/exe/sander.MPI',
                envs = dict(AMBERHOME = '/home/ishikura/opt/amber10.eth'),
                path = '/home/ishikura/opt/amber10.eth/exe/sander.MPI',
            ),
            marvin = dict(
                envs = {},
                # path = '/home/hpcs/Nagara/app/bin/marvin',
                path = '/home/ishikura/Nagara/app/bin/marvin',
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
        #pass
        rec.save()
        
    def OnCanel(self,event):
        wx.CloseEvent()

########################################################################
class SshSetPanel(wx.Panel):
    #----------------------------------------------------------------------
    def __init__(self,parent):
        """Constructor"""
        wx.Panel.__init__(self,parent,-1)
        # create the controls
        self.topLbl = wx.StaticText(self, -1, "Ssh Setting")
        self.topLbl.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.hostLbl = wx.StaticText(self, -1, "Host:")
        self.host = wx.TextCtrl(self, -1, "");
        self.portLbl = wx.StaticText(self, -1, "Port:")
        self.port = wx.TextCtrl(self, -1, "");
        self.userLbl = wx.StaticText(self, -1, "User:")
        self.user = wx.TextCtrl(self, -1, "");
        self.passLbl = wx.StaticText(self, -1, "Password:")
        self.password = wx.TextCtrl(self, -1, "",style =wx.PASSWORD);
        #self.okBtn = wx.Button(self, -1, "Save")
        #self.cancelBtn = wx.Button(self, -1, "Cancel")
        self.Dolayout()

    def Dolayout(self):
        self.mainsizer = wx.BoxSizer(wx.VERTICAL)
        fgsizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        fgsizer.AddGrowableCol(1)
        fgsizer.Add(self.hostLbl, 0,
                    wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        fgsizer.Add(self.host,0,wx.EXPAND)

        fgsizer.Add(self.portLbl, 0,
                    wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        fgsizer.Add(self.port,0,wx.EXPAND)

        fgsizer.Add(self.userLbl, 0,
                    wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        fgsizer.Add(self.user,0,wx.EXPAND)

        fgsizer.Add(self.passLbl, 0,
                    wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        fgsizer.Add(self.password,0,wx.EXPAND)
        #btsizer = wx.BoxSizer(wx.HORIZONTAL)
        #btsizer.Add(self.okBtn,-1,wx.ALIGN_RIGHT)
        #btsizer.Add(self.cancelBtn,-1,wx.ALIGN_RIGHT)
        self.mainsizer.Add(self.topLbl,0, wx.ALL, 5)
        self.mainsizer.Add(wx.StaticLine(self), 0,
                           wx.EXPAND|wx.TOP|wx.BOTTOM, 5)
        self.mainsizer.Add(fgsizer,1,wx.EXPAND|wx.ALL,5)
        #self.mainsizer.Add(btsizer,0,wx.ALIGN_RIGHT,5)
        self.SetSizer(self.mainsizer)

class PathSetPanel(wx.Panel):
    #----------------------------------------------------------------------
    def __init__(self,parent):

        wx.Panel.__init__(self,parent,-1)
            # create the controls
        self.topLbl = wx.StaticText(self, -1, "Path Setting")
        self.topLbl.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.localLbl = wx.StaticText(self, -1, "Locl Dir Path:")
        self.local = wx.TextCtrl(self, -1, "")
        self.remoteLbl = wx.StaticText(self, -1, "Remote Dir Path:")
        self.remote = wx.TextCtrl(self, -1, "")
        """"""
        self.Dolayout()
    def Dolayout(self):
        self.mainsizer = wx.BoxSizer(wx.VERTICAL)
        fgsizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        fgsizer.AddGrowableCol(1)
        fgsizer.Add(self.localLbl, 0,
                    wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        fgsizer.Add(self.local,0,wx.EXPAND)
        fgsizer.Add((-1,10),0)
        fgsizer.Add((-1,10),0)

        fgsizer.Add(self.remoteLbl, 0,
                    wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        fgsizer.Add(self.remote,0,wx.EXPAND)       

        self.mainsizer.Add(self.topLbl,0, wx.ALL, 5)
        self.mainsizer.Add(wx.StaticLine(self), 0,
                           wx.EXPAND|wx.TOP|wx.BOTTOM, 5)
        self.mainsizer.Add(fgsizer,1,wx.EXPAND|wx.ALL,5)
        #self.mainsizer.Add(btsizer,0,wx.ALIGN_RIGHT,5)
        self.SetSizer(self.mainsizer)



if __name__ =='__main__':

    app = wx.App()
    frame = SettingDialog(None,-1,selection = 0)
    frame.Show()
    app.MainLoop()