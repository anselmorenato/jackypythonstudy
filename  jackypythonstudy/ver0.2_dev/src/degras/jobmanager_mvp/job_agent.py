#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura
#
# $Date: 2010-01-20 13:52:45 +0900 (水, 20 1 2010) $
# $Rev: 54 $
# $Author: ishikura $
#
import os, sys


class JobAgent(object):

    def __init__(self, job):

        from job_presenter import JobPresenter
        from job_view import JobView, JobInteractor

        view       = JobView()
        presen     = JobPresenter(job, view)
        interactor = JobInteractor(view, presen)

        self.__view = view

    def get_menu(self):
        return self.__view.get_menu()

    def get_state(self):
        return self.__view.get_state()

    def get_view(self):
        return self.__view

if __name__ == '__main__':
    import wx
    app = wx.App(redirect=False)
    
    from tests.jobmock import JobMock
    job = JobMock(10)
    a = JobAgent(job)

    menu = a.get_menu()
    print menu

