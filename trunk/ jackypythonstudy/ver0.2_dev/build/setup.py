# setup.py
import sys, os
from distutils.core import setup

options = {
    # 'name': 'Nagara',
    # 'version': '1',
    'description': 'Nagara',
    'packages': ['ctypes','logging','weakref','Crypto'],
    'includes': ['new', 'distutils.util'],
    'excludes': ['OpenGL'],
    'compressed' : 1,
    'optimize' : 0,
    'bundle_files' : 1,
}

data_files = [
    # ('', ['libs/PyOpenGL-3.0.0c1-py2.5.egg']),
    # ('', ['libs/setuptools-0.6c9-py2.5.egg']),
    # ('', ['libs/paramiko-1.7.4-py2.5.egg']),
    ('libs', ['libs/PyOpenGL-3.0.0c1-py2.5.egg',
              'libs/setuptools-0.6c9-py2.5.egg',
              'libs/paramiko-1.7.4-py2.5.egg']),
    ('', ['nagara.ico'])
]

# this manifest enables the standard Windows XP/Vista-looking theme
manifest = """
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1"
manifestVersion="1.0">
<assemblyIdentity
    version="0.64.1.0"
    processorArchitecture="x86"
    name="Controls"
    type="win32"
/>
<description>Picalo</description>
<dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.Windows.Common-Controls"
            version="6.0.0.0"
            processorArchitecture="X86"
            publicKeyToken="6595b64144ccf1df"
            language="*"
        />
    </dependentAssembly>
</dependency>
</assembly>
"""

# windows specific for py2exe
if len(sys.argv) >= 2 and sys.argv[1] == 'py2exe':
    try:
        import py2exe
    except ImportError:
        print 'Could not import py2exe. Windows exe could not be built.'
        sys.exit(0)
    # windows-specific options
    options_win = [
        {
            'script':  'nagara.py',
            'icon_resources': [(1,'nagara.ico')],
            'other_resources': [ (24, 1, manifest), ],
        },
    ]

# mac specific
if len(sys.argv) >= 2 and sys.argv[1] == 'py2app':
    try:
        import py2app
    except ImportError:
        print 'Could not import py2app. Mac bundle could not be built.'
        sys.exit(0)
    # mac-specific options
    options['app'] = ['nagara.py']
    options['options'] = {
        'py2app': {
            'argv_emulation': True,
        }
    }

# run the setup
setup(
    options = {'py2exe': options},
    windows = options_win,
    data_files = data_files,
    zipfile = None,
)
