#! /usr/bin/env python
#coding=utf-8
import wx
import sys

testlist = {1:('10001','2008-12-5',u'奇洋皮具专厅',u'厂发大厦-三楼东',u'晨鑫商贸','2 <-1>'),
            2:('10002','2009-01-12',u'百魅多内衣专厅',u'天都商厦-五楼',u'恒隆实业','1 <-1>'),
            3:('10003','2008-02-21',u'POOL专厅',u'人民商场-四楼',u'禾禾商贸','2 <-1>'),
            4:('10004','2008-03-02',u'老人头皮鞋专厅',u'盛世厂场-六楼',u'竹枷','4 <2>'),
            5:('10005','2008-03-15',u'金利来皮具专厅',u'威盛大厦-三楼',u'申城商贸','2 <1>'),
            6:('10006','2008-03-28',u'彬彬西服专厅',u'天都商厦-三楼',u'彬彬','-'),
            }

class myFrame(wx.Frame):
    def __init__(self,parent=None):

            wx.Frame.__init__(self,parent,-1,pos=wx.DefaultPosition,size=(820,450))
            self.Center(wx.BOTH)
            self.panel = wx.Panel(self)
            self.box = wx.BoxSizer(wx.VERTICAL)
            self.panel.SetSizer(self.box)
            self.listctl = wx.ListCtrl(self.panel,-1,style=wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES,size=(815,320))
            self.PopulateList()

    def PopulateList(self):
        ColLables = (u'序号', u'日期', u'项目名称', u'安装/施工地点', u'客户名', u'表单数')
        ColsWidth = (70,100,160,240,160,80)
        il = wx.ImageList(1,21, True)
        self.listctl.AssignImageList(il, wx.IMAGE_LIST_SMALL) 
        
        for i in xrange(len(ColLables)):
            self.listctl.InsertColumn(i, ColLables[i],wx.LIST_FORMAT_CENTRE)
            self.listctl.SetColumnWidth(i, ColsWidth[i])

        for key,data in testlist.items():
            index = self.listctl.InsertStringItem(key, data[0])#

            # Demos

            # import sys
            # index = self.listctl.InsertStringItem(sys.maxint, data[0])
            for col in xrange(len(data)-1):
                self.listctl.SetStringItem(index, col+1, data[col+1])
            self.listctl.SetItemData(index, key)

if __name__ == '__main__':
    class App(object):
        def __init__(self):
            self.wxApp = wx.App(0)
            self.init()
            self.wxApp.MainLoop()

        def init(self):
            self.frame = myFrame()
            self.frame.Show()

    App()
# end 
