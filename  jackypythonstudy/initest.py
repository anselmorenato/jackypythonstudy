

import wx

from modules import dict4ini as d4i

rem = d4i.DictIni('remote_config.ini')
if not len(rem['remote_configs']['hpcs']['commands'].values())==0:
    print len(rem['remote_configs']['hpcs']['commands'].keys())
    print rem['remote_configs']['hpcs']['commands'].keys()
else:
    print 'aaa'
#if rem.has_key('local')==True: #and type(rem['local'])==str:
#    print rem['local']['jms']



