import wx
from modules import dict4ini as d4i
import sys

rec = d4i.DictIni('remote_config.ini')

########################################################################
class SettingDialog(wx.Frame):
    """"""

    #----------------------------------------------------------------------
    def __init__(self,parent,id,selection,target):
        self.target = target
        wx.Frame.__init__(self,parent,-1,title =self.target+' setting',size=(-1,-1))
        

        panel = wx.Panel(self)
        #panel.SetBackgroundColour('white')
        self.nb = wx.Notebook(panel, id, size=(21,21), style=
                         wx.BK_DEFAULT
                         #wx.BK_TOP 
                         #wx.BK_BOTTOM
                         #wx.BK_LEFT
                         #wx.BK_RIGHT
                         # | wx.NB_MULTILINE
                         )

        self.ssh = SshSetPanel(self.nb,self.target)
        self.nb.AddPage(self.ssh, "Ssh")

        self.path = PathSetPanel(self.nb,self.target)
        self.nb.AddPage(self.path, "Path")
        
        self.command = CmdSetPanel(self.nb,self.target)
        self.nb.AddPage(self.command,"Command")
        
        self.jms = wx.Panel(self.nb)
        self.nb.AddPage(self.jms,"Jms")
        
        sel = self.nb.GetSelection()
        print 'sel', sel
        page = self.nb.GetPageText(sel)
        print 'page', page

        #self.nb.SetSelection(min(selection,self.nb.GetPageCount()-1)) # the selection must smaller than pagecount.
        self.CenterOnParent()
        self.SetMinSize((400,380))

        self.okBtn = wx.Button(panel, wx.ID_OK, "Ok")
        self.cancelBtn = wx.Button(panel, wx.ID_CANCEL, "Cancel")

        self.Bind(wx.EVT_BUTTON,self.OnOk,self.okBtn)
        self.Bind(wx.EVT_BUTTON,self.OnCanel,self.cancelBtn)

        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(self.okBtn,0,wx.ALIGN_RIGHT,5)
        sizer_2.Add(self.cancelBtn,0,wx.ALIGN_RIGHT,5)


        mainsizer = wx.BoxSizer(wx.VERTICAL)
        mainsizer.Add(self.nb,1,wx.EXPAND,5)
        mainsizer.Add(sizer_2,0,wx.ALIGN_RIGHT,5)

        panel.SetSizer(mainsizer)
        mainsizer.Fit(self)
        #mainsizer.SetSizeHints(panel)
    def OnOk(self,event):
        target = self.target
        selection = self.nb.GetSelection()
        
        if selection ==0:
            rec['remote_configs'][target]['ssh']['address'] = self.ssh.host.GetValue()
            rec['remote_configs'][target]['ssh']['port'] = self.ssh.port.GetValue()
            rec['remote_configs'][target]['ssh']['user'] = self.ssh.user.GetValue()
            rec['remote_configs'][target]['ssh']['passwd'] = self.ssh.passwd.GetValue()
        elif selection ==1:
            rec['remote_configs'][target]['path']['localpath'] = self.path.local.GetValue()
            rec['remote_configs'][target]['path']['remotepath'] = self.path.remote.GetValue()
        elif selection ==2:
            rec.save()
        #pass
        rec.save()
        self.Close(True)
        
    def OnCanel(self,event):
        self.Close(True)

########################################################################
class SshSetPanel(wx.Panel):
    #----------------------------------------------------------------------
    def __init__(self,parent,target=''):
        """Constructor"""
        wx.Panel.__init__(self,parent,-1)
        target =target
        # create the controls
        
        self.hostLbl = wx.StaticText(self, -1, "Host:")
        self.host = wx.TextCtrl(self, -1, "");
        self.portLbl = wx.StaticText(self, -1, "Port:")
        self.port = wx.TextCtrl(self, -1, "");
        self.userLbl = wx.StaticText(self, -1, "User:")
        self.user = wx.TextCtrl(self, -1, "");
        self.passLbl = wx.StaticText(self, -1, "Password:")
        self.passwd = wx.TextCtrl(self, -1, "",style =wx.PASSWORD);
        #self.okBtn = wx.Button(self, -1, "Save")
        #self.cancelBtn = wx.Button(self, -1, "Cancel")
        self.Dolayout()

    def Dolayout(self):
        self.mainsizer = wx.BoxSizer(wx.VERTICAL)
        
        sbsizer = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Ssh Setting'), orient=wx.VERTICAL)
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
        fgsizer.Add(self.passwd,0,wx.EXPAND)
        #btsizer = wx.BoxSizer(wx.HORIZONTAL)
        #btsizer.Add(self.okBtn,-1,wx.ALIGN_RIGHT)
        #btsizer.Add(self.cancelBtn,-1,wx.ALIGN_RIGHT)
        sbsizer.Add(fgsizer,0,wx.EXPAND)
        self.mainsizer.Add(sbsizer,0,wx.EXPAND|wx.ALL,5)
        #self.mainsizer.Add(btsizer,0,wx.ALIGN_RIGHT,5)
        self.SetSizer(self.mainsizer)

