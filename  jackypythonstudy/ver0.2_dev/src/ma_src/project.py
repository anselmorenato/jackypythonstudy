#! /usr/bin/env python
# _*_ coding: utf-8 _*_
# Copyright (C)  2009 Takakazu Ishikura
import os, sys
import shutil
import datetime
from optparse import OptionParser, OptionValueError
import connection

# Global variables : NAGARA_ROOT
# Global variables : PROJECT_ROOT = NAGARA_ROOT/project_name
# Global variables : REMOTE_NAGARA_ROOT
# Global variables : REMOTE_PROJECT_ROOT = REMOTE_NAGARA_ROOT/project_name

#-------------------------------------------------------------------------------

class Project(object):

    """
    The class to administrate the project including the operation of
    synchronuous between client and server.
    """

    def __init__(self, root=None, name=None):
        """Constructor."""
        self.__id_count = 0

        self.__rootdir  = root
        self.__name     = name
        self.tree  = Group(id=1)

        self.__systems = []
        self.__tasks = []
        self.__datas = []
        self.__scripts = []
        self.__settings = []
        self.__groups = []

    def load(self, root):
        """Load the project used before from the saved project object."""
        self.__rootdir = root

    def save(self, filename):
        """Save the project object to a file to store."""
        pass

    def check(self):
        """Check a consistency between the project tree and real project dir."""
        pass

    def getLocalProject():
        pass

    def __traverse(self, task):
        """Traverse all of the tasks."""
        if isinstance(task, Task):
            yield task
        elif isinstance(task, TaskGroup):
            for t in task.getTasks():
                yield t
                self.traverse(t)

    def getMaxId(self):
        """Get the max id."""
        id = max( [ t.id for t in self.__traverse(self.project) ] )
        self.__id_count = id
        return id

    def create(self, parent, name):
        """Create new task from the specified task name."""
        self.__id_count += 1
        task = Task(parent=parent, id=self.__id_count, name=name)
        parent.append(task)

    def createGroup(self, parent, name):
        """Create new task group from the specified task group name."""
        self.__id_count += 1
        task_group = Group(parent=parent, id=self.__id_count, name=name)
        parent.appendGroup(task_group)

    def existsTaskName(self, name):
        """Check whether the task of specified name exists or not."""
        names = (t.name for t in self.__tasks)
        return True if name in names else False
        
    def syncLocal(self):
        root = self.project
        # if 
        # for task in root.getTasks():

    def delete(self, project_path, id=-1):
        """Delete the project by project id or path from project root."""
        if project_path in self.projects:
            shutil.rmtree(os.path.join(self.proot, project_path))
            return True
        else:
            return False


        # if os.path.exists(self.project):
        #     shutil.rmtree(self.project)
        # else:
        #     os.mkdir(self.project)
        # os.mkdir(self.project)

    def copy(self, src, dst):
        """Copy the specified task from src to destination."""


    def delGroup(self, task_group):
        pass

    def clean(self):
        """Clean up all of the projects."""
        # shutil.rmtree(self.__rootdir)
        return True

    def find(self, name, cond):
        """Find the project id from project_name."""
        pass

    def appendSystem(self, system):
        """Append the system to this project."""
        if not self.__systems:
            self.__systems = [system]
        else:
            self.__systems.append(system)

    def getSystem(self):
        """Return the bio system as a list."""
        return self.__systems

    def getProjects(self):
        """ return recursive project list by list under the root directory
        """
        root_size = len(self.proot)
        projects = []
        for root, dirs, files in os.walk(self.proot):
            for d in dirs:
                project = os.path.join(root, d)
                projects.append(project[root_size+1:])
        return projects

    def create(self, project_path):
        """ create project from project name with pid(from datetime)
        """
        # project id
        # date = datetime.datetime.today()
        # now = date.strftime("%Y%m%d%H%M%S")
        # project_path = os.path.join(self.proot, '%s.%s'% (project_path,now))
        if project_path in self.projects:
            return False
        else:
            abspath = os.path.join(self.proot, project_path)
            os.makedirs(abspath)
            self.projects.append(abspath)
            return True

    def setRoot(self, rootdir):
        """Set the root directory."""
        self.__rootdir = rootdir

    def getRoot(self):
        """Return the root directory for this project."""
        return self.__rootdir

    def appendTask(self, task):
        """Append the task to this project."""
        self.__tasks.append(task)

    def appendGroup(self, taskgroup):
        """Append the task group to this project."""
        self.__groups.append(taskgroup)

    def __lshift__(self, obj):
        if isinstance(obj, Task):
            self.appendTask(obj)
        elif isinstance(obj, Group):
            self.appendGroup(obj)
        else:
            raise KeyError

    def getName(self):
        """Return the label."""
        return self.__name

    def getId(self):
        self.__id_count += 1
        return self.__id_count

