# _*_ coding: utf-8 _*_
# Copyright (C)  2009 Takakazu Ishikura

"""Friendly Python SSH2 interface."""

from __future__ import with_statement 
import os
import tempfile
import warnings  
# warnings.filterwarnings('ignore', category=DeprecationWarning,
#                         message=r'Crypto')
warnings.filterwarnings('ignore', category=DeprecationWarning,
                        message=r'the sha module')
warnings.filterwarnings('ignore', category=DeprecationWarning,
                        message=r'the md5 module')
import socket
import paramiko
from exception import NagaraException

class ConnectionException(NagaraException): pass


class Connection(object):
    """Connects and logs into the specified hostname. 
    Arguments that are not given are guessed from the environment.""" 

    def __init__(self,
                 host,
                 username = None,
                 private_key = None,
                 password = None,
                 port = 22,
                 logfile='socket.log'
                 ):
        self._sftp_live = False
        self._sftp = None
        if not username:
            if os.environ.get('LOGNAME'):
                username = os.environ['LOGNAME']
            else:
                username = os.environ['USERNAME']

        # Log to a temporary file.
        logfile = tempfile.mkstemp('.txt', 'ssh-')[1]
        paramiko.util.log_to_file(logfile)

        # Begin the SSH transport.
        self._transport = paramiko.Transport((host, port))
        self._tranport_live = True
        self.__host = host

        # Authenticate the transport.
        if password:
            # Using Password.
            self._transport.connect(username = username, password = password)
        else:
            # Use Private Key.
            if not private_key:
                # Try to use default key.
                if os.path.exists(os.path.expanduser('~/.ssh/id_rsa')):
                    private_key = '~/.ssh/id_rsa'
                elif os.path.exists(os.path.expanduser('~/.ssh/id_dsa')):
                    private_key = '~/.ssh/id_dsa'
                else:
                    raise TypeError, "You have not specified a password or key."

            private_key_file = os.path.expanduser(private_key)
            rsa_key = paramiko.RSAKey.from_private_key_file(private_key_file)
            self._transport.connect(username = username, pkey = rsa_key)
    
    def _sftp_connect(self):
        """Establish the SFTP connection."""
        if not self._sftp_live:
            self._sftp = paramiko.SFTPClient.from_transport(self._transport)
            self._sftp_live = True

    def get(self, remotepath, localpath = None):
        """Copies a file between the remote host and the local host."""
        if not localpath:
            localpath = os.path.split(remotepath)[1]
        self._sftp_connect()
        self._sftp.get(remotepath, localpath)

    def put(self, localpath, remotepath = None):
        """Copies a file between the local host and the remote host."""
        if not remotepath:
            remotepath = os.path.split(localpath)[1]
        self._sftp_connect()
        self._sftp.put(localpath, remotepath)

    def mkdir(self, remotedir):
        self._sftp.mkdir(remotedir, mode=511)

    def putdir(self, localdir, remotedir=None):
        """Copies a directory to the remote host, recursively."""
        if not remotedir:
            remotedir = os.path.split(localdir)[1]
        self._sftp_connect()
        # check remote dir
        if not self.exists(remotedir):
            self._sftp.mkdir(remotedir, mode=511)

        for file in os.listdir(localdir):
            if __debug__: print file
            localpath = localdir + '\\' + file
            remotepath = remotedir + '/' + file
            self._sftp.put(localpath, remotepath)

    #def getdir(self, remotedir, localdir)

    def exists(self, path):
        """Check whether the path exists or not."""
        self._sftp_connect()
        try:
            stat = self._sftp.lstat(path)
            # stat = self._sftp.stat(path)
        except IOError:
            return None
        return stat

    def rmdir(self, path):
        self._sftp.rmdir(path)

    def chmod(self, path, mode):
        self._sftp.chmod(path, mode)

    def execute(self, command):
        """Execute the given commands on a remote machine."""
        channel = self._transport.open_session()
        channel.exec_command(command)
        output = channel.makefile('rb', -1).readlines()
        if output:
            return output
        else:
            return channel.makefile_stderr('rb', -1).readlines()

    def open(self, filename, mode='r', pipeline=False):
        """Open the specified file on a remote host."""
        self._sftp_connect()
        remotefile = self._sftp.open(filename, mode=mode)
        remotefile.set_pipelined(pipelined=pipeline)
        return remotefile

    def close(self):
        """Closes the connection and cleans up."""
        # Close SFTP Connection.
        if self._sftp_live:
            self._sftp.close()
            self._sftp_live = False
        # Close the SSH Transport.
        if self._tranport_live:
            self._transport.close()
            self._tranport_live = False

    def remove(self, filename):
        """Remove the file on the remote host."""
        self._sftp_connect()
        self._sftp.remove(filename)

    def tail(self, filename):
        """Return the content the file on the remote, like tail command."""
        pass

    def get_pty(self):
        """Request a pseudo-terminal from the server."""
        return self._channel.get_pty()

    def get_env_dict(self):
        """Get all of the the environment variables."""
        output = self.execute('env')
        env_dict = {}
        for var_vals in output:
            var = var_vals.split('=')[0]
            vals = var_vals[len(var)+1:]
            env_dict[var] = vals.strip()
        return env_dict

    def set_envs(self, **envs):
        """set the environment variable on the remote """
        for key, var in envs.items():
            self._remote_envs[key] = var

    def get_env(self, env):
        """ get the environment variable on the remote """
        env_dict = self.get_env_dict()
        if env in env_dict:
            return env_dict[env]
        else:
            return None

    def get_host_by_ip(self):
        return socket.gethostbyname(self.__host)

    def __del__(self):
        """Attempt to clean up if not explicitly closed."""
        self.close()

    def is_communicating(self):
        return False



