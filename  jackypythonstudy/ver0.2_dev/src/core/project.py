# _*_ coding: utf-8 _*_
# Copyright (C)  2009 Takakazu Ishikura
import os, sys
import shutil
import datetime
from optparse import OptionParser, OptionValueError


# Nagara modules
import connection
from config import Config

# Global variables : NAGARA_ROOT
# Global variables : PROJECT_ROOT = NAGARA_ROOT/project_name
# Global variables : REMOTE_NAGARA_ROOT
# Global variables : REMOTE_PROJECT_ROOT = REMOTE_NAGARA_ROOT/project_name

from exception import NagaraException
class CommandNotFound(NagaraException): pass
class CommandInvalid(NagaraException): pass
class ProjectException(NagaraException): pass
class FieldError(ProjectException): pass
class ProjectDirectoryCreatedError(ProjectException): pass

#-------------------------------------------------------------------------------

def save_project(project):
    """Save the project object to a file to store."""
    pass

def load_project(dirpath):
    """Load the project used before from the saved project object."""
    pass


class Project(object):

    """
    The class to administrate the project including the operation of
    synchronuous between client and server.
    """

    def __init__(self, dirpath=None, name=None):
        """Constructor."""
        self.__id = hash(self)
        self.__id_count = 0

        self.__rootdir = None
        self.__dirpath = dirpath
        self.__name    = name
        # self.tree  = Group(id=1)

        self.__task_dict  = {} # task_dict[task_id] = task
        self.__data_dict  = {} # data_dict[data_id] = data
        self.__group_dict = {}
        self.__configs  = Config()

    # property: nagara root
    def get_root(self):
        """Return the root directory for this project."""
        if not self.__rootdir:
            rootdir = Config().get_common()['nagara']['rootdir']
            self.__rootdir = os.path.expanduser( rootdir )
        return self.__rootdir
    def set_root(self, rootdir):
        """Set the root directory."""
        self.__rootdir = rootdir
    rootpath = property(get_root, set_root)

    def get_name(self):
        """Return the name."""
        return self.__name
    def set_name(self, name):
        self.__name = __name
    name = property(get_name, set_name)

    def get_hightest_id(self):
        self.__id_count += 1
        return self.__id_count

    def check(self):
        """Check a consistency between the project tree and real project dir."""
        pass

    def __traverse(self, task):
        """Traverse all of the tasks."""
        if isinstance(task, Task):
            yield task
        elif isinstance(task, TaskGroup):
            for t in task.getTasks():
                yield t
                self.traverse(t)

    def get_max_id(self):
        """Get the max id."""
        id = max( [ t.id for t in self.__traverse(self.project) ] )
        self.__id_count = id
        return id

    def create_group(self, parent, name):
        """Create new task group from the specified task group name."""
        self.__id_count += 1
        task_group = Group(parent=parent, id=self.__id_count, name=name)
        parent.append_group(task_group)

    def exists_taskname(self, name):
        """Check whether the task of specified name exists or not."""
        names = (t.name for t in self.__tasks)
        return True if name in names else False
        
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

    def append_data(self, data):
        """Append the data to this project."""
        self.__data_dict[data.id] = data

    def delete_data(self, data):
        pass

    def append_task(self, task):
        """Append the task to this project."""
        self.__task_dict[task.id] = task

    def delete_task(self, task):
        pass

    def append_group(self, group):
        """Append the task group to this project."""
        self.__group_dict.append(group)

    def delete_group(self, task_group):
        pass

    def clean(self):
        """Clean up all of the projects."""
        # shutil.rmtree(self.__rootdir)
        return True

    def find(self, name, cond):
        """Find the project id from project_name."""

        self.__id = self.__project.get_hightest_id()

        self.__type = type          # type
        self.__format = format      # format
        self.__define_context(self) # context
        self.__multi = multiplicity # multiplicity
        pass

    def sort_data_by(self, field='type'):
        """Return the data list sorted by any field."""
        if field not in ('type', 'context', 'format', 'multiplicity'):
            raise FieldError()

        field_set = set(
            [getattr(data, field) for data in self.__data_dict.values()]
        )
        data_field_dict = dict( [ (type, []) for type in field_set ] )

        for id, data in self.__data_dict.items():
            data_field_dict[getattr(data, field)].append( data )

        return data_field_dict

    def sort_data_by_task(self):
        """Return the socket data list in each task."""
        task_input_data_dict  = {}
        task_output_data_dict = {}

        for id, task in self.__task_dict.items():
            task_input_data_dict[id]  = task.inputs
            task_output_data_dict[id] = task.outputs

        return task_input_data_dict, task_output_data_dict

    def get_task_data(self):
        """Return the internal data list in each task."""
        pass

    # def getProjects(self):
    #     """Return recursive project list by list under the root directory."""
    #     root_size = len(self.proot)
    #     projects = []
    #     for root, dirs, files in os.walk(self.proot):
    #         for d in dirs:
    #             project = os.path.join(root, d)
    #             projects.append(project[root_size+1:])
    #     return projects

    # def create(self, project_path):
    #     """ create project from project name with pid(from datetime)
    #     """
    #     # project id
    #     # date = datetime.datetime.today()
    #     # now = date.strftime("%Y%m%d%H%M%S")
    #     # project_path = os.path.join(self.proot, '%s.%s'% (project_path,now))
    #     if project_path in self.projects:
    #         return False
    #     else:
    #         abspath = os.path.join(self.proot, project_path)
    #         os.makedirs(abspath)
    #         self.projects.append(abspath)
    #         return True

    def create(self):
        if self.__dirpath:
            if os.path.exists(self.__dirpath):
                raise ProjectDirectoryCreatedError()
            else:
                os.path.mkdir(self.__dirpath)
        else:
            self.__dirpath = os.path.join(self.rootpath, self.name)
            if os.path.exists(self.__dirpath):
                raise ProjectDirectoryCreatedError()
            else:
                os.path.mkdir(self.__dirpath)

