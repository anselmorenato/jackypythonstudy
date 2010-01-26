# _*_ coding: utf-8 _*_
# Copyright (C)  2010 - 2009/11/22 Takakazu Ishikura

# standard modules
import os, sys
from optparse import OptionParser, OptionValueError
from abc import abstractmethod, abstractproperty, ABCMeta
import time

# nagara modules
from exception import NagaraException
import connection
if __name__ == '__main__':
    sys.path.append('../utils')

from config  import Config
from pattern import Null
from log     import Log

import abstractjms

# jms_dict
def get_jms(jms_class_name):
    jms_dict = dict(
        Win     = Win,      # Local
        Mac     = Mac,      # Local
        Linux   = Linux,    # Local
        Single  = Single,   # Remote
        MPI     = MPI,      # Remote
        LSF     = LSF,      # Remote
        NQS     = NQS,      # Remote
        JQS     = JQS,      # Remote
    )
    return jms_dict(jms_class_name)

class LSFException(NagaraException): pass
class LSF(abstractjms.IJobManagerSystem):

    def __init__(self, job=Null(), channel=None, name='', intensive=True,
                 remote_path='', runscript_fn='run.sh', host=None,
                 nproc=1, nnode=1, node_list=[]):

        self.initialize()

        self._job = job
        if self._job:
            self.reload_job()
        else:
            self.__channel      = channel
            self.__name         = name
            self.__remote_path  = remote_path
            self.__runscript_fn = runscript_fn
            self.__intensive    = intensive

        c = Config()

        self._nproc     = nproc
        self._nnode     = nnode
        self._node_list = node_list
        if host:
            self.__host = host
        else:
            self.__host = c.get_common()['location']['default']
        self.__id = None

        host_config = c.get_common()['location'][self.__host]
        self.__init_file   = host_config['init_file']
        self.__mpi_command = host_config['mpi_command']

        # lsf commands
        self.__rerun_command  = 'bresume '
        self.__stop_command   = 'bstop '
        self.__cancel_command = 'bkill ' 
        self.__submit_template = (
            'bsub -o jms.log -J {jobname} -n {nproc}'
        )

    def get_job_info(self, id=0, all=False):
        """Get the job information by dictionary."""

        if id:
            self.__id = id

        if not self.__id:
            job_info_dict = {}
            return job_info_dict

        option = ''
        if all:
            option += ' -u all '
        
        pre_cmd = 'source ' + self.__init_file + ';'
        cmd = pre_cmd +  'bjobs -w ' + option + str(self.__id)
        output = self.__channel.execute(cmd)

        if len(output) == 1:
            job_info_dict = {}

        elif len(output) >= 2:
            cols = output[1].split()

            job_info_dict = dict(
                id         = cols[0],
                user       = cols[1],
                status     = cols[2],
                queue      = cols[3],
                from_host  = cols[4],
                exec_hosts = [cols[5]],
                start_time = cols[-3:]
            ) 

            if len(output) >= 3:
                for line in output[2:]:
                    job_info_dict['exec_hosts'].append( line.strip() )
                
            ncore = 0
            for h in job_info_dict['exec_hosts']:
                try:
                    ncore += int( h.split('*')[0] )
                except ValueError:
                    ncore += 1

            job_info_dict['ncore'] = ncore
            job_info_dict['nnode'] = len( job_info_dict['exec_hosts'] )

        else:
            raise LSFException()

        return job_info_dict

    def get_submit_command(self):
        """Return the job management command by string."""
        options = ''
        self.reload_job()
        np = self._nproc
        nn = self._nnode
        if self._node_list:
            nl = ' '.join(self._node_list)
            options += '-m "{node_list}"'.format(node_list=nl)
        jn = 'nagara_job_' + self.__name

        submit_cmd = self.__submit_template.format(nproc=np, jobname=jn)

        if self.__intensive:
            options += ' -R "span[hosts=1]" '

        submit_cmd = submit_cmd + ' ' + options
        return submit_cmd

    def do_submit(self):
        self.reload_job()
        rdir = self.__remote_path
        run_script = rdir + '/' + self.__runscript_fn

        # make submit command
        pre_cmd = 'source ' + self.__init_file + ';'
        cd_cmd  = 'cd ' + self.__remote_path + ';'
        submit_cmd = self.get_submit_command() + ' ' + run_script
        command = pre_cmd + cd_cmd + submit_cmd
        if __debug__: Log(command)

        # submit
        output = self.__channel.execute(command)

        # check the submit command and get lsf job id
        lsf_id = output[0].split()[1]
        try:
            self.__id = int(lsf_id[1:-1])
        except ValueError:
            raise abstractjms.JMSSubmittedError()

    def do_rerun(self):
        pre_cmd = 'source ' + self.__init_file + ';'
        command = pre_cmd + self.__rerun_command + ' ' + str(self.__id)
        self.__channel.execute(command)

    def do_stop(self):
        pre_cmd = 'source ' + self.__init_file + ';'
        command = pre_cmd + self.__stop_command + ' ' + str(self.__id)
        self.__channel.execute(command)

    def do_cancel(self):
        pre_cmd = 'source ' + self.__init_file + ';'
        command = pre_cmd + self.__cancel_command + ' ' + str(self.__id)
        self.__channel.execute(command)

    def is_pending(self):
        return self.__is_status('PEND')

    def is_running(self):
        return self.__is_status('RUN')

    def is_stopping(self):
        return self.__is_status('USUSP')

    def is_done(self):
        if self.__is_status('DONE'):
            ret = True

        else:
            jms_log_fn = self.__remote_path + '/jms.log'
            if self.__channel.exists(jms_log_fn): # 'jms.log' exists
                file = self.__channel.open(jms_log_fn)
                log_lines =  file.readlines()
                file.close()

                if log_lines[1].find('Done') >= 0: # succecefully
                    ret = True

                else: # when job is error, get the error log
                    for i, line in enumerate(log_lines):
                        if line.find('The output (if any) follows:') >= 0:
                            error_log = '\n'.join(log_lines[i:])
                            break
                    raise abstractjms.ProgramError(data=error_log)

            else: # delayed time
                ret = False

        return ret

    def is_canceled(self):
        if self.__is_status('EXIT'):
            ret = True

        else:
            jms_log_fn = self.__remote_path + '/jms.log'
            if self.__channel.exists(jms_log_fn): # 'jms.log' exists
                file = self.__channel.open(jms_log_fn)
                log_lines =  file.readlines()
                file.close()

                if log_lines[1].find('Exited') >= 0: # canceled
                    ret = True
                else:
                    ret = False

            else:
                ret = False
                # raise abstractjms.JMSError()

        return ret

    def __is_status(self, status):
        status_value = self.get_job_info().get('status')
        if status:
            if status == status_value:
                ret = True
            else:
                ret = False
        else:
            ret = False

        return ret

    def reload_job(self):
        if self._job:
            self.__channel     = self._job.task.get_channel()
            self.__name        = self._job.name
            self.__remote_path = self._job.task.remote.path
            self.__runscript   = self._job.task.remote.get_runscript_fn()
            self.__intensive   = self._job.is_intensive()

    def set_intensive(self, b=True):
        self.__intensive = b


