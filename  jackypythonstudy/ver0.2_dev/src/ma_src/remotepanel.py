#! /opt/python2.6/bin/python
#  -*- encoding: utf-8 -*-

import os 
import wx
#import htlpanel 
import wx.lib.agw.hypertreelist as HTL
import dict4ini as d4i
dirName = os.path.dirname(os.path.abspath(__file__))
if os.path.isfile(dirName+'\remote_config.ini')==False:
    import makeini

rec = d4i.DictIni('remote_config.ini')
remote_configs = d4i.DictIni('remote_config.ini').remote_configs._items
        
        self.CreateTreeList()
        
    def OnOk(self, event): 
        rec.save()
        self.parent.Close()
        
    def OnApply(self, event):
                
        self.tree.DeleteAllItems()
        rec = d4i.DictIni('remote_config.ini')
        remote_configs = rec.remote_configs._items
        sel = self.listbox.GetSelection()
        self.root = self.tree.AddRoot(self.listbox.GetString(sel))
        
        self.AddTreeNodes(self.root, remote_configs[self.listbox.GetString(sel)])
        
        self.tree.ExpandAll(self.tree.GetRootItem())
        self.tree.SetItemText(self.root, "Description", 1)
      
        rec.save()
        
    def OnCancel(self,event):
        self.GetParent().Close(True)
    
    #----------------------------------------------------------------------
    # Create the event hander for Edit Buttons
    def OnAddNewListItem(self,event):
        selection = self.listbox.GetSelection()
        dlg = wx.TextEntryDialog(self,'Please enter the item name you want to add!','Add the new item','new')
        if dlg.ShowModal()== wx.ID_OK:
            if selection ==-1: # If all items had deleted,the selection == -1
                self.listbox.Insert(dlg.GetValue(),selection+1)
                self.listbox.Select(selection+1)
            else:
                self.listbox.Insert(dlg.GetValue(),selection)
                self.listbox.Select(selection)
            rec['remote_configs'][dlg.GetValue()] = dict()
            #rec.save()
            self.listbox.Refresh()
        dlg.Destroy()
    def OnEditListItem(self,event):
        selection = self.listbox.GetSelection()
        
        if selection == -1: # If no item selected, the selection == -1
            dlg = wx.MessageDialog(self,'Error! No item is selected!','Error',style = wx.OK|wx.ICON_ERROR)
            dlg.ShowModal()
        else:
            dlg = wx.TextEntryDialog(self,'Please enter the new item name!',' The Item Edit',self.listbox.GetString(selection))
            if dlg.ShowModal()== wx.ID_OK:
                self.listbox.SetString(selection, dlg.GetValue()) 
                #self.listbox.Insert(dlg.GetValue(),selection)
                #self.listbox.Delete(selection+1)
                #self.listbox.Select(selection)
                rec['remote_configs'][self.listbox.GetString(selection)]=rec['remote_configs'][dlg.GetValue()] = dict()
                #rec.save()
                dlg.Destroy()
    def OnCopyListItem(self,event):
        selection = self.listbox.GetSelection()
        self.listbox.Insert(self.listbox.GetString(selection),selection)
        self.listbox.Select(selection)
    def OnDeleteListItem(self,event):
        selection = max(0,self.listbox.GetSelection())
        if selection > self.listbox.GetCount():
            selection = selection-1
        dlg =wx.MessageDialog(self,'Do you real want to delete this item?','The Item Delete',style = wx.OK|wx.CANCEL|wx.ICON_WARNING)
        if dlg.ShowModal()== wx.ID_OK:
            del rec['remote_configs'][self.listbox.GetString(selection)]
            self.listbox.Delete(selection)
            
            #rec.save()
            if selection+1 > self.listbox.GetCount():
                self.listbox.Select(selection-1)
            else:
                self.listbox.Select(selection)
            
    # Create the event handers for listbox
    def EvtListBoxDClick(self,event):
        '''this method is to eject the setting dialog when doulue click the listitem'''
        lb = event.GetEventObject()
        selection = lb.GetSelection()
        sel_string = event.GetString()
        
    
        import settingdlg
        dlg = settingdlg.SettingDialog(None,-1,selection=selection,target = sel_string)
        dlg.Show()
        event.Skip()
    def EvtListBox(self,event):
        
        
        rec = d4i.DictIni('remote_config.ini')
        remote_configs = d4i.DictIni('remote_config.ini').remote_configs._items

        #change the ItemText of root
        _root = self.tree.GetRootItem()
        _str = event.GetString()
        #_item = remote_configs[str(_str)]
        self.tree.SetItemText(_root,_str)
        #self.AddTreeNodes(self.tree.GetRootItem(),remote_configs[event.GetString()])
        if remote_configs.has_key(event.GetString())==True and type(remote_configs[event.GetString()])==str:
            self.tree.SetItemText(self.tree.GetRootItem(),remote_configs[event.GetString()],1)
        else:
            self.tree.SetItemText(self.tree.GetRootItem(),event.GetString(),1)
        
        if self.tree.HasChildren(self.tree.GetRootItem())==True:
            self.tree.DeleteChildren(self.tree.GetRootItem())
            if remote_configs.has_key(event.GetString())==True and type(remote_configs[event.GetString()])==dict:
                self.AddTreeNodes(self.tree.GetRootItem(),remote_configs[event.GetString()])
                self.tree.ExpandAll(self.tree.GetRootItem())
        elif remote_configs.has_key(event.GetString())==True and type(remote_configs[event.GetString()])==dict:
            self.AddTreeNodes(self.tree.GetRootItem(),remote_configs[event.GetString()])
            self.tree.ExpandAll(self.tree.GetRootItem())

        
        
                
def main():
    app = wx.App()
    frame = wx.Frame(None, -1, '')


    dlg = wx.Dialog(frame, -1, title='Remote Setting Dialog',size =(500,500),style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
    remote = RemotePanel(dlg,log=False)

    #dlg.SetSize(dlg.GetBestSize())
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(remote,1,wx.EXPAND)
    dlg.SetSizer(sizer)
    #sizer.Fit(dlg)
    #dlg.SetAutoLayout(True)
    dlg.ShowModal()
    dlg.Destroy()                

    try:
        app.MainLoop()
    except:
        app.RedirectStdio()


if __name__ == '__main__':
    main()
    
   
    
       
