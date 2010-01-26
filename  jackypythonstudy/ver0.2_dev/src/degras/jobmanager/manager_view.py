#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura
#
# $Date: 2010-01-20 14:50:42 +0900 (水, 20 1 2010) $
# $Rev: 60 $
# $Author: ishikura $
#

# standard modules
import os, sys
import wx

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from utils.event import NagaraEvent
from core.exception import NagaraException

class JobManagerError(NagaraException): pass

class JobListCtrl(wx.ListCtrl):

    def __init__(self, *args, **kwds):
        wx.ListCtrl.__init__(self, *args, **kwds)
    

from interfaces.imanager_view import IManagerView
class ManagerView(IManagerView, wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)

        self.__job_listctrl = JobListCtrl(
            self, style = wx.LC_REPORT | wx.LC_HRULES , 
            #self, style = wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES , 
        )

        # create and set sizer
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.__job_listctrl, 1, wx.EXPAND)
        self.SetSizer(sizer)

        # set column
        column_list = [
             ('Job ID'  , wx.LIST_FORMAT_LEFT), # wx.LIST_FORMAT_RIGHT
             ('Name'    , wx.LIST_FORMAT_LEFT), 
             ('Status'  , wx.LIST_FORMAT_LEFT), # wx.LIST_FORMAT_CENTRE
             ('Location', wx.LIST_FORMAT_LEFT), 
             ('Start'   , wx.LIST_FORMAT_LEFT), # wx.LIST_FORMAT_RIGHT
             ('Expected', wx.LIST_FORMAT_LEFT), # wx.LIST_FORMAT_RIGHT
             ('Elasped' , wx.LIST_FORMAT_LEFT), # wx.LIST_FORMAT_RIGHT
             ('Finish'  , wx.LIST_FORMAT_LEFT), # wx.LIST_FORMAT_RIGHT
             ('Project' , wx.LIST_FORMAT_LEFT), 
             ('JMS'     , wx.LIST_FORMAT_LEFT), 
        ]
        for icol, (name, style) in enumerate(column_list):
            self.__job_listctrl.InsertColumn(icol, name, style)
            self.__job_listctrl.SetColumnWidth(icol, -2)

        # assign image list
        self.__image_list = wx.ImageList(16,16)
        self.__job_listctrl.AssignImageList(
            self.__image_list, wx.IMAGE_LIST_SMALL)

        # job request menu
        self.__job_listctrl.Bind(wx.EVT_LEFT_DOWN, self.on_popup_jobmenu)

        # define properties
        self.__is_auto = True

        # generate events
        self.__cancel_event   = NagaraEvent()
        self.__convert_event  = NagaraEvent()
        self.__delete_event   = NagaraEvent()
        self.__receive_event  = NagaraEvent()
        self.__rename_event   = NagaraEvent()
        self.__operate_event  = NagaraEvent()
        self.__rerun_event    = NagaraEvent()
        self.__run_event      = NagaraEvent()
        self.__select_event   = NagaraEvent()
        self.__send_event     = NagaraEvent()
        self.__set_auto_event = NagaraEvent()
        self.__stop_event     = NagaraEvent()
        self.__submit_event   = NagaraEvent()
        self.__sync_event     = NagaraEvent()
        self.__update_event   = NagaraEvent()

    # events
    @property
    def cancel_event(self):
        return self.__cancel_event

    @property
    def convert_event(self):
        return self.__convert_event

    @property
    def delete_event(self):
        return self.__delete_event

    @property
    def receive_event(self):
        return self.__receive_event

    @property
    def rename_event(self):
        return self.__rename_event

    @property
    def operate_event(self):
        return self.__operate_event

    @property
    def rerun_event(self):
        return self.__rerun_event

    @property
    def run_event(self):
        return self.__run_event

    @property
    def select_event(self):
        return self.__select_event

    @property
    def send_event(self):
        return self.__send_event

    @property
    def set_auto_event(self):
        return self.__set_auto_event

    @property
    def stop_event(self):
        return self.__stop_event

    @property
    def submit_event(self):
        return self.__submit_event

    @property
    def sync_event(self):
        return self.__sync_event

    @property
    def update_event(self):
        return self.__update_event

    # enables
    def enable_auto(self, enable=True):
        self.__auto = enable
    def is_auto(self):
        return self.__is_auto
    def on_check_auto(self, event):
        #pos = event.GetItem()
        pos = event.GetPosition()
        col, row = self.get_col_row_by_pos(pos)
        self.set_auto_event()

    # methods
    def append(self, job):
        m, v, p = job
        
        # append_job_info
        num_job = self.__job_listctrl.GetItemCount()
        
        # append new row
        self.__job_listctrl.InsertStringItem(num_job, str(m.id))

        append_col = self.__job_listctrl.SetStringItem
        append_col(num_job, 1, str(m.name) ) 
        state, image = v.get_state()
        self.__image_list.Add( image )
        num_image = self.__image_list.GetImageCount()
        if num_job+1 != num_image:
            raise JobManagerError('{0} != {1}'.format(num_job+1, num_image))

        append_col( num_job, 2,  str(state),  num_job      ) 
        append_col( num_job, 3 , str(m.location     ))
        append_col( num_job, 4 , str(m.start_time   ))
        append_col( num_job, 5 , str(m.expected_time))
        append_col( num_job, 6 , str(m.elasped_time ))
        append_col( num_job, 7 , str(m.finish_time  ))
        append_col( num_job, 8 , str(m.project      ))
        append_col( num_job, 9 , str(m.jms          ))

    def update_all(self, jobmodel_list):

        # clear job view info
        self.__menu_list = []
        self.__stateimg_list.RemoveAll()

        # update job view and job info
        for jobmodel  in jobmodel_list:
            self.append_job( jobmodel )

    def get_selected_jobid_list(self):
        pass

    def get_jobname(self):
        pass

    def on_popup_jobmenu(self, event):
        #item = event.GetItem()
        #icol = item.GetColumn()
        #irow = item.GetId()
        pos = event.GetPosition()
        icol, irow = self.get_col_row_by_pos(pos)
        if irow == -1:
            pass
        elif icol == 2:
            item = self.__job_listctrl.GetItem(irow, 0)
            id = int(item.GetText())
            self.operate_event.fire(id)
        else:
            pass

    def popup_jobmenu(self, menu):
        self.__job_listctrl.PopupMenu( menu )

    def get_col_row_by_pos(self, pos):
        x, y = pos
        row,flags = self.__job_listctrl.HitTest(pos)
        # if row != self.curRow: # self.curRow keeps track of the current row
        #     evt.Skip()
        #     return
        col_locs = [0]
        loc = 0
        for n in range(self.__job_listctrl.GetColumnCount()):
            loc = loc + self.__job_listctrl.GetColumnWidth(n)
            col_locs.append(loc)
        
        from bisect import bisect
        col = bisect(
            col_locs, x+self.__job_listctrl.GetScrollPos(wx.HORIZONTAL)) - 1
        return col, row