class Win(abstractjms.IJobManagerSystem): pass
class Mac(abstractjms.IJobManagerSystem): pass
class Linux(abstractjms.IJobManagerSystem): pass
class Single(abstractjms.IJobManagerSystem): pass
class MPI(abstractjms.IJobManagerSystem): pass


class Local(object):

    def run(self, cmd):
        # args = self.jmscmd.split()
        # popen_args = dict(
        #     args   = command.split(),
        #     stdin  = None,
        #     stdout = PIPE,
        #     stderr = PIPE,
        #     shell  = False,
        #     env    = os.environ,
        # )        
        # proc = Popen( **popen_args )
        # stdout, stderr, pid = proc.stdout, proc.stderr, proc.pid
        # return (stdout, stderr, pid)
        pass

class Single(object):

    def __init__(self, log=None):

        # self.nproc   = nproc
        self._jmscmd = None

    def log(self, message):
        if self._log: self._log.write(message)

    pass

    def getCommand(self):
        """Return the job management command by string."""
        # self.jmscmd = ('bsub -o %s -J %s -m %s -n %d run.sh'
        #                % (self.logfile, self.taskname, self.hosts, self.nproc))
        self._jmscmd = ''
        return self._jmscmd

    def getMPICmd(self):
        """Return a mpi command for the jms."""
        self.mpicmd = ''
        return self.mpicmd

    def getType(self):
        return self._type




