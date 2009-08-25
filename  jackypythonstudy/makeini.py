from modules import dict4ini as d4i

rec = d4i.DictIni('remote_configback.ini')

rec.remote_configs.comment = 'This file is created use "dict4ini"module. \n The detailed information for "dict4ini", please access this website http://code.google.com/p/dict4ini/'
              
rec.remote_configs = dict(
        # email = 'ishikura@gifu-u.ac.jp',
        local = dict(
            ssh = {},
            rootdir = 'C:\path\to\nagara-root',
            workdir = '',
            jms = dict(
                Single = dict(
                    envs = {},
                    path = {},
                    ),
                MultiProcess = dict(
                    ),
                ),
            commands = {},
            ),
        hpcs = dict(
            ssh = dict(
                address = '133.66.117.139',
                user = 'ishikura',
                passwd = '*********',
                port = 22,
                ),
            rootdir = '/home/ishikura/Nagara/projects',
            workdir = '/work/ishikura',
            # jms = ['Single', 'MPI', 'LSF'], #Local
            jms = dict(
                Single = dict(
                    envs = {},
                    path = {},
                    ),
                MPI = dict(
                    envs = {},
                    path = {},
                    ),
                LSF = dict(
                    envs = {},
                    path = {},
                    script = {},
                    ),
                ),
            commands = dict(
                amber = dict(
                    # envs = dict(AMBERHOME = '/home/hpc/opt/amber10.eth'),
                    # path = '/home/hpcs/opt/amber10.eth/exe/sander.MPI',
                    envs = dict(AMBERHOME = '/home/ishikura/opt/amber10.eth'),
                    path = '/home/ishikura/opt/amber10.eth/exe/sander.MPI',
                    ),
                marvin = dict(
                    envs = {},
                    # path = '/home/hpcs/Nagara/app/bin/marvin',
                    path = '/home/ishikura/Nagara/app/bin/marvin',
                    ),
                paics = dict(
                    # envs = dict(PAICS_HOME='/home/ishi/paics/paics-20081214'),
                    # path = '/home/ishi/paics/paics-20081214/main.exe',
                    envs = dict(PAICS_HOME='/home/ishi/paics/paics-20081214'),
                    path = '/home/ishi/paics/paics-20081214/main.exe',
                    ),
                ),
            ),
        vlsn = dict(),
        rccs = dict(),
)
    #pass
rec.save()