if __name__ == '__main__':
    app = wx.App(redirect=False)
    frame = wx.Frame(None, -1, 'Job ListCtrl')
    managerview = ManagerView(frame)

    # create JobView
    from job_view import JobView
    from job_model import JobModel
    from tests.jobmock import JobMock
    job = JobMock(1)

    jobview = JobView()
    # set properties
    init_prop_dict = dict(
        id            = 5           , 
        expected_time = '3:00'      , 
        start_time    = '15:00'     , 
        elasped_time  = '1:00'      , 
        finish_time   = ''          , 
        location      = 'hpcs'      , 
        jms           = 'LSF'       , 
        name          = 'test job'  , 
        project       = 'project X' , 
    )

    for prop, val in init_prop_dict.items():
        set_prop = 'set_'+prop
        get_prop = 'get_'+prop
        getattr(jobview, set_prop)( val )

    # set state
    jobview.set_state( 'Runnable' )

    # set popup menu
    init_request_dict = dict(
        request_submit  = False , 
        request_convert = False , 
        request_send    = False , 
        request_run     = True  , 
        request_stop    = True  , 
        request_cancel  = True  , 
        request_rerun   = False , 
        request_receive = False , 
        request_sync    = False , 
    )
    jobview.set_request_dict( init_request_dict )

    managerview.append(jobview)
    managerview.append(jobview)
    managerview.append(jobview)
    managerview.append(jobview)
    managerview.append(jobview)
    managerview.append(jobview)

    frame.Show()

    app.MainLoop()

    #view.update_all( [jobview] )
