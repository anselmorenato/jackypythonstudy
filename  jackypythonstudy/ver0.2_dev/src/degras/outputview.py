# _*_ coding: utf-8 _*_
# Copyright (C)  2009 Takakazu Ishikura

import wx

#-------------------------------------------------------------------------------

class OutputView(wx.Panel):

    """
    Log View Class.
    """

    def __init__(self, parent, log=None):
        """Constructor."""
        wx.Panel.__init__(self, parent, -1)

        self._log = log

        # initilize
        self.parent = parent
        self.initView()

        if __debug__:
            self.log('loding log view panel... ')

        # self.setLogTarget()

    def log(self, message):
        if self._log: self._log.write(message)

    def __del__(self):
        """Destructor."""
        self.logfile.close()

    def initView(self):
        """Init the Log View."""
        self.output_ctrl = wx.TextCtrl(self, -1,
                                    style=wx.TE_MULTILINE|wx.TE_READONLY)
        sizer = wx.BoxSizer()
        sizer.Add(self.output_ctrl, 1, wx.EXPAND)
        self.SetSizer(sizer)

    # def setLogTarget(self, use_timestamp=True):
    #     """Set the log target to text_ctrl."""
    #     if use_timestamp:
    #         wx.Log.SetActiveTarget(wx.LogTextCtrl(self.output_ctrl))
    #     else:
    #         wx.Log.SetActiveTarget(wx.LogTextCtrl(self.output_ctrl))

    def write(self, output):
        """Print out the log message to the target."""
        self.output_ctrl.AppendText(str(output))

    # def writeDate(self):
    #     """Print out a current date."""
    #     import datetime
    #     datestr = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    #     message = (
    #         '\n\n'
    #         '=====<< ' + datestr 
    #         + ' >>==================================================\n'
    #     )
    #     self.logfile.write(message)

    # def printError(self, message='',prompt=False, level='info'):
    #     """Print out the log message with level info to the target."""
    #     print_log = dict(
    #         debug    = wx.LogDebug,
    #         error    = wx.LogError,
    #         info     = wx.LogInfo,
    #         message  = wx.LogMessage,
    #         status   = wx.LogStatus,
    #         syserror = wx.LogSysError,
    #         verbose  = wx.LogVerbose,
    #         warning  = wx.LogWarning,
    #         fatal    = wx.LogFatalError
    #     )
    #     print_log[level](message)

    #     if prompt:
    #         print_log[level](self.prompt + message)
    #     else:
    #         print_log[level](message)

    # def setPrompt(self, prompt='>> '):
    #     """Set a prompt string."""
    #     self.prompt = prompt

#-------------------------------------------------------------------------------

class LogTextCtrl(wx.PyLog):
    def __init__(self, text_ctrl, log_time=False):
        """Constructor."""
        wx.Pylog.__init__(self)
        self.output_ctrl = text_ctrl
        self.logTime = log_time
        self.DoLogString(self.__class__.__name__ + '>')

    def DoLogString(self, message, timeStamp):
        """ print message, timeStamp
        """
       #if self.logTime:
       #    message = time.strftime('%X', time.localtime(timeStamp)) + \
       #            ': ' + message
        if self.tc:
            self.output_ctrl.AppendText(message + '\n')

#-------------------------------------------------------------------------------

class OutputDlg(wx.Dialog):
    def __init__(self, parent=None):
        wx.Dialog.__init__(self, parent, -1, 'log dialog', size=(500,500))

        self.outputview = OutputView(self)
        sizer = wx.BoxSizer()
        sizer.Add(self.outputview, 1, wx.EXPAND)
        self.SetSizer(sizer)
        # self.showDlg()

    def write(self, output):
        self.outputview.write(output)

    def show(self):
        self.ShowModal()
        # self.Destroy()

#-------------------------------------------------------------------------------

def _test():
    import doctest
    doctest.testmod()

def main():
    logfile =  "_error.log"
    app = wx.App(redirect=False, filename=logfile)
    frame = wx.Frame(None, -1, "TestFrame")
    # panel = wx.Panel(frame,-1)
    dlg = OutputDlg()
    dlg.write('aaaaa')
    dlg.show()
    frame.Show()


    try:
        app.MainLoop()
    except:
        app.RedirectStdio()



if __name__ == '__main__':
    main()
    module = __file__.split('.')[0]
    print 