#-------------------------------------------------------------------------------

class Group(object):
    
    """
    class to group tasks.
    """
    
    def __init__(self, parent=None, id=-1, name=None):
        self.parent = parent
        self.childs = []
        self.id = id
        self.name = name
        self.tasks = []

    def append(self, task):
        """Append the task into this task group."""
        self.tasks.append(task)

    def appendGroup(self, task_group):
        """Append the taks group into this task group."""
        self.tasks.append(task_group)

    def getTasks(self):
        """Get the tasks in this group."""
        return self.tasks

    def getState(self, task_group):
        pass

#-------------------------------------------------------------------------------

class Task(object):

    """
    Class to define tasks that perform each calculation.
    """

    def __init__(self, parent, configs, name=None,
                 host='local', log=None):

        self.__parent = parent
        self.__log = log
        self.__configs  = configs
        self.__host = host

        self.__dateid =name + datetime.datetime.today().strftime('%Y%m%d%H%M%S')

        # task name
        if name:
            self.__name = name
        else:
            self.__name = 'task'
        self.__id = self.__parent.getId()
        self.__label = self.__name + '.' + str(self.__id)

        # remote_path format : username@host:path
        self.local = TaskLocal(self)
        self.remote = TaskRemote(self)

        # other objects
        self.__cmd = None
        self.__conn = None
        self.__jms = None

        # __inputs and __outputs = {identifier : file or object name}
        # __input_types and __output_types = {identifier : ('file'|'obj', type)}
        # file type : pdb, xyz, marvinxyz, mol2, a-data, b-data, ...
        # obj type : system, crd, vel, any-data, log, energy, text, ...
        self.__inputs       = {}  
        self.__input_types  = {}
        self.__outputs      = {}
        self.__output_types = {}
        # settings
        self.__settings    = {}

        # state
        # state type: preparing, running, done, error, warning,
        self.__state = ('preparing', 0)

    def log(self, message):
        """Write the message."""
        if self.__log: self.__log.write(message)

    def getProject(self):
        """Return the project."""
        return self.__parent

    def getConfigs(self):
        """Return the global remote configs."""
        return self.__configs

    # def setCommand(self, cmd):
    #     """Set a command."""
    #     import jms
    #     if isinstance(jms, str):
    #         self.__setJMS_str(self, jms):
    #     elif isinstance(jms, jms.JMS):
    #         self.__setJMS_jms(self, jms)
    #     else:
    #         raise TypeError
    def setCommand(self, cmd):
         """Set a command."""
         self.__setCmd_cmd(cmd)

    def __setCmd_str(self, cmd):
        pass

    def __setCmd_cmd(self, cmd):
        """Set a command to this task."""
        cmd_configs = self.__configs[self.__host]['commands']
        c = cmd_configs[cmd.getName()]
        cmd.setPath(c['path'])
        cmd.setEnvs(c['envs'])
        self.__cmd = cmd

    def getCommand(self):
        """Return a command to this task."""
        return self.__cmd

    def setConnection(self, conn):
        """Set a connection to a remote."""
        self.__conn = conn

    def getConnection(self):
        """Return a connection to a remote."""
        return self.__conn

    def checkConnection(self):
        """Check a remote connection."""
        pass

    def setJMS(self, jms_arg):
        """Set a job manager system for a remote."""
        import jms
        if isinstance(jms_arg, str):
            self.__setJMS_str(jms_arg)
        # elif isinstance(jms_arg, jms.JMS):
        #     self.__setJMS_jms(jms_arg)
        elif isinstance(jms_arg, jms.LSF):
            self.__setJMS_jms(jms_arg)
        else:
            raise TypeError

    def __setJMS_jms(self, jms):
        self.__jms = jms

    def __setJMS_str(self, jms_str):
        config = self.__configs.get(self.__host)
        if config:
    #       if jms_str in config['jms']:
    #           import jms
    #           self.__jms = jms.JMS(type=jms_str)
            if jms_str in config['jms'].keys():
                import jms
                if jms_str == 'Single':
                    self.__jms = jms.Single()
                elif jms_str == 'LSF':
                    self.__jms = jms.LSF()
                else:
                    pass

    def getJMS(self):
        """Return the job manager system for a remote."""
        return self.__jms

    def getJMSTypes(self):
        return self.__configs[self.__host]['jms']

    # def setInputObj(self, **objs):
    #     """Set a input object."""
    #     self.__input_objs = objs

    # def setInputFile(self, input_fn):
    #     """Set a input format."""
    #     self.__input_fns = input_fns
    #     self.__input_fmts.append('file')

    # def setInputType(self, type):
    #     self.__input_types = type

    # def getInputFile(self):
    #     """Return the input format."""
    #     return self.__inputs_fns, self.__input_fmts

    # def checkInput(self):
    #     """Check the validity between command and input object."""
    #     pass

    # def setOutputs(self, outputs, output_fmts):
    #     """Set a output object and format."""
    #     self.__outputs = outputs

    # def getOutputs(self):
    #     """Return the output object and output format."""
    #     return self.__outputs, self.__output_fmts

    # def setSettings(self, objs, file=False):
    #     """Set the settings."""
    #     if file:
    #         self.__settings = objs
    #         fmt = self.__task.getSettings
    #         self.__setting_fmts.append( 'file' )
    #     else:
    #         self.__settings_
    #     self.__setting_fn
    #     self.__settings = settings

    # def getSettings(self):
    #     """Return the settings."""
    #     return self.__settings

    def getName(self):
        """Return name."""
        return self.__name

    def getLabel(self):
        """Return label."""
        return self.__label

    def getHost(self):
        """Return the host to use."""
        return self.__host

    def changeHost(self):
        pass

    def checkSettings(self):
        pass

    def checkIO(self):
        """Check the validity between the connected task and this task.

        Check the validity between the connected task and this task about input
        object and output object.
        """
        pass

    def checkOutput(self):
        pass

    def getId(self):
        return self.__id

    def setup(self):
        """Setup the task."""
        self.setupLocal()
        self.setupRemote()

    def setupLocal(self):
        if self.local.isNone():
            self.local.create()
            self.local.setCreated()
            self.__cmd.setup()
            self.local.setReady()
            return True
        elif self.local.isCreated():
            self.__cmd.setup()
            self.local.setReady()
            return True
        else:
            return False

    def setupRemote(self):
        self.remote.put()
        self.remote.setReady()

    def run(self, input_fn=None):
        self.setup()
        if self.remote.isReady():
            # self.__cmd.run(input_fn=input_fn)
            self.__cmd.run()
            # self.remote.setRunnning()
            self.remote.setDone()
        ##self.setup(input_fn=input_fn)

    def getRemoteInfo(self):
        """Return remote info: user name, host and working path."""
        rpath = self.remote.getPath()
        if rpath.find('@') >= 0:
            username, tmp = rpath.split('@')
        else:
            username = None
            tmp = rpath

        if tmp.find(':') >=0:
            host, path = tmp.split(':')
        else:
            host = None
            path = tmp
        return username, host, path

    def delete(self):
        self.remote.delete()
        # self.local.delete()
        self.log('delete the task: '+ str(self) + '\n')

    def move(self):
        pass

    # def copy(self, dst):
    #     return shutil.copytree(src, dst)

    def getLocal(self):
        return self.local

    def getRemote(self):
        return self.remote