def main():
    """Little test when called directly."""
    import wx
    # Set these to your own details.
    # myssh.put('ssh.py')
    # output = chan.execute('ls -lhrt')
    fn = "/home/ishikura/projects/prp/binding-mode-bfe/2Search-Pattern/30/sam24.out"

    app = wx.App(redirect=False)
    frame = wx.Frame(None, -1, 'remote test')


    import configremote
    with configremote.ConfigRemote(frame) as dlg:
        configs = dlg.getConfigs()
    
    log.write(configs)
    
    # conn = Connection(configs['host'], configs['passwd']) 
    conn = Connection(host=configs['host'], password=configs['passwd']) 

    cmd = 'ls $HOME/opt'
    output = conn.execute(cmd)
    for line in output:
        log.write(line)

    # file = conn.open(filename=fn, mode='r',pipeline=True).readlines()


    # print file
    conn.close()

    try:
        app.MainLoop()
    except:
        app.RedirectStdio()

def main2():
    logfile = 'network_error.log'
    app = wx.App(redirect=False, filename=logfile)
    frame = wx.Frame(None, -1, 'TestFrame')

    config_ssh = dict(
        user = 'ishikura',
        host = '133.66.117.139',
        port = 22,
        passwd = '********',
        server_cmd = ''
    )
    config_remote = dict(
        nagara_root = '/home/ishikura/Nagara',
        project_root = None,
    )
    config_remote['project_root'] = \
        '/'.join([config_remote['nagara_root'], 'projects'])
    config_local = dict(
        nagara_root = None,
        project_root = None,
    )
    config_paics = dict(
        paics_root = '',
        input_file = '',
        output_file = '',
    )
    config_app = dict(
    )
    configs = dict(
        ssh = config_ssh,
        remote = config_remote,
        local  = config_local,
        paics = config_paics,
        app    = config_app,
        keybind = config_keybind
    )

    from logview import SimpleLogView
    remote = RemoteConnection('133.66.117.139')

    print configs
    
    frame.Show()

    try:
        app.MainLoop()
    except:
        app.RedirectStdio()

def test_write():
    conn = Connection(host='133.66.117.139', password='*********') 

    cmd = 'ls $HOME/opt'
    rfn = 'hoge'
    print conn.exists(rfn)
    rfile = conn.open(rfn, 'w')
    rfile.write('hogehogehoge')
    # for l in rfile:
    #     print(l)

    rfile.close()
    conn.remove(rfn)

    # output = conn.execute('cat hosts')
    # for line in output:
    #     print(line)

    # file = conn.open(filename=fn, mode='r',pipeline=True).readlines()


    # print file
    conn.close()

def test_tail_remote():
    conn = Connection(host='133.66.117.139', password='*******') 
    rfn = 'hoge'
    rfile = conn.open(rfn, 'r')
    # print rfile.read()
    for l in tail(rfile): print l,

def test_tail_local():
    file = open('hoge', 'r')
    # print rfile.read()
    for l in tail(file): print l,

def test_get_shell():
    # conn = Connection(host='133.66.117.139', password='sdio3871') 
    conn = Connection(host='hpcs.med.gifu-u.ac.jp', password='sdio3871') 
    print conn.get_env('SHELL')
    print conn.get_host_by_ip()


# start the ball rolling.
if __name__ == "__main__":
    # main()
    # main2()
    # main3()

    # test_tail_remote()
    test_get_shell()
