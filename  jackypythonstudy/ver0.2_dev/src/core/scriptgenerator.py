#  -*- encoding: utf-8 -*-
import os, sys


class ScriptGenerator(object):

    def __init__(self, job):
        self.__command = job.task.command
        self.__jms = job.jms
        self.__place = task.place
        self.__runscript_fn = 'run.sh'

    def __make_submit(self):
        """Make the command line string for submitting"""
        place_cmd = self.__place.get_prepare_cmd() # source /etc/profile.local;
        chdir = 'cd ' + rdir + '/' + self.__script_fn
        jms_cmd = self.__jms.get_cmdline()
        submit_cmdline = place_cmd + ';' + chdir + ';' + jms_cmd
        return submit_cmdline

    def __make_script(self):
        """Make a content string for a run script for this command."""

        # run_script
        header = '#! /bin/sh'
        # self.__jms.get_header()

        # environment of the remote host
        envs = self.__command.get_envs()
        env_lines = [ '{0}={1}'.format(key.strip(),value.strip())
                      for key, value in self._envs.items() ]
        env_lines.append('TASK_PATH={0}'.format(self.__task_path))

        # prefix, for mpi, and other
        if self.__command.use_mpi:
            mpi_cmd = self.__jms.get_mpi()
        else:
            mpi_cmd = ''

        # get the command line
        cmdline = self.__command.get_cmdline()

        # make the script contents
        run_script = (
            header + '\n' +
            '\n'.join(env_lines) + '\n\n' +
            mpi_cmd + ' ' + 
            cmdline + '\n'
        )
        return run_script

    def __generate_script(self):
        """Generate a run script for this command."""
        dir = self.__task.get_path()
        runscript_fn = os.path.join(dir, self.__runscript_fn)
        with open(runscript_fn, 'wb') as file:
            file.write(self.__make_script())



#    def __genInputFile(self, input_fn=None):
#        """Generate a input data file on the local host."""
#        src_path = input_fn 
#        dst_fn = self._opts['input_file']
#        ldir = self._task.local.getPath()
#        dst_path = os.path.join(ldir,dst_fn)
#        if file:
#            # print src_path, dst_path
#            src_file = open(src_path, 'rb')
#            dst_file = open(dst_path, 'wb')
#            dst_file.write(src_file.read())
#            src_file.close()
#            dst_file.close()
#            # shutil.copyfile(src_path, dst_path)
#        else:
#            input_file = open(dst_path, 'wb')
#            input_file.write(self.__mkInputData())
#            input_file.close()
#

