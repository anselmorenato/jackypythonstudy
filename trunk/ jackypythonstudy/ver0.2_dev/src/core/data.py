#  -*- encoding: utf-8 -*-
# Copyright (C)  2010 Takakazu Ishikura
#
# $Date$
# $Rev$
# $Author$
#

# standard module
import os, sys
import time
from abc import ABCMeta, abstractmethod, abstractproperty


nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )

# Nagara modules
from config import Config

# Context: InternalLocalFile, ExternalLocalFile, InternalRemoteFile,
#       DataBase, WebAPI,
# Type: System, Trajectory, Plotable,
# Format: NDO, AMBER_RESTART, AMBER_PRMTOP, etc...

from exception import NagaraException
class DataException(NagaraException): pass
class DataTypeError(DataException): pass
class DataFormatError(DataException): pass
class DataReadError(DataException): pass
class DataFileError(DataException): pass
class DataContentError(DataException): pass
class DataRechangeError(DataException): pass


from utils.pattern import Null

# valid types
valid_type_list = [
    # 'System', 'Restart', 'Group', 'Trajectory', 'Energy',
    'System', 'Restart', 'Trajectory', 'Energy',
]

# NagaraData

# Interface for System, Log, Output, Coordinate, 
class Data(object):

    """
    The class to define a data.
    """

    def __init__(self, project, type, name=None, format=None, data=None,
                 multiplicity=0, description=''):
        # (database, web_api)
        # multiplicity = 0: single
        #              = 1: multiple
        #              = 2: sequence

        # type
        if type not in valid_type_list:
            raise DataTypeError(type)
        self.__type = type
        # project
        self.__project = project 
        # id
        self.__id = self.__project.get_hightest_id()
        # name
        if name:
            self.__name = name
        else:
            # self.__name = type + ' data ' + str(self.__id)
            self.__name = 'New Data'

        # data is disabled for default
        self.enable(False)

        self.__context = TempData()

        # channel
        # self.__channel = self.__project.channel
        self.__channel = None
        self.__filename = None

        self.__format = format      # format
        self.__multi = multiplicity # multiplicity

        self.__description = description
        self.__is_complete = False

    @property
    def id(self):
        return self.__id

    # property: name
    def get_name(self):
        return self.__name
    def set_name(self, name):
        self.__name = __name
    name = property(get_name, set_name)

    # property: project
    def get_project(self):
        return self.__project
    def set_project(self, project):
        self.__project = __project
    project = property(get_project, set_project)

    def enable(self, b):
        self.__enable = b

    def get_file(self):
        return self.__context.get_file()

    def set_file(self, file):
        self.__context.set_file( file )

    file = property(get_file, set_file)

    def is_enable(self):
        return self.__enable

    # property: format
    def get_format(self):
        return self.__format
    def set_format(self, format):
        if not isinstance(self.__context, TempData):
            raise DataRechangeError()
        if format == 'NagaraData':
            self.__context = NagaraDataObject()
        else:
            self.__context = FormattedData(format)

    format = property(get_format, set_format)

    def set_local_file(self, filename, format):
        if not isinstance(self.__context, TempData):
            raise DataRechangeError()

        root = self.__project.rootpath
        if filename.find(root) >= 0:
            self.__format   = format
            self.__context  = IntFileData(filename=filename)
        else:
            self.__format   = format
            self.__context  = ExtFileData(filename=filename)

    def set_remote_file(self, filename, format, channel):
        if not isinstance(self.__context, TempData):
            raise DataRechangeError()

        # rip = channel.get_host_by_ip()
        # Config().get_common()[]
        self.__context = RemoteFileData(channel=channel, filename=filename)

    def get_ndo(self):
        print 6666
        if not isinstance(self.__context, NagaraDataObject):
            raise NotImplementedError()
        print 7777
        return self.__context.ndo
    def set_ndo(self, ndo):
        if not ( isinstance(self.__context, TempData) or
                isinstance(self.__context, NagaraDataObject)):
            raise DataRechangeError()

        self.__enable = False
        self.__context = NagaraDataObject(ndo)
    ndo = property(get_ndo, set_ndo)

    # property: description
    def get_desc(self):
        return self.__description
    def set_desc(self, desc):
        self.__description = desc
    description = property(get_desc, set_desc)

    # property: multiplicity
    def get_multiplicity(self):
        return self.__multiplicity
    def set_multiplicity(self, multiplicity):
        self.__multiplicity = __multiplicity
    multiplicity = property(get_multiplicity, set_multiplicity)
    
    @property
    def context(self):
        return self.__context.__class__.__name__

    @property
    def type(self):
        return self.__type

    def delete(self):
        self.__context.delete()
        pass

    def is_empty(self):
        return self.__context.is_empty()

    def is_single(self):
        ret = True if self.__multi==0 else False
        return ret

    def is_multi(self):
        ret = True if self.__multi==1 else False
        return ret

    def is_sequence(self):
        ret = True if self.__multi==2 else False
        return ret

    def is_ndo(self):
        return True if isinstance(self.__context, NagaraDataObject) else False

    def tail(self, nline_back=10, interval=1):
        
        # rfile = conn.open(rfn, 'r')
        # # print rfile.read()
        # for l in tail(rfile): print l,

        # if data is ndo, then raise error
        if self.is_ndo(): raise DataTailError()

        # find the size of the file and move to the end
        file_size = file.stat().st_size
        try:
            # for remote file
            file_size = file.stat().st_size
        except AttributeError:
            # for local file
            file_size = os.fstat(file.fileno()).st_size

        # initial character/line
        avg_char_per_line = 75
        # get lines of the number of nline_back
        while True:
            if avg_char_per_line*nline_back < file_size:
                file.seek(-1 * avg_char_per_line * nline_back, 2)
            else:
                file.seek(0)
                at_start = True if file.tell()==0 else False

            lines = file.read().split('\n')
            if (len(lines) > nline_back+1) or at_start: break

            avg_char_per_line = int(avg_char_per_line*1.2)

        if len(lines) > nline_back:
            start = len(lines) - nline_back - 1
        else:
            start = 0

        yield '\n'.join(lines[start:len(lines)-1]) + '\n'

        # move to the end of file
        file.seek(0, 2)
        # execute like the tail
        try:
            while True:
                where = file.tell()
                line = file.readline()
                if not line:
                    time.sleep(interval)
                    file.seek(where)
                else:
                    yield line

        except KeyboardInterrupt:
            print "Done."
            sys.exit()

    def is_complete(self):
        return self.__complete

    def show(self, out):
        pass

    def dump(self, filename=None):
        pass

    def save(self, filename=None):
        pass

    def show_ndo(self):
        pass

    def copy(self):
        pass

    def delete(self):
        pass