class PathSetPanel(wx.Panel):
    #----------------------------------------------------------------------
    def __init__(self,parent,target=''):

        wx.Panel.__init__(self,parent,-1)
            # create the controls
        
        self.localLbl = wx.StaticText(self, -1, "Local Dir Path:")
        self.local = wx.TextCtrl(self, -1, "")
        self.remoteLbl = wx.StaticText(self, -1, "Remote Dir Path:")
        self.remote = wx.TextCtrl(self, -1, "")
        """"""
        self.Dolayout()
    def Dolayout(self):
        self.mainsizer = wx.BoxSizer(wx.VERTICAL)
        sbsizer = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Path Setting'), orient=wx.VERTICAL)
        fgsizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        fgsizer.AddGrowableCol(1)
        fgsizer.Add(self.localLbl, 0,
                    wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        fgsizer.Add(self.local,0,wx.EXPAND)
        
        fgsizer.Add(self.remoteLbl, 0,
                    wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        fgsizer.Add(self.remote,0,wx.EXPAND)       

        sbsizer.Add(fgsizer,0,wx.EXPAND)
        self.mainsizer.Add(sbsizer,0,wx.EXPAND|wx.ALL,5)
        #self.mainsizer.Add(btsizer,0,wx.ALIGN_RIGHT,5)
        self.SetSizer(self.mainsizer)
########################################################################
class CmdSetPanel(wx.Panel):
    """this is the panel of command setting """
    #----------------------------------------------------------------------
    def __init__(self,parent,target):
        
        wx.Panel.__init__(self,parent)
        self.target = target
        
        
        
        
        self.cmdpanel = wx.Notebook(self, -1, size=wx.DefaultSize, style=
                         wx.BK_DEFAULT
                         #wx.BK_TOP 
                         #wx.BK_BOTTOM
                         #wx.BK_LEFT
                         #wx.BK_RIGHT
                         # | wx.NB_MULTILINE
                         )
        
        #self.subnb = CmdTagPanel(self.cmdpanel)
        if rec['remote_configs'][self.target]._items.has_key('commands') and not len(rec['remote_configs'][self.target]['commands'].values())==0:
            for pagename in rec['remote_configs'][self.target]['commands'].keys():
                self.subnb = CmdTagPanel(self.cmdpanel,target)
                self.cmdpanel.AddPage(self.subnb,str(pagename))
        else:
            self.subnb = CmdTagPanel(self.cmdpanel,target)
            self.cmdpanel.AddPage(self.subnb,'noname')
        
        self.addBtn = wx.Button(self, -1, "+",size=(15,15))
        self.delBtn = wx.Button(self, -1,"-",size =(15,15))
        self.Bind(wx.EVT_BUTTON,self.OnAddTag,self.addBtn)
        self.Bind(wx.EVT_BUTTON,self.OnDelTag,self.delBtn)
        
        
        global sel
        sel = self._GetSelection()
        global page
        page = self._GetPageText()
        
        print sel
        print page
        
                                 
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        mainsizer.Add(self.addBtn,0,wx.ALIGN_RIGHT,5)
        mainsizer.Add(self.cmdpanel,1,wx.EXPAND,5)
        #mainsizer.Add(btsizer,0,wx.ALIGN_LEFT,5)
        

        self.SetSizer(mainsizer)
        mainsizer.Fit(self)
        #mainsizer.SetSizeHints(panel)
    def _GetSelection(self):
        
        selection = self.cmdpanel.GetSelection()
        return selection
    
    def _GetPageText(self):
        sel = self._GetSelection()
        pagetext = self.cmdpanel.GetPageText(sel)
        return pagetext
        
    def OnAddTag(self,event):
        self.subnb = CmdTagPanel(self.cmdpanel,self.target)
        self.cmdpanel.AddPage(self.subnb,'noname')
        self.cmdpanel.SetSelection(self.cmdpanel.GetSelection()+1)
    
    def OnDelTag(self,event):
        sel= self._GetSelection()
        page = self._GetPageText()
        page_cnt = self.cmdpanel.GetPageCount()
        dlg =wx.MessageDialog(self,'Do you real want to remove this page?','The Page Remove',style = wx.OK|wx.CANCEL|wx.ICON_WARNING)
        if dlg.ShowModal()== wx.ID_OK and page_cnt <= 1:
            dlg2 = wx.MessageDialog(self,'Because only one page,you can not remove this page!','Error',style = wx.OK|wx.CANCEL|wx.ICON_WARNING)
            dlg2.ShowModal()
            dlg2.Destroy()
        else:
            self.cmdpanel.RemovePage(sel)
            del rec['remote_configs'][self.target]['commands'][page]
            
            print page
            #rec.save()
       

########################################################################
class CmdTagPanel(wx.Panel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self,parent,target):
        """Constructor"""
        wx.Panel.__init__(self,parent)
        
        self.parent = parent
        self.target = target
        print self.parent.GetPageCount()

        self.name = wx.TextCtrl(self, -1, "")
        self.pathLbl = wx.StaticText(self, -1, "Path:")
        self.path = wx.TextCtrl(self, -1, "")
        
        self.name.Bind(wx.EVT_KILL_FOCUS,self.NameKillFocus,self.name)
        self.path.Bind(wx.EVT_KILL_FOCUS,self.PathKillFocus,self.path)
        
        self.listctrl = wx.ListCtrl(self,-1,style = wx.LC_REPORT|wx.LC_EDIT_LABELS)
        self.showlist()
        
        self.plusBtn = wx.Button(self,-1,"+",size=(22,15))
        self.minusBtn = wx.Button(self,-1,"-",size=(22,15))
        self.editBtn = wx.Button(self,-1,"Edit")
        
        self.Bind(wx.EVT_BUTTON,self.OnPlus,self.plusBtn)
        self.Bind(wx.EVT_BUTTON,self.OnMinus,self.minusBtn)
        self.Bind(wx.EVT_BUTTON,self.OnEdit,self.editBtn)
        
        self.mainsizer = wx.BoxSizer(wx.VERTICAL)
        sbsizer = wx.StaticBoxSizer(wx.StaticBox(self, -1, ''), orient=wx.VERTICAL)
        sbsizer_lc = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Environment'), orient=wx.VERTICAL)
        fgsizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        fgsizer.AddGrowableCol(1)
        fgsizer.Add(self.nameLbl, 0,
                    wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        fgsizer.Add(self.name,0,wx.EXPAND)
        #fgsizer.Add((-1,10),0)
        #fgsizer.Add((-1,10),0)

        fgsizer.Add(self.pathLbl, 0,
                    wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        fgsizer.Add(self.path,0,wx.EXPAND)
        
        sbsizer.Add(fgsizer,0,wx.EXPAND)
        sbsizer_lc.Add(self.listctrl,0,wx.EXPAND)
        
        btsizer = wx.BoxSizer(wx.HORIZONTAL)
        btsizer.Add(self.plusBtn,0,wx.EXPAND,5)
        btsizer.Add(self.minusBtn,0,wx.EXPAND,5)
        btsizer.Add(self.editBtn,0,wx.ALIGN_LEFT,5)
        

        self.mainsizer.Add(sbsizer,0, wx.EXPAND|wx.ALL, 5)
        #self.mainsizer.Add(wx.StaticLine(self), 0,
                           #wx.EXPAND|wx.TOP|wx.BOTTOM, 5)
        self.mainsizer.Add(sbsizer_lc,0,wx.EXPAND|wx.ALL,5)
        self.mainsizer.Add(btsizer,0,wx.ALIGN_LEFT,5)
        
        self.SetSizer(self.mainsizer)
    def showlist(self):
                  
        #self.sel= CmdSetPanel._GetSelection()
        #self.page = CmdSetPanel._GetPageText()
        #sel = sel
        #page = page
        
       # print 'sel',sel
        #print 'page',page
        self.listctrl.InsertColumn(0,'Variable',width = 150)
        self.listctrl.InsertColumn(1,'Value',width = 150)
        if rec['remote_configs'][self.target]['commands']['vlsn'].has_key('envs'):
            for key,val in rec['remote_configs'][self.target]['commands']['vlsn']['envs'].items():
                index = self.listctrl.InsertStringItem(0,key)
                self.listctrl.SetStringItem(index,1,str(val))
            
    def OnPlus(self,event): 
        #dlg = wx.Dialog(None, -1, title='Envs Setting Dialog',size =(300,300),style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.OK|wx.CANCEL)
        envs = EnvsPanel(None,self.target)
        if envs.ShowModal()==wx.ID_OK:
            index = self.listctrl.InsertStringItem(0,envs.variable.GetValue())
            self.listctrl.SetStringItem(index,1,envs.value.GetValue())
            rec['remote_configs'][self.target]['commands']['vlsn']['envs'][envs.variable.GetValue()]=envs.value.GetValue()
    def OnMinus(self,event): 
        envs = EnvsPanel(None,self.target)
        if envs.ShowModal()==wx.ID_OK:
            index = self.listctrl.DeleteStringItem(0,envs.variable.GetValue())
            #self.listctrl.SetStringItem(index,1,envs.value.GetValue())
            del ['remote_configs'][self.target]['commands']['vlsn']['envs'][envs.variable.GetValue()]
    def OnEdit(self,event):
        envs = EnvsPanel(None,self.target)
        
        
    def NameKillFocus(self,event):
        '''this method is set the pagetext'''
        self.sel = self.parent.GetSelection()
        if not len(self.name.GetValue())==0:
            self.parent.SetPageText(self.sel,self.name.GetValue())
            rec['remote_configs'][self.target]['commands'][self.name.GetValue()]=dict()
        
        
    def PathKillFocus(self,event):
        '''this method is set the path '''
        if not len(self.path.GetValue())==0:
            rec['remote_configs'][self.target]['commands']['vlsn']['path']=self.path.GetValue()
        
########################################################################
class EnvsPanel(wx.Dialog):
    """"""

    #----------------------------------------------------------------------
    def __init__(self,parent,target=''):

        wx.Dialog.__init__(self,parent,-1,size =(300,150))
            # create the controls
        
        self.variableLbl = wx.StaticText(self, -1, "Variable:")
        self.variable = wx.TextCtrl(self, -1, "")
        self.valueLbl = wx.StaticText(self, -1, "Value:")
        self.value = wx.TextCtrl(self, -1, "")
        
        self.okBtn = wx.Button(self, wx.ID_OK, "Ok")
        self.cancelBtn = wx.Button(self, wx.ID_CANCEL, "Cancel")
        """"""
        self.Dolayout()
    def Dolayout(self):
        self.mainsizer = wx.BoxSizer(wx.VERTICAL)
        sbsizer = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Envs Setting'), orient=wx.VERTICAL)
        fgsizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        fgsizer.AddGrowableCol(1)
        fgsizer.Add(self.variableLbl, 0,
                    wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        fgsizer.Add(self.variable,0,wx.EXPAND)
        
        fgsizer.Add(self.valueLbl, 0,
                    wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        fgsizer.Add(self.value,0,wx.EXPAND)       

        sbsizer.Add(fgsizer,0,wx.EXPAND)
        
        btsizer = wx.BoxSizer(wx.HORIZONTAL)
        btsizer.Add(self.okBtn,0,wx.ALIGN_RIGHT,5)
        btsizer.Add(self.cancelBtn,0,wx.ALIGN_RIGHT,5)
        self.mainsizer.Add(sbsizer,0,wx.EXPAND|wx.ALL,5)
        self.mainsizer.Add(btsizer,0,wx.ALIGN_RIGHT,5)
        self.SetSizer(self.mainsizer)
        self.SetAutoLayout(True)
        
        
    
    
    
    

if __name__ =='__main__':

    app = wx.App()
    frame = SettingDialog(None,-1,selection = 0,target = 'test')
    frame.Show()
    app.MainLoop()