#-------------------------------------------------------------------------------

class TaskLocal(object):

    """
    The class to perform the local operations for task.
    """

    state = ['none', 'created', 'ready', 'running', 'done', 'error']
    state_fn = '.nagara'

    def __init__(self, task):
        """Constructor."""
        self.__task = task

        # set the local path
        name = self.__task.getLabel()
        local_root = self.__task.getProject().getRoot()
        self.__path = os.path.join(local_root, name)
        
        self.__state = 'none'
        if os.path.exists(self.__path): self.setCreated()

    def create(self):
        """Make a local directory for task."""
        if self.isNone():
            os.mkdir(self.__path)
            self.setCreated()
            return True
        else:
            return False

    def move(self, dst_path):
        """Move the local directory to dst_path."""
        if not self.isNone():
            if not os.path.exists(dst_path):
                os.rename(self.__path, dst_path)
                return True
            else:
                return False
        else:
            return False

    def putFile(self, src_path, dst_fn):
        """Copy the external file to the task directory with dst_fn."""
        ldir = self.__path
        dst_base = os.path.basename(dst_fn)
        dst_path = os.path.join(ldir, dst_base)

        src_file = open(src_path, 'rb')
        dst_file = open(dst_path, 'wb')
        dst_file.write(src_file.read())
        src_file.close()
        dst_file.close()

    def delete(self):
        """Delete the local directory."""
        if not self.isNone():
            shutil.rmtree(self.__path)
            self.setNone()
            return True
        else:
            return False

    def show(self):
        pass

    def getPath(self):
        """Return the local absolute path of this task."""
        return self.__path

    def save(self):
        pass

    def restore(self):
        pass

    def getFiles(self):
        pass

    def __isState(self, state):
        if self.getState() == state and self.__state == state:
            return True
        else:
            return False

    def isNone(self):
        if not os.path.exists(self.__path):
            return True
        else:
            return False

    def isCreated(self):
        return self.__isState('created')

    def isReady(self):
        return self.__isState('ready')

    def isRunning(self):
        return self.__isState('running')

    def isDone(self):
        return self.__isState('done')

    def __setState(self, state):
        state_path = os.path.join(self.__path, self.state_fn)
        state_file = open(state_path, 'wb')
        state_file.write(state)
        self.__state = state
        state_file.close()

    def setNone(self):
        self.delete()

    def setCreated(self):
        self.__setState('created')

    def setReady(self):
        self.__setState('ready')

    def setRunnning(self):
        self.__setState('running')

    def setDone(self):
        self.__setState('done')

    def getState(self):
        state_path = self.__path + '/' + self.state_fn
        state_file = open(state_path, 'rb')
        state = state_file.read()
        state_file.close()
        return state

