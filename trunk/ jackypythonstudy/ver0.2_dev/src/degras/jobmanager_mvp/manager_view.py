#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura
#
# $Date$
# $Rev$
# $Author$
#

# standard modules
import os, sys
import wx

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from utils.event import NagaraEvent
from core.exception import NagaraException

class ManagerInteractor(object):
    
    def __init__(self, view, presenter):
        joblist = view.get_joblist()

        joblistctrl.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)

    def on_left_down(self, event):
        self.presenter.pupup_jobmenu()

    def on_submit(self, event):
        self.presenter.request_submit()

    def on_convert(self, event):
        self.presenter.request_convert()
    
    def on_send(self, event):
        self.presenter.request_send()

    def on_run(self, event):
        self.presenter.request_run()

    def on_stop(self, event):
        self.presenter.request_stop()

    def on_cancel(self, event):
        self.presenter.request_cancel()

    def on_rerun(self, event):
        self.presenter.request_rerun()

    def on_receive(self, event):
        self.presenter.request_receive()

    def on_sync(self, event):
        self.presenter.request_sync()

    def on_delete(self, event):
        self.presenter.delete_job()

    def on_update(self, event):
        self.presenter.update_view()

    def on_rename(self, event):
        self.presenter.rename()

    

class JobManagerError(NagaraException): pass

class JobListCtrl(wx.ListCtrl):

    def __init__(self, *args, **kwds):
        wx.ListCtrl.__init__(self, *args, **kwds)
    

class ManagerView(wx.Panel):
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
        self.__delete_event   = NagaraEvent()
        self.__rename_event   = NagaraEvent()
        self.__select_event   = NagaraEvent()
        self.__set_auto_event = NagaraEvent()
        self.__update_event   = NagaraEvent()

    # events
    @property
    def rename_event(self):
        return self.__rename_event

    @property
    def operate_event(self):
        return self.__operate_event

    @property
    def select_event(self):
        return self.__select_event

    @property
    def set_auto_event(self):
        return self.__set_auto_event

    @property
    def update_event(self):
        return self.__update_event

    # auto
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
    def append_old(self, job):
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

    def append_row(self, label):
        """Append new row item."""
        nrow = self.__job_listctrl.GetItemCount()
        self.__job_listctrl.InsertStringItem(nrow, str(label))
        return nrow

    def append_col(self, irow, icol, label, image=None):
        """Append item for column."""
        if image:
            num_image = self.__image_list.GetImageCount()
            if num_image+1 == irow:
                self.__image_list.Add(image)
            elif num_image >= irow:
                self.__image_list.Replace(irow, image)
            else:
                raise JobManagerError(
                    'irow: {0}, num_image:{1}'.format(irow, num_image))
            self.__job_listctrl.SetStringItem( irow, icol, str(label), irow )
        else:
            self.__job_listctrl.SetStringItem( irow, icol, str(label) )


    def clear(self):
        self.__stateimg_list.RemoveAll()
        self.__job_listctrl.ClearAll()

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
