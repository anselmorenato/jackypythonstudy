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




class xrcAmberView(wx.Panel):
#!XRCED:begin-block:xrcAmberView.PreCreate
    def PreCreate(self, pre):
        """ This function is called during the class's initialization.
        
        Override it for custom setup before the window is created usually to
        set additional window styles using SetWindowStyle() and SetExtraStyle().
        """
        pass
        
#!XRCED:end-block:xrcAmberView.PreCreate

    def __init__(self, parent):
        # Two stage creation (see http://wiki.wxpython.org/index.cgi/TwoStageCreation)
        pre = wx.PrePanel()
        self.PreCreate(pre)
        get_resources().LoadOnPanel(pre, parent, "AmberView")
        self.PostCreate(pre)

        # Define variables for the controls, bind event handlers





# ------------------------ Resource data ----------------------

def __init_resources():
    global __res
    __res = xrc.EmptyXmlResource()

    wx.FileSystem.AddHandler(wx.MemoryFSHandler())

    amber_xrc = '''\
<?xml version="1.0" ?><resource>
  <object class="wxPanel" name="AmberView">
    <object class="wxBoxSizer">
      <orient>wxVERTICAL</orient>
      <object class="sizeritem">
        <object class="wxStaticBoxSizer">
          <object class="sizeritem">
            <object class="wxGridSizer">
              <object class="sizeritem">
                <object class="wxStaticText">
                  <label>input file :</label>
                </object>
              </object>
              <object class="sizeritem">
                <object class="wxFilePickerCtrl" name="input_file"/>
                <option>1</option>
                <flag>wxEXPAND</flag>
              </object>
              <object class="sizeritem">
                <object class="wxStaticText">
                  <label>log file : </label>
                </object>
              </object>
              <object class="sizeritem">
                <object class="wxFilePickerCtrl" name="log_file"/>
                <option>1</option>
                <flag>wxEXPAND</flag>
              </object>
              <object class="sizeritem">
                <object class="wxStaticText">
                  <label>parameter file(*.prmtop) : </label>
                </object>
              </object>
              <object class="sizeritem">
                <object class="wxFilePickerCtrl" name="prmtop_file"/>
                <option>1</option>
                <flag>wxEXPAND</flag>
              </object>
              <object class="sizeritem">
                <object class="wxStaticText">
                  <label>restart coordinate : </label>
                </object>
              </object>
              <object class="sizeritem">
                <object class="wxFilePickerCtrl" name="restart_file"/>
                <option>1</option>
                <flag>wxEXPAND</flag>
              </object>
              <object class="sizeritem">
                <object class="wxStaticText">
                  <label>output restart file : </label>
                </object>
              </object>
              <object class="sizeritem">
                <object class="wxFilePickerCtrl" name="out_restart_file"/>
                <option>1</option>
                <flag>wxEXPAND</flag>
              </object>
              <object class="sizeritem">
                <object class="wxStaticText">
                  <label>trajectory file : </label>
                </object>
              </object>
              <object class="sizeritem">
                <object class="wxFilePickerCtrl" name="crds_file"/>
                <option>1</option>
                <flag>wxEXPAND</flag>
              </object>
              <object class="sizeritem">
                <object class="wxStaticText">
                  <label>energy file : </label>
                </object>
                <option>1</option>
                <flag>wxEXPAND</flag>
              </object>
              <object class="sizeritem">
                <object class="wxFilePickerCtrl" name="energies_file"/>
              </object>
              <object class="sizeritem">
                <object class="wxStaticText">
                  <label>velocity file : </label>
                </object>
              </object>
              <object class="sizeritem">
                <object class="wxFilePickerCtrl" name="vels_file"/>
                <option>1</option>
                <flag>wxEXPAND</flag>
              </object>
              <cols>2</cols>
              <rows>2</rows>
              <vgap>5</vgap>
            </object>
          </object>
          <label>setting</label>
          <orient>wxVERTICAL</orient>
        </object>
        <option>0</option>
        <flag>wxALL</flag>
        <border>5</border>
      </object>
      <object class="sizeritem">
        <object class="wxStaticBoxSizer">
          <object class="sizeritem">
            <object class="wxButton" name="run_Amber">
              <label>run</label>
            </object>
            <option>0</option>
            <flag>wxALL</flag>
            <border>5</border>
          </object>
          <object class="sizeritem">
            <object class="wxGauge" name="run_guage"/>
            <option>1</option>
            <flag>wxALL|wxEXPAND</flag>
            <border>5</border>
          </object>
          <label>run</label>
          <orient>wxHORIZONTAL</orient>
        </object>
        <option>0</option>
        <flag>wxALL|wxEXPAND</flag>
        <border>5</border>
      </object>
      <object class="sizeritem">
        <object class="wxStaticBoxSizer">
          <object class="sizeritem">
            <object class="wxButton" name="view_config">
              <label>view config</label>
            </object>
            <option>0</option>
            <flag>wxALL|wxEXPAND</flag>
            <border>5</border>
          </object>
          <object class="sizeritem">
            <object class="wxButton" name="view_remotelog">
              <label>view remote config</label>
            </object>
            <option>0</option>
            <flag>wxALL</flag>
            <border>5</border>
          </object>
          <label>logview</label>
          <orient>wxHORIZONTAL</orient>
        </object>
        <option>0</option>
        <flag>wxALL|wxEXPAND|wxALIGN_RIGHT</flag>
        <border>5</border>
      </object>
    </object>
  </object>
</resource>'''

    wx.MemoryFSHandler.AddFile('XRC/amber/amber_xrc', amber_xrc)
    __res.Load('memory:XRC/amber/amber_xrc')
