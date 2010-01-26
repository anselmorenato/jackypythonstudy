#  -*- encoding: utf-8 -*-

# available classes
__all__ =['DataConverter', 'ToNDO_Parser', 'FromNDO_Formatter']

# Standard modules
import os, sys
from abc import ABCMeta, abstractmethod, abstractproperty

# additional modules

# Nagara  modules
# sys.path.append('..')
if __name__ == '__main__':
    sys.path.append('../utils')
from data import Data
from deco import threaded
from exception  import NagaraException
from config     import Config
from plugin     import load_converter_module

user_plugin = Config().get_user_plugin()
converter_module = load_converter_module(user_plugin)

# ((PDB), (AMBER_PRMTOP, AMBER_RESTART)) = 
#     PDB_AMBER_PRMTOP_AMBER_RESTART_Converter
# 
# ((PDB), (AMBER_LIB)) = PDB_AMBER_LIB_Converter


# exceptions ===================================================================
class DataConvertException(NagaraException): pass
class DataNotFoundException(DataConvertException): pass
class FormatCannotConvertError(DataConvertException): pass

# abstract class, algorithm convertion only
class DataConverter(object):

    data_context = [
        'IntFileData', 'ExtFileData', 'NagaraData', 'FormattedStringData',
        'RemoteFileData', 'ExtRemoteData', 'ExtDBData'
    ]

    def __init__(self, input_data_list, output_format_list=[],
                 output_filename_list=[], use_command=True, setting=None):
        """Constructor."""
        # if formats == [], then format will be nagara object

        if len(output_filename_list) != 0:
            if len(output_format_list) != len(output_filename_list):
                mes = ('the number of format list '
                       'and file list for output is different.')
                raise DataConveterException(mes)

        self.__input_data_list = input_data_list
        self.__output_format_list = output_format_list
        self.__use_command = use_command

        self.__converted = False
        self.__set_convert_strategy()

    def __sort_data_by_list(self, input_data_list, output_format_list):
        sorted_data_list = []
        for out_fmt in output_format_list:
            for in_data in input_data_list:
                if in_data.format == out_fmt:
                    sorted_data_list.append( in_data )
        return sorted_data_list

    #@threaded
    def __set_convert_strategy(self):

        # find the converter for input_format_list and output_format_list
        in_fmt_set  = set([ data.format for data in self.__input_data_list ])
        out_fmt_set = set(self.__output_format_list)
        converter_dict = converter_module.converter_dict

        if in_fmt_set == out_fmt_set:
            self.__define_strategy_1()

        elif (in_fmt_set == set(['NagaraData']) and
              out_fmt_set == set[('NagaraData')]):
            raise FormatCannotConvertError()

        elif (in_fmt_set == set(['NagaraData']) and # input:  NDO
              out_fmt_set != set(['NagaraData'])):   # output: Other
            self.__define_strategy_2(converter_dict, out_fmt_set)

        elif (in_fmt_set != set(['NagaraData']) and # input: Other
              out_fmt_set == set(['NagaraData'])):   # output: NDO
            self.__define_strategy_3(converter_dict, in_fmt_set)

        else:
            # use external converter program
            if self.__use_command:
                self.__define_strategy_4(
                    converter_dict, in_fmt_set, out_fmt_set)

            else: # use NagaraDataObject
                self.__define_strategy_5(
                    converter_dict, in_fmt_set, out_fmt_set)

    def __define_strategy_1(self):
        sorted_data_list = self.__sort_data_by_list(
            self.__input_data_list, self.__output_format_list)
        # set convert strategy
        self.__convert_strategy = SameFormatConverter(
            input_data_list = sorted_data_list,
            output_filename_list = output_filename_list
        )

    def __define_strategy_2(self, conv_dict, out_fmt_set):
        for in_out_fmt in conv_dict:
            in_fmt, out_fmt = in_out_fmt
            if (set(in_fmt) == set(['NagaraData']) and
                set(out_fmt) == out_fmt_set):
                conv_cls = convr_dict[in_out_fmt]
                break
        else:
            mes = 'Not Found Output Format'
            raise FormatCannotConvertError()

        # set convert strategy
        self.__convert_strategy = FromNDO_Formatter(
            converter_cls = conv_cls, 
            input_data = self.__input_data_list[0],
            output_format_list = self.__output_format_list
        )

    def __define_strategy_3(self, conv_dict, in_fmt_set):
        for in_out_fmt in conv_dict:
            in_fmt, out_fmt = in_out_fmt
            if (set(in_fmt) == in_fmt_set and
                set(out_fmt) == set(['NagaraData'])):
                conv_cls = conv_dict[in_out_fmt]
                break
        else:
            mes = 'Not Found Input Format'
            raise FormatCannotConvertError(mes)

        # set convert strategy
        self.__convert_strategy = ToNDO_Parser(
            converter_cls = conv_cls,
            input_data_list = self.__input_data_list,
        )

    def __define_strategy_4(self, conv_dict, in_fmt_set, out_fmt_set):
        for in_out_fmt in conv_dict:
            in_fmt, out_fmt = in_out_fmt
            if (set(in_fmt) == in_fmt_set and
                set(out_fmt) == out_fmt_set):
                conv_cls = conv_dict[in_out_fmt]
                break
        else:
            raise FormatCannotConvertError()

        # set convert strategy
        self.__convert_strategy = ConverterCommand(
            converter_cls = conv_cls,
            input_data_list = self.__input_data_list,
            output_format_list = self.__output_format_list,
            output_filename_list = self.__output_filename_list
        )

    def __define_strategy_5(self, conv_dict, in_fmt_set, out_fmt_set):
        conv_cls_list = []
        for in_out_fmt in conv_dict:
            in_fmt, out_fmt = in_out_fmt
            if (set(in_fmt) == in_fmt_set and
                set(out_fmt) == set(['NagaraData'])):
                conv_cls1 = conv_dict[in_out_fmt] 
                break
        else:
            mes = 'Not Found Input Format'
            raise FormatCannotConvertError(mes)

        # for output format
        for in_out_fmt in conv_dict:
            in_fmt, out_fmt = in_out_fmt
            if (set(in_fmt) == set(['NagaraData']) and
                set(out_fmt) == out_fmt_set):
                conv_cls2 = conv_dict[in_out_fmt]
                break
        else:
            mes = 'Not Found Output Format'
            raise FormatCannotConvertError()

        # set convert strategy
        self.__convert_strategy = ThroughNDOConverter(
            converter_cls_list = [conv_cls1, conv_cls2],
            input_data_list = self.__input_data_list,
            output_format_list = self.__output_format_list
        )

    # @threaded
    def convert(self):
        if not self.__converted:
            self.__convert_strategy.convert()

    def set_property(self):
        self.__convert_strategy.copy_property()

    def get_data_list(self):
        self.convert()
        self.__converted = True
        return self.__convert_strategy.get_data_list()
    

