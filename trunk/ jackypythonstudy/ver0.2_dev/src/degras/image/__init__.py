#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura
#
# $Date: 2010-01-20 14:48:22 +0900 (水, 20 1 2010) $
# $Rev: 57 $
# $Author: ishikura $
#
# standard modules
import os, sys
import wx

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from core.exception import NagaraException

# variables
image_abspath = os.path.join( nagara_path, 'src', 'images' )

class NotFoundImageError(NagaraException): pass

# job state images
JOBSTATE_PATH_DICT  = dict(
    runnable = os.path.join(image_abspath, 'jobstate', 'arrow_right.png' ) ,
    running  = os.path.join(image_abspath, 'jobstate', 'arrow_undo.png'  ) ,
    done     = os.path.join(image_abspath, 'jobstate', 'arrow_undo.png'  ) ,
)

JOBSTATE_IMAGE_DICT = {}
def get_jobstate_image(statename):
    statename = statename.lower()
    if statename not in JOBSTATE_PATH_DICT.keys():
        raise NotFoundImageError(statename)

    image = JOBSTATE_IMAGE_DICT.get(statename)
    if image:
        image = JOBSTATE_IMAGE_DICT[statename]
    else:
        image = wx.Bitmap( JOBSTATE_PATH_DICT[statename] )
        JOBSTATE_IMAGE_DICT[statename] = image
    return image


# menu item images
MENU_IMAGE_DICT = {}
MENU_PATH_DICT = dict(
)


if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(None, -1, 'wxPython', size=(220, 260))
    frame.Show()
    image = get_jobstate_image('Running')
    stbmap = wx.StaticBitmap(frame, -1, image, (16, 16))
    image2 = get_jobstate_image('Running')
    stbmap2 = wx.StaticBitmap(frame, -1, image2, (32, 32))
    image3 = get_jobstate_image('Running')
    stbmap3 = wx.StaticBitmap(frame, -1, image3, (48, 48))
    image4 = get_jobstate_image('Running')
    stbmap4 = wx.StaticBitmap(frame, -1, image4, (64, 64))
    app.MainLoop()