class NQS(abstractjms.IJobManagerSystem):

    def __init__(self, nproc=1):
        self.mpi_cmd = 'mpiexec'
        self.nproc = 1
        JobNanager.__init__(self)

    def getPrefix(self):
        return self.mpi_cmd + ' -n ' + str(self.nproc)

    def getQueueName(self): pass

    def setup(self):
        # setup nqs options
        if 1 <= nproc <= 7:
            queue = 'p8'
        elif 8 <= nproc <= 15:
            queue = 'p16'
        elif 16 <= nproc <= 63:
            queue = 'p64'
        elif 64 <= nproc <= 127:
            queue = 'p128'
        elif 128 <= nproc <= 255:
            queue = 'p256'
        else:
            raise "ErrorNProcess"

        self.__jmsopts = dict(
            queue = queue,
            stdlog = self.logfile,
            nproc  = nproc+1,
            cputime = '',
            memory = '',
            mail = None,
        )
        self.jmscmd = ('qsub -q %(queue)s -eo -o %(stdlog)s -lP %(nproc) run.sh'
                      % self.__jmsopts)

        self.header = '#! /bin/sh'
        self.__mpicmd = 'mpiexec -n ' + str(nproc) + '\\'

class JQS(abstractjms.IJobManagerSystem):

    def setup(self):
        self.jmscmd = 'jsub -q PA' # or PB


class JobManager(object):
    def __init__(self):
        self.nproc
        self.mpi_cmd = 'mpijob mpirun'
        self.options = None
        self.workdir = None
        pass

    def getPrefix(self):
        raise NotImplementationError

    def getJobCmd(self): pass


# class LSF(JobManager):
#     def __init__(self, name, nproc=1):
#         JobManager.__init__(self)
#         self.name  = bsub
#         self.nproc = nproc
#         self.options = {
#             '-o' : 'lsf.log',
#             '-J' : self.name,
#             '-m' : None,
#             '-n' : self.nproc,
#         }
# 
#     def getPrefix(self):
#         return self.mpi_cmd
# 
#     def getCommand(self):
#         """Get the command line for LSF."""
#         opts = [ key+' '+value for key, value in self.options.items() ]
#         return = self.name + ' ' + ' '.join(opts)


        

class UnknownJobManager(object):
    def __init__(self, **options):
        JobNanager.__init__(self)

    def getPrefix(self): pass


def runCommand(command):
    """ run command and return tuple of (output, status)
    """
    popen_args = dict(
        args   = command.split(),
        stdin  = None,
        stdout = PIPE,
        stderr = PIPE,
        shell  = False,
        env    = os.environ,
    )        
    proc = Popen( **popen_args )
    stdout, stderr, pid = proc.stdout, proc.stderr, proc.pid
    return (stdout, stderr, pid)



if __name__ == "__main__":

    ssh_config = dict(
        host = '133.66.117.139',
        passwd = 'sdio3871',
        user = 'ishikura',
    )

    channel = connection.Connection(
        host     = ssh_config['host'],
        username = ssh_config['user'],
        password = ssh_config['passwd'],
    )

    remote_path = '/home/ishikura/Nagara/projects/paics-test.1'
    #remote_path = '/home/ishikura/'
    runscript_fn = 'run.sh'

    lsf = LSF(
        remote_path   = remote_path,
        runscript_fn  = runscript_fn,
        channel       = channel,
        name          = 'test',
    )

    def print_data(lsf, id=0):
        job_info_dict = lsf.get_job_info(id=id)
        print '==== id = ', job_info_dict['id'], '============================='

        for k, v in job_info_dict.items():
            print k, ' = ', v

        print 'is_pending', lsf.is_pending()
        print 'is_running', lsf.is_running()
        print 'is_done',    lsf.is_done()
        print 'is_stopping',lsf.is_stopping()
        print 'is_canceled',lsf.is_canceled()

    # lsf.do_submit()
    # print_data(lsf)
    # time.sleep(5)
    # print_data(lsf)
    # lsf.do_stop()
    # print_data(lsf)
    # lsf.do_cancel() 

    # lsf.set_resources(node_list=['hpcs18'])

    lsf.do_submit()
    print_data(lsf)
    lsf.check_run().join()
    lsf.do_stop()
    lsf.check_stop().join()
    lsf.do_rerun()
    lsf.check_run()

    # print_data(lsf, 18109)
    # print_data(lsf, 18193)
    # lsf.do_cancel()
    # lsf.check_cancel()
    # lsf.check_cancel().join()
    print_data(lsf)


    channel.close()

    from pubsub.utils import printTreeDocs
    printTreeDocs(extra="a")
    print '\nTopic tree listeners:'
    printTreeDocs(extra="L")





    # single = Single()
    # print a.getCommand(), single.getCommand()
    # print a.getMPICmd(), single.getMPICmd()

    # jobadmin = JobAdmin('lsf')
    # print jobadmin.printHosts()

