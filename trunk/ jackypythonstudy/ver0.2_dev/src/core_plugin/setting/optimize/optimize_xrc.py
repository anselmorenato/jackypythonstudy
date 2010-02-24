# This file was automatically generated by pywxrc.
# -*- coding: UTF-8 -*-

import wx
import wx.xrc as xrc

__res = None

def get_resources():
    """ This function provides access to the XML resources in this module."""
    global __res
    if __res == None:
        __init_resources()
    return __res




class xrcOptimize(wx.Panel):
#!XRCED:begin-block:xrcOptimize.PreCreate
    def PreCreate(self, pre):
        """ This function is called during the class's initialization.
        
        Override it for custom setup before the window is created usually to
        set additional window styles using SetWindowStyle() and SetExtraStyle().
        """
        pass
        
#!XRCED:end-block:xrcOptimize.PreCreate

    def __init__(self, parent):
        # Two stage creation (see http://wiki.wxpython.org/index.cgi/TwoStageCreation)
        pre = wx.PrePanel()
        self.PreCreate(pre)
        get_resources().LoadOnPanel(pre, parent, "Optimize")
        self.PostCreate(pre)

        # Define variables for the controls, bind event handlers





# ------------------------ Resource data ----------------------

def __init_resources():
    global __res
    __res = xrc.EmptyXmlResource()

    wx.FileSystem.AddHandler(wx.MemoryFSHandler())

    optimize_xrc = '''\
<?xml version="1.0" ?><resource>
  <object class="wxPanel" name="Optimize">
    <object class="wxBoxSizer">
      <orient>wxVERTICAL</orient>
      <object class="sizeritem">
        <object class="wxNotebook" name="ID_MultiBook">
          <object class="notebookpage">
            <object class="wxPanel" name="Input"/>
            <label>Input</label>
          </object>
          <object class="notebookpage">
            <object class="wxPanel" name="Output"/>
            <label>Output</label>
          </object>
        </object>
        <option>1</option>
        <flag>wxALL|wxEXPAND|wxGROW</flag>
        <border>5</border>
      </object>
    </object>
    <size>600, 800</size>
  </object>
</resource>'''

    wx.MemoryFSHandler.AddFile('XRC/optimize/optimize_xrc', optimize_xrc)
    __res.Load('memory:XRC/optimize/optimize_xrc')