#-------------------------------------------------------------------------------

class TaskRemote(object):

    """
    The class to perform the remote operations for task.
    """

    state = ['none', 'created', 'ready', 'running', 'done', 'error']
    state_fn = '.nagara'

    def __init__(self, task):
        """Constructor."""
        self.__task = task
        configs = self.__task.getConfigs()

        host = self.__task.getHost()
        config = configs[host]
        remote_root = configs[host]['rootdir']
        self.__path = remote_root + '/' + self.__task.getLabel()

        self.__host = self.__task.getHost()
        # if self.__task.getConnection():
        #     self.__conn = self.__task.getConnection()
        self.__configs = self.__task.getConfigs()
        
        # remote state :
        #     'None', exists, 'running', 'done', donesync', donenone', 'error'
        self.__state = 'none'

    def connect(self):
        if not self.__task.getConnection():
            host = self.__task.getHost()
            if  self.__task.getConfigs().get(host):
                configs = self.__task.getConfigs()[host]
                import connection
                conn = connection.Connection(
                    host = configs[ssh][addr],
                    password = configs[ssh][passwd],
                    user = configs[ssh][user]
                )
                self.__task.setConnection(conn)


    def create(self):
        """Create the remote task directory."""
        configs = self.__task.getConfigs()
        host = self.__task.getHost()
        remote_root = configs[host]['rootdir']
        conn = self.__task.getConnection()

        if not conn.exists(remote_root):
            conn.mkDir(remote_root)

        if not conn.exists(self.__path):
            conn.mkDir(self.__path)
            self.setCreated()

    # def setConnection(self, conn):
    #     """Set the connection to remote host."""
    #     self.__conn = conn

    # def getConnection(self):
    #     """Get the connection to remote host."""
    #     return self.__conn

    def put(self, force=False):
        """Put the local task to a directory on the remote project dir."""
        if self.isNone():
            local = self.__task.local
            ldir = local.getPath()
            if local.isReady():
                self.create()
                conn =  self.__task.getConnection()
                conn.putDir(ldir, self.__path)
                self.setReady()
                return True
            raise 'not already put the local dir to remote dir.'
        else:
            return False

    def get(self):
        local = self.__task.local
        if self.isDone() and local.isReady():
            ldir = local.getPath()
            rdir = self.__path
            conn = self.__task.getConnection()
            conn.getDir(rdir, ldir)

    def getPath(self):
        """Return the remote absolute path."""
        return self.__path

    def checkState(self):
        return True if self.getState() == self.__state else False

    def syncState(self, state):
        self.__setState( self.__state )

    def delete(self):
        """Delete the remote directory."""
        if not self.isNone():
            self.__task.getConnection().execute('rm -rf '+self.__path)
            self.setNone()

    def getFile(self, remote_fn):
        conn = self.__task.getConnection()
        return conn.get(remote_fn, self.__task.local.getPath())

    def tail(self, remote_fn, output):
        conn = self.__task.getConnection()
        rfile = conn.open(remote_fn, mode='r', pipeline=True)
        while True:
            where = rfile.tell()
            line = rfile.readline()
            if not line:
                time.sleep(10)
                rfile.seek(where)
            else:
                output.write(line), # already has newline
                # or + generator + external method

    def getPath(self):
        return self.__path

    def __isState(self, state):
        conn = self.__task.getConnection()
        if conn.exists(self.__path):
            if self.getState() == state and self.__state == state:
                return True
        else:
            return False

    def isNone(self):
        conn = self.__task.getConnection()
        if not conn.exists(self.__path):
            return True
        else:
            return False

    def isCreated(self):
        return self.__isState('created')

    def isReady(self):
        return self.__isState('ready')

    def isRunnning(self):
        return self.__isState('running')

    def isDone(self):
        return self.__isState('done')

    def __setState(self, state):
        conn = self.__task.getConnection()
        if conn.exists(self.__path):
            conn = self.__task.getConnection()
            state_path = self.__path + '/' + self.state_fn
            state_file = conn.open(state_path, 'wb')
            state_file.write(state)
            self.__state = state
            state_file.close()
        else:
            raise 'Exception : setState'

    def setNone(self):
        self.delete()
        # try:
        #     self.__setState('none')

        # self.__setState('none', False)

    def setCreated(self):
        self.__setState('created')

    def setReady(self):
        self.__setState('ready')

    def setRunnning(self):
        self.__setState('running')

    def setDone(self):
        self.__setState('done')

    def getState(self):
        conn = self.__task.getConnection()
        state_path = self.__path + '/' + self.state_fn
        state_file = conn.open(state_path, 'rb')
        state = state_file.read()
        state_file.close()
        return state

