#  -*- encoding: utf-8 -*-
# Copyright (C)  2009 Takakazu Ishikura
import os, sys
import connection
from abc import abstractmethod, abstractproperty, ABCMeta

class IJMSInfo():
    __metaclass__ =  ABCMeta

    @abstractmethod
    def get_info(self): pass

    @abstractmethod
    def get_core_info(self): pass

    @abstractmethod
    def get_node_info(self): pass

    @abstractmethod
    def set_config(self): pass


class IHostInfo():
    __metaclass__ =  ABCMeta

    @abstractmethod
    def get_info(self): pass

    @abstractmethod
    def set_channel(self, channel): pass


class IConfigInfo():
    __metaclass__ =  ABCMeta

    @abstractmethod
    def set_channel(self, channel): pass

    @abstractmethod
    def check(self, arg): pass

class LocalInfo(IJMSInfo): pass

class MPIInfo(IJMSInfo): pass

class NQSInfo(IJMSInfo): pass


class LSFInfo(IJMSInfo):
    def __init__(self, config=None, precmd=''):
        if config:
            self.set_config(config)
        self.__precmd = precmd
        self.__info_history = []

    def set_config(self, config, precmd=''):
        self.__config = config
        self.__setup()

    def __setup(self):
        self.__channel = connection.Connection(
            host = self.__config['host'],
            username = self.__config['user'],
            password = self.__config['passwd'],
        )

    def __retrieve_node_info(self):
        """Get the host information by dictionary."""
        if not self.__channel: 
            self.__setup()
        
        cmd = self.__precmd +  ';bhosts -w'
        output = self.__channel.execute(cmd)
        job_info_list = []
        output[0]
        keys = output[0].split()
        for line in output[1:]:
            cols = line.split()
            job_info = {
                keys[0] : cols[0],
                keys[1] : cols[1],
                keys[2] : cols[2],
                keys[3] : int(cols[3]),
                keys[4] : int(cols[4]),
                keys[5] : int(cols[5]),
                keys[6] : int(cols[6]),
                keys[7] : int(cols[7]),
                keys[8] : int(cols[8]),
            }
            job_info_list.append( job_info )
        self.__info_history.append( job_info_list )

    def get_info(self, n=-1):
        self.__retrieve_node_info()
        return self.__info_history[n]

    def get_core_info(self):
        if self.__info_history == []:
            self.__retrieve_node_info()
        infolist = self.__info_history[-1]
        all_cores = 0
        free_cores = 0
        run_cores = 0
        for info in infolist:
            all_cores  += info['MAX']
            run_cores  += info['RUN']

        free_cores = all_cores - run_cores
        return all_cores, run_cores, free_cores

    def get_node_info(self):
        if self.__info_history == []:
            self.__retrieve_node_info()
        infolist = self.__info_history[-1]
        all_nodes = len(infolist)
        unavail_nodes = 0
        closed_nodes = 0
        part_nodes = 0
        full_ok_nodes = 0
        for info in infolist:
            if info['STATUS'] in ['unavail', 'busy', 'unknown']:
                unavail_nodes += 1
            elif info['STATUS'] == 'closed_Full':
                closed_nodes += 1
                continue
            elif info['MAX'] - info['RUN'] != 0:
                part_nodes += 1
                continue
            else:
                full_ok_nodes += 1
        nodeinfo = dict(
            nnode = all_nodes,
            unavail = unavail_nodes,
            ok = full_ok_nodes,
            part = part_nodes,
            closed = closed_nodes
        )
        return nodeinfo

    def get_charge(self): pass

    def get_free(self): pass

    def close(self):
        self.__channel.close()

    def get_job_info(self, id, all=False):
        """Get the job information by dictionary."""
        if not self.__channel: 
            self.__setup()

        option = ''
        if all:
            option += ' -u all '
        
        cmd = self.__precmd +  ';bjobs -w ' + option + str(id)
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

        return job_info_dict


def main():
    ssh_config = dict(
        host = '133.66.117.139',
        passwd = 'sdio3871',
        user = 'ishikura',
    )
    hpcs = LSFInfo(ssh_config, precmd='source /etc/profile.local')
    # for job_info in jmsinfo.get_info():
    #     print job_info

    for i in hpcs.get_info():
        print i
    
    print hpcs.get_core_info()
    print hpcs.get_node_info()

    id = 5555
    if hpcs.get_job_info(id):
        for k, v in hpcs.get_job_info(id).items():
            print k, ' = ', v
    else:
        print id, ' is not found.'

    hpcs.close()

if __name__ == '__main__':
    main()