class IDataContext(object):
    """
    Interface class to define a data to be used by Nagaradocstring
    for IDataContext
    """

    __metaclass__ = ABCMeta

    def __init__(self):
        super(IDataContext, self).__init__()
        
    @abstractmethod
    def get_file(self): pass
    @abstractmethod
    def set_file(self, file): pass

    @abstractmethod
    def delete(self): pass

    @abstractmethod
    def exists(self): pass

    @abstractmethod
    def is_empty(self): pass
    

class TempData(IDataContext):

    def get_file(self): return Null()
    def set_file(self, ): pass
    file = property(get_file, set_file)

    def delete(self): pass
    def exists(self): pass
    def is_empty(self): return True
    


import cStringIO as sio
class FormattedData(IDataContext):
    """
    Class to tread the formatted string data, but not file.
    """
    def __init__(self, content=None):
        self.__content = content

    def get_file(self):
        file = sio.StringIO()
        file.write(self.__content)
        file.seek(0)
        return file
    def set_file(self, file):
        self.__content = file.read()
        file.close()
    file = property(get_file, set_file)

    def delete(self):
        pass

    def exists(self):
        if self.__content:
            return True
        else:
            return False

    def is_empty(self):
        return False if self.__content else False


class IntFileData(IDataContext):
    """
    Class to treat the internal file data.
    """
    def __init__(self, filename=None):
        self.__filename = filename

        if os.path.exists(filename):
            self.__exists  = True
            self.__pointer = True
        else:
            self.__exists  = False
            self.__pointer = True

    def get_file(self):
        if self.exists():
            file = open(self.__filename, 'r')
        else:
            raise DataFileError()
        return file

    def set_file(self, file):
        with open(self.__filename, 'w') as infile:
            infile.write( file.read() )
        file.close()

    def delete(self):
        if self.check():
            os.path.remove(self.__filename)

    def exists(self):
        if os.path.exists(self.__filename):
            ret = True
            raise DataFileError()
        else:
            ret = False
        return ret