#-------------------------------------------------------------------------------

class Data(object):

    """
    The class to define a data.
    """

    def __init__(self):
        self.__isfile = False
        self.__type = None
        self.__name = 'data'
        self.__id = 1
        self.__label = self.__name + '.' + self.__id


    def set(self, data):
        pass

    def __set_data(self, data):
        pass

    def __set_file(self, fn):
        pass

    def getType(self):
        return self.__type

    def setType(self, type):

        pass

#-------------------------------------------------------------------------------

class Setting(object):

    """
    The class to define a settings.
    """

    def __init__(self):
        pass


#-------------------------------------------------------------------------------


# os.chdir(project)
# HOME = os.environ['HOME']

if __name__ == "__main__":
    import optparse

    usage = ""
    parser = optparse.OptionParser(usage)
    parser.add_option("-o", "--opt", dest="opt", help=u"", default=None)
    (options, args) = parser.parse_args()

    # configs for command and connection and task
    remote_configs = dict(
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


    # generate project
    nagara_root = 'C:\\Home_Ishikura\\docs\\Nagara-ishikura\\test-projects'

    proj = Project(root=nagara_root)

    # generate task
    task = Task(proj, configs=remote_configs, name='test', host='hpcs')
    proj.appendTask(task)

    import jms
    # task.setJMS(jms.LSF())
    task.setJMS('LSF')
    # import connection
    # conn = connection.Connection('133.66.117.139', password='')
    # task.setConnection(conn)

    import paics
    cmd = paics.Paics(task)

    task.setCommand(cmd)

    print 'task = ', task.getLabel()
    print 'task id = ', task.getId()
    print 'local = ', task.local.getPath()
    print 'remote = ', task.remote.getPath()
    print 'cmd_envs = ', task.getCommand().getEnvs()
    print 'cmd_path = ', task.getCommand().getPath()
    print 'cmd_name = ', task.getCommand().getName()
    # t.put()
    # t.setup('C:\\Home_Ishikura\\docs\\Nagara\\src\\local-root\\test\\fmo-h2o-4-631gdp.inp')
    # input_file = 'C:\\Home_Ishikura\\docs\\Nagara\\src\\local-root\\test\\fmo-h2o-4-631gdp.inp'
    # input_file = 'C:\Home_Ishikura\docs\Nagara\src\local-root\test\fmo-h2o-4-631gdp.inp'
    # t.setup(input_fn=input_file)
    # task.run(input_fn=input_file)
    # conn.close()


