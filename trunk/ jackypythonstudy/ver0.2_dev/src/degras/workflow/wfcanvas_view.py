# _*_ coding: utf-8 _*_
# Copyright (C)  2010 Biao Ma

# standard modules
import wx
import wx.lib.ogl as ogl
import os,sys

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from degras.frame.menubar_view import MenubarView
import datapiece_view as data
from utils.event import NagaraEvent
from core.exception import NagaraException, DialogCancelException

class CtrlNotFoundError(NagaraException): pass

from  utils.wxutils import BindManager    
    
class WorkFlowCanvasInteractor(object):
    binder = BindManager()
    def __init__(self, view, presenter): 
        self.view = view
        self.presenter = presenter
        self.binder.bindAll(view, self)
        mv =MenubarView()
        
        
        view.Bind(wx.EVT_RIGHT_DOWN,self.on_right)
        view.Bind(wx.EVT_MOTION,self.on_motion)
        view.Bind(wx.EVT_KEY_DOWN,self.on_key_press)
        #view.Bind(wx.EVT_MENU,self.on_delete_shape,view.item_dict['deltet'])
        view.Bind(wx.EVT_MENU,self.on_add_data,id=mv.get_item('workflow:add_data')[0])
        print mv.get_item('workflow:add_data')[0]
        #view.Bind(wx.EVT_MENU,self.on_add_task,mv.get_item('Energy'))
        
    def on_right(self,event):
        x,y = event.GetPosition()
        print 'right click at canvs',x,y
        self.presenter.popup(event)
        event.Skip(True)
    def on_motion(self,event):
        event.Skip(True)
        
    def on_key_press(self,event):
        self.presenter.key_press(event)
        event.Skip(True)
    def on_delete_shape(self,event):
        self.presenter.delete()
        
    def on_add_data(self,event):
        #x,y = event.GetEventObject().GetPosition()
        id = event.GetID()
        shape = data.DataPieceView(self.view)
        #shape = ogl.CircleShape(10)
        #self.view.diagram.AddShape(shape)
        #shape.Show(True)
        self.presenter.add_shape(shape,x=50,y=50)
        self.view.shapes.append(shape)
        self.view.Refresh()
        print 'Ok',id
        event.Skip(True)
        
    def on_add_task(self,event):
        print ' add task ok'
        
   # @binder(wx.EVT_MENU, id='ID_delete')
    def h1(self, event):
        self.presenter.delete()
        
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
        self.__idctrl_dict = {}
    def make_popmenu(self):
        """creat the popupmenu when right click on shape."""
        self.popmenu = wx.Menu()
        self.__idctrl_dict['ID_delete'] = deleteID = wx.NewId()
        print self.__idctrl_dict
        self.popmenu.Append(deleteID,'Delete')
        #self.item_dict['delete'] = (deleteID, item_delete)
        #self.Bind(wx.EVT_MENU,self.on_delete)
        
        self.PopupMenu(self.popmenu)
        self.popmenu.Destroy()
        
    def make_popmenu_2(self):
        """ creat the popup menu when right click on canvas(not on shape)."""
        
        
        mv = MenubarView()
        mv.init_workflow_menu()
        menu = mv.get_menu('Workflow')
        self.PopupMenu(menu)
        menu.Destroy()
        
    def selected_shape(self): 
        
        return self.__selected_shape
    def on_select(self,event):
        pass 
    def on_delete(self,event):
        pass

    def getCtrl(self, ctrl_name):
        ctrl = self.FindWindowByName(ctrl_name)
        if not ctrl:
            raise CtrlNotFoundError(ctrl_name)
        return ctrl

    def getCtrlById(self, id_ctrl_name):
        id_ctrl = self.__idctrl_dict.get(id_ctrl_name)
        if not id_ctrl:
            raise CtrlNotFoundError(id_ctrl_name)
        return id_ctrl

    def getCtrlNames(self):
        for ctrl in self.GetChildren():
            if ctrl.GetName().startswith('ID_'):
                yield ctrl.GetName()

        for menuitem in self.__menu.GetMenuItems():
            print menuitem.GetLabel()

    def getCtrlIdList(self):
        return self.__idctrl_dict.keys()
    
if __name__ == '__main__':
     
    app = wx.App(redirect=False)
    frame = wx.Frame(None, -1, 'Work Flow Canvas')

    wfc = WorkFlowCanvasView( frame )
    from  wfcanvas_presenter import WorkFlowCanvasPresenter
    presenter = WorkFlowCanvasPresenter(view=wfc)
    interactor = WorkFlowCanvasInteractor(wfc,presenter)

    frame.Show()
    app.MainLoop()