# Interface
class IConverterStrategy(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def convert(self): pass

    @abstractmethod
    def set_property(self): pass

    @abstractmethod
    def get_data_list(self): pass


class SameFormatConverter(IConverterStrategy):

    def __init__(self, input_data_list, output_filename_list):
        self.__input_data_list = input_data_list
        self.__output_filename_list = output_filename_list

        self.__output_data_list = []

    def convert(self):
        inp_d_list = self.__input_data_list
        out_f_list = self.__output_filename_list
        for d, file in zip(inp_d_list, out_f_list):
            odata = Data( d.project, type=d.type)
            odata.format = d.format
            odata.file   = file
            self.__output_data_list.append(odata)

    def get_data_list(self):
        self.convert()
        return self.__output_data_list

    def set_property(self):
        inp_d_list = self.__input_data_list
        out_d_list = self.__output_data_list
        for inpd, outd in zip(inp_d_list, out_d_list):
            outd.multiplicity = inpd.multiplicity


class ToNDO_Parser(IConverterStrategy):

    """
    The class that parse the formatted content
    and convert it to Nagara Data Object.
    """

    def __init__(self, converter_cls, input_data_list):
        """Constructor."""
        # determine Parser to use by analysis of format
        # number of file set == number of format set

        self.__parser_cls = converter_cls
        self.__input_data_list = input_data_list

    def convert(self):
        inp_d_list = self.__input_data_list
        file_dict = dict([(d.format, d.file) for d in self.__input_data_list])

        parser = self.__parser_cls()
        parser.set_file_dict( file_dict )

        odata = Data( inp_d_list[0].project, type=inp_d_list[0].type)
        odata.format = 'NagaraData'
        odata.ndo   = parser.get_ndo()
        self.__output_data = odata

    def get_data_list(self):
        self.convert()
        return [self.__output_data]

    def set_property(self):
        self.__output_data.multiplicity = self.__input_data_list[0].multiplicity


class FormatterError(DataConvertException): pass
class FromNDO_Formatter(IConverterStrategy):

    """
    The class to convert Nagara Data Object to a formatted content.
    """

    def __init__(self, converter_cls, input_data, output_format_list):
        """Constructor."""
        self.__formatter_cls      = converter_cls
        self.__input_data         = input_data
        self.__output_format_list = output_format_list

    def convert(self):
        inpd = self.__input_data
        formatter = self.__formatter_cls()
        formatter.set_ndo( inpd.ndo )
        file_dict = formatter.get_file_dict()

        odata_list = []
        for out_fmt in self.__output_format_list:
            odata = Data( inpd.project, type=inpd.type)
            odata.format = out_fmt
            file = file_dict[out_fn]
            if file:
                odata.file = file
            else:
                raise FormatterError()
            odata_list.append( odata )

        self.__output_data_list = odata_list

    def get_data_list(self):
        self.convert()
        return self.__output_data_list

    def set_property(self):
        for outd in self.__output_data_list:
            outd.multiplicity = self.__input_data.multiplicity


class ThroughNDOConverter(IConverterStrategy):

    def __init__(self, converter_cls_list, input_data_list, output_format_list):
        self.__converter_cls_list = converter_cls_list
        self.__input_data_list    = input_data_list
        self.__output_format_list = output_format_list

    def convert(self):
        conv_cls1, conv_cls2 = self.__converter_cls_list

        # parser
        parser = conv_cls1()
        file_dict = dict([(d.format, d.file) for d in self.__input_data_list])
        parser.set_file_dict( file_dict )

        # formatter
        formatter = conv_cls2()
        formatter.set_ndo( parser.get_ndo() )
        file_dict = formatter.get_file_dict()

        odata_list = []
        for out_fmt in self.__output_format_list:
            odata = Data( inpd.project, type=inpd.type)
            odata.format = out_fmt
            file = file_dict[out_fn]
            if file:
                odata.file = file
            else:
                raise FormatterError()
            odata_list.append( odata )

        self.__output_data_list = odata_list

    def get_data_list(self):
        self.convert()
        return self.__output_data_list

    def set_property(self):
        for outd in self.__output_data_list:
            outd.multiplicity = self.__input_data_list[0].multiplicity


class ConverterCommand(IConverterStrategy):

    def __init__(self, converter_cls, input_data_list,
                output_format_list, output_filename_list):
        self.__converter_cls        = converter_cls
        self.__input_data_list      = input_data_list
        self.__output_format_list   = output_format_list
        self.__output_filename_list = output_filename_list

    def convert(self):
        conv_obj = self.__converter_cls()

        input_dict = dict(
            [(d.format, d.file) for d in self.__input_data_list]
        )
        output_tup = zip(self.__output_format_list, self.output_filename_list)

        conv_obj.set_input_dict( input_dict )
        conv_obj.set_output_dict( dict(output_tup) )

        # run converter command and get files
        fn_dict = conv_obj.run_convert()

        odata_list = []
        for fmt, fn in output_tup:
            odata = Data( inpd.project, type=inpd.type)
            odata.format   = fmt
            if os.path.exists(fn):
                odata.filename = fn
            else:
                raise ConverterCommandException()

            odata_list.append( odata )

        self.__output_data_list = odata_list

    def get_data_list(self):
        self.convert()
        return sefl.__output_data_list

    def set_property(self):
        for outd in self.__output_data_list:
            outd.multiplicity = self.__input_data_list[0].multiplicity


class DataTypeChecker(object):
    """Class to inspect the data type."""
    def __init__(self):
        pass
        
