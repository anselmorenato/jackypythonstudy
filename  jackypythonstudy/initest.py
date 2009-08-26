

import wx

from modules import dict4ini as d4i

rem = d4i.DictIni('remote_config.ini').remote_configs

print rem._items
#if rem.has_key('local')==True: #and type(rem['local'])==str:
#    print rem['local']['jms']



