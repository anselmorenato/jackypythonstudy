#! /opt/python2.6/bin/python
#  -*- encoding: utf-8 -*-
# Copyright (C)  2009 Ma and Ishikura
import os, sys

import wx
import dict4ini as d4i

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