class ExtFileData(IDataContext):
    """
    Class to treat the external file data.
    """
    def __init__(self, filename=None):
        self.__filename = filename

        if os.path.exists(filename):
            self.__exists  = True
            self.__pointer = True
        else:
            self.__exists  = False
            self.__pointer = True

    def get_file(self):
        if self.exists():
            file = open(self.__filename, 'r')
        else:
            raise DataFileError()
        return file

    def set_file(self, file):
        with open(self.__filename, 'w') as infile:
            infile.write( file.read() )
        file.close()

    def delete(self):
        raise "shouldn't delete the external file."

    def exists(self):
        if os.path.exists(self.__filename):
            ret = True
            # raise DataFileError()
        else:
            ret = False
        return ret

    def is_empty(self):
        return False


class RemoteFileData(IDataContext):

    def __init__(self, filename=None, channel=None):
        self.__filename = filename
        self.__channel = channel

        if channel.exists(filename):
            self.__exists  = True
            self.__pointer = True
        else:
            self.__exists  = False
            self.__pointer = True
        
    # For these methods, the thread is essential.
    def get_file(self):
        if self.exists():
            file = self.__channel.open(self.__filename, 'r')
        else:
            raise DataFileError()
        return file

    def set_file(self, file):
        remote_file = self.__channel.open(self.__filename, 'w')
        remote_file.write( file.read() )
        remote_file.close()
        file.close()

    def delete(self):
        if self.exists():
            os.path.remove(self.__filename)

    def exists(self):
        if self.__chann.exists(self.__filename):
            ret = True
            raise DataFileError()
        else:
            ret = False
        return ret

    def tail(self):
        if not self.exists(): ret = False

        file = self.get_file()
        while 1:
            where = file.tell()
            line = filereadline()
            if not line:
                time.sleep(1)
                file.seek(where)
            else:
                target.write(line)


class NagaraDataObject(object):
    """
    Class to treat Nagara Data (Nagara Data Object)
    """
    def __init__(self, ndo=None):
        self.__ndo = ndo

    def get_ndo(self):
        return self.__ndo
    def set_ndo(self, ndo):
        self.__ndo = ndo
    ndo = property(get_ndo, set_ndo)


class ExtDBData(object): pass
class ExtRemoteData(object): pass

#-------------------------------------------------------------------------------

class Setting(object):

    """
    The class to define a settings.
    """

    def __init__(self):
        pass

def main():
    # d = DataConverter()
    # for k, f in d.convert_dict.items():
    #     print k, f
    import project
    p = project.Project()
    d = Data(p, type='System')
    p.append_data(d)
    print d.context

    pdb_path = '~/Dropbox/Office/Nagara/v02-src/examples/structures/1HEW.pdb'
    pdb_abspath = os.path.expanduser(pdb_path)
    d.set_local_file(filename=pdb_abspath, format='PDB')
    print d.context
    print d.get_file()

    from dataconverter import DataConverter
    dc = DataConverter(
        input_data_list=[d],
        output_format_list=['NagaraData']
    )

    system_data = dc.get_data_list()[0]
    print system_data.context



    system = system_data.ndo
    # for atom in system.atoms:
    #     print atom


    dc2 = DataConverter(
        input_data_list=[system_data], output_format_list=['PDB']
    )
    pdb_data = dc2.get_data_list()[0]
    print 222222222, pdb_data.type
    print 33333333333, pdb_data.context

    # system = sys_ndo.ndo
    # for atom in system.atoms:
    #     print(atom)






if __name__ == '__main__':
    main()