#-------------------------------------------------------------------------------

class Group(object):
    
    """
    class to group tasks.
    """

    __id = 1
    
    def __init__(self, parent=None, id=-1, name=None):
        self.parent = parent
        self.childs = []
        self.__name = name
        self.__task_dict = {}
        self.__data_dict = {}
        self.__id += 1

    def get_name(self):
        return self.__name
    def set_name(self, name):
        self.__name = __name
    name = property(get_name, set_name)

    def get_task_dict(self):
        """Get the tasks in this group."""
        return self.__task_dict

    def append_task(self, task):
        """Append the task into this task group."""
        self.__task_dict[task.id] = task

    def append_data(self, data):
        self.__data_dict[data.id] = data

    # def appendGroup(self, task_group):
    #     """Append the taks group into this task group."""
    #     self.tasks.append(task_group)

#-------------------------------------------------------------------------------



# os.chdir(project)
# HOME = os.environ['HOME']

if __name__ == "__main__":
    # generate project
    p = Project()
    print p.rootpath

    # generate task
    # task = Task(proj, configs=remote_configs, name='test', host='hpcs')
    # proj.appendTask(task)

    # import jms
    # task.setJMS(jms.LSF())
    # task.setJMS('LSF')
    # import connection
    # conn = connection.Connection('133.66.117.139', password='')
    # task.setConnection(conn)

    # import paics
    # cmd = paics.Paics(task)

    # task.setCommand(cmd)

    # print 'task = ', task.getLabel()
    # print 'task id = ', task.getId()
    # print 'local = ', task.local.getPath()
    # print 'remote = ', task.remote.getPath()
    # print 'cmd_envs = ', task.getCommand().getEnvs()
    # print 'cmd_path = ', task.getCommand().getPath()
    # print 'cmd_name = ', task.getCommand().getName()
    # t.put()
    # t.setup('C:\\Home_Ishikura\\docs\\Nagara\\src\\local-root\\test\\fmo-h2o-4-631gdp.inp')
    # input_file = 'C:\\Home_Ishikura\\docs\\Nagara\\src\\local-root\\test\\fmo-h2o-4-631gdp.inp'
    # input_file = 'C:\Home_Ishikura\docs\Nagara\src\local-root\test\fmo-h2o-4-631gdp.inp'
    # t.setup(input_fn=input_file)
    # task.run(input_fn=input_file)
    # conn.close()


