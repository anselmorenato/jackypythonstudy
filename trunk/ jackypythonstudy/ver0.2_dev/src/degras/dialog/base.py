import os, sys
import wx
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from core.exception import NagaraException, DialogCancelException


class MessageDialog(wx.MessageDialog):
    def __init__(self, message, caption):
        wx.MessageDialog.__init__(self, None, message, caption, 
                                  style=wx.ICON_INFORMATION)
    def __enter__(self):
        self.ShowModal()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.Destroy()
        return True


# class MessageDialog(wx.MessageDialog):

    # def __init__(self, None, message, caption, use_exc=False):
        # wx.MessageDialog.__init__(self, None, message, caption,
                                  # style=wx.ICON_INFORMATION)
        # self.__exc = exc
    
    # def __enter__(self):
        # self.__flag = self.ShowModal()
        # return self

    # def __exit__(self, exc_type, exc_value, traceback):
        # self.Destroy()
        # return not self.__use_exc

