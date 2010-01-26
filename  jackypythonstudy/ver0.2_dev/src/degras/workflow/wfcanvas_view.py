# _*_ coding: utf-8 _*_
# Copyright (C)  2010 Biao Ma

# standard modules
import wx
import wx.lib.ogl as ogl
import os,sys

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )

class WorkFlowCanvasView(ogl.ShapeCanvas):
    # def __init__(self, parent, log, frame):
    def __init__(self, parent):
        ogl.ShapeCanvas.__init__(self, parent)
        ogl.OGLInitialize()
        maxWidth  = 1500
        maxHeight = 1500
        self.SetScrollbars(20, 20, maxWidth/20, maxHeight/20)

        #self.log = log
        # self.frame = frame
        self.SetBackgroundColour("light blue") #wx.WHITE)
        self.diagram = ogl.Diagram()
        self.SetDiagram(self.diagram)
        self.diagram.SetCanvas(self)
        self.shapes = []
        self.save_gdi = []
        self.lines = []
        # define dict
        self.item_dict = {}
    def make_popmenu(self):
        """creat the popupmenu when right click on shape."""
        deleteID = wx.NewId()
        
        popmenu = wx.Menu()
        item_delete =popmenu.Append(deleteID,'Delete')
        self.item_dict['delete'] = (deleteID, item_delete)
        self.Bind(wx.EVT_MENU,self.on_delete_shape)
        
        self.PopupMenu(popmenu)
        popmenu.Destroy()
        
    def make_popmenu_2(self):
        """ creat the popup menu when right click on canvas(not on shape)."""
        
        from degras.frame.menubar_view import MenubarView
        mv = MenubarView()
        mv.init_workflow_menu()
        menu = mv.get_menu('Workflow')
        self.PopupMenu(menu)
        menu.Destroy()
        
    def selected_shape(self): 
        
        return self.__selected_shape
    def on_select(self,event):
        pass 
class WorkFlowCanvasInteractor(object):
    def __init__(self, view, presenter): 
        self.view = view
        self.presenter = presenter
        
        view.Bind(wx.EVT_RIGHT_DOWN,self.on_right)
        view.Bind(wx.EVT_MOTION,self.on_motion)
        view.Bind(wx.EVT_KEY_DOWN,self.on_key_press)
        #view.Bind(wx.EVT_MENU,self.on_delete_shape,view.item_dict['deltet'])
        
    def on_right(self,event):
        print 'on right at canvs'
        self.presenter.popup(event)
    def on_motion(self,event):
        pass
    def on_key_press(self,event):
        self.presenter.key_press()
    def on_delete_shape(self,event):
        self.presenter.delete()
        
    