# _*_ coding: utf-8 _*_
# Copyright (C)  2009 Takakazu Ishikura

# standard modules
import os, sys

# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )
from core.exception import NagaraException
from utils.setting_helper import ConvertManager

# Exceptions ===================================================================
class AmberSettingConvertException(NagaraException): pass
class InvalidSettingKeyword(NagaraException): pass

#-------------------------------------------------------------------------------

class FromNagaraConverter(object):

    def __init__(self, settings, toname=None, header=None):
        self.__toname = toname
        self.__header = header

        self.__settings = settings
        self.__fd = None

    def getFormattedFile(self):
        return self.__fd

    # property: toname
    def getToName(self):
        return self.__toname

    def setToName(self, toname):
        self.__toname = toname
    toname = property(getToName, setToName)

    # property: header
    def getHeader(self):
        return self.__header

    def setHeader(self, header):
        self.__header = header
    header = property(getHeader, setHeader)

    def convert(self):

        from cStringIO import StringIO
        fd = StringIO()

        if   self.__toname == 'Energy':
            # EnergyConverter()
            pass
        elif self.__toname.lower() == 'optimize':
            # if self.__settings['taskobject'].lower() != 'optimize':
            #     raise InvalidSettingKeyword('optimize')

            cntrl_options = OptimizeConverter(self.__settings).getOptions()
            cntrl_content = SettingFormatter(
                cntrl_options, 'cntrl').getContent()

        # wt_content_list = self.getWeightContentent()
        fd.write(self.__header + '\n')
        fd.write(cntrl_content + '\n')
        # fd.write('\n'.join(wt_content_list))
        self.__fd = fd

    def getFile(self):
        self.__fd.seek(0)
        return self.__fd

    def getWeightContent(self):
        cond_type_dict = self.__settings['vary conditions']['type_dict']
        content_list = []
        for ct, args in cond_type_dict.items():
            conv = WtConverter(
                ct, args['start_value'], args['end'], self.__settings)
            content_list.append( conv.get_content() )
        return content_list


class EnergyConverter(object):

    option = ConvertManager()

    def __init__(self, settings):
        self.__settings = settings
        self.option.convert_all(self) 
        self.__new_options = self.option.get_converted_options()

    def convert(self):
        self.option.convert_all(self)

    def format(self):
        SettingFormatter(self.__new_options, 'cntrl')

    def get_content(self):
        self.convert()
        self.format()
        return self.__content

    @option
    def imin(self):
        return 1

    @option
    def ntmin(self):
        method = self.__setting['minimize']['method']
        if   method == 'steepest_descent'  : return 2
        elif method == 'conjugate_gradient': return 0
        else: raise AmberSettingConvertException()

    @option
    def maxcyc(self):
        return self.__setting['minimize']['method']

    def ncyc(self):
        return 0

    def ntf(self):
        if not self.__settings['restraint']:
            return 1
        else:
            return 1

    def ntc(self):
        if not self.__settings['restraint']:
            return 1
        else:
            return 1

    @option
    def ntt(self):
        method = self.__settings['temp_ctrl'].get(0)
        if   method == 'weak':     ret = 1
        elif method == 'andersen': ret = 2
        elif method == 'langevin': ret = 3
        else: raise NotImplementedError()
        return ret

    @option
    def gamma_ln(self):
        # {temp_ctrl : {langevin:[2}}
        method = self.__settings['temp_ctrl'].get(0)
        params = self.__settings['temp_ctrl']
        if method == 'langevin':
            ret= params['gamma']
        else:
            ret = False
        return ret

    def check_ntt(self):
        pass

class GroupConverter(object):
    def __init__(self):
        pass


class OptimizeConverter(object):

    option = ConvertManager()

    def __init__(self, model):
        self.__model = model
        self.option.convertAll(self) 
        self.__new_option_dict = self.option.getConvertedOptions()

    def getOptions(self):
        return self.__new_option_dict

    @option
    def imin(self):
        return 1

    @option
    def ncyc(self):
        m = self.__model.method
        if   m.optmethod == 'cg':    ret = 0
        elif m.optmethod == 'sd':    ret = m.ncycle
        elif m.optmethod == 'sd+cg': ret = m.ncycle_switch
        else: InvalidSettingKeyword('for ncyc')
        return ret

    @option
    def maxcyc(self):
        return self.__model.method.ncycle


class EnsembleConverter(object):
    pass


class DynamicsConverter(object):

    option = ConvertManager()

    def __init__(self, settings):
        self.__settings = settings
        self.option.convert_all(self) 
        self.__new_options = self.option.get_converted_options()

    def convert(self):
        self.option.convert_all(self)

    def format(self):
        SettingFormatter(self.__new_options, 'cntrl')

    def get_content(self):
        self.convert()
        self.format()
        return self.__content

    @option
    def imin(self):
        method = self.__settings['object']
        if   method == 'energy':
            self.__do_energy
            ret = 1
        elif method == 'minimize': ret = 1
        elif method == 'dynamics': ret = 0
        else: pass
        return ret

    @option
    def dt(self):
        return self.__settings['integrator']['dt']

    @option
    def tempi(self):
        ensemble = self.__settings['ensemble']
        return ensemble['temperature']

    @option
    def nstlim(self):
        l = self.__settings['integrator']['time_limit']
        dt = self.__settings['integrator']['dt']
        nstep = l / dt
        return int(nstep)

    @option
    def temp0(self):
        pass

    # {temp_ctrl : {0: 'langevin', 'gamma':2.0}}
    @option
    def ntt(self):
        method = self.__settings['temp_ctrl'].get(0)
        if   method == 'weak':     ret = 1
        elif method == 'andersen': ret = 2
        elif method == 'langevin': ret = 3
        else: raise NotImplementedError()
        return ret

    @option
    def gamma_ln(self):
        # {temp_ctrl : {langevin:[2}}
        method = self.__settings['temp_ctrl'].get(0)
        params = self.__settings['temp_ctrl']
        if method == 'langevin':
            ret= params['gamma']
        else:
            ret = False
        return ret

    def check_ntt(self):
        pass

#     ntr = 1, restraintmask=':1-109 & !@H=',
#     restraint_wt = 99.0,

class RestraintConverter(object):

    def __init__(self, group, args, settings):
        self.__group = group


    def ntr(self):
        group_list = self.__settings['restraint']['group_list']



class PositionalRestraint(object):

    option = ConvertManager()

    def __init__(self, args, settings):
        self.__settings = settings



    @option
    def ntr(self):
        return 1

    @option
    def restraintmask(self):
        pass
        # return ':1-109 & !@H=', 

    @option
    def restraint_wt(self):
        return 99.0


class WtConverter(object):

    option = ConvertManager()

    def __init__(self, vary_type, start_value, end_value, settings):
        self.__vary_type   = type
        self.__start_value = start_value
        self.__end_value   = end_value
        self.__settings    = settings

        # convert
        self.option.convert_all(self) 

    def format(self):
        new_options = self.option.get_converted_options()
        return SettingFormatter(new_options, 'wt').get_content()

    @option
    def type(self):
        type_dict = dict(
            # energy weight
            bond        = 'bond',
            angle       = 'angle',
            torsion     = 'torsion',
            improper    = 'improper',
            vdw         = 'vdw',
            coulomb     = 'coulomb',
            nonbond     = 'nb',
            all         = 'all',
            # for other
            temperature = 'temp0',
        )
        return type_dict[ cond_type ]

    @option
    def istep1(self):
        return 0

    @option
    def istep2(self):
        l  = self.__settings['integrator']['time_limit']
        dt = self.__settings['integrator']['dt']
        nstep = l / dt
        return int(nstep)

    @option
    def value1(self):
        return self.__start_value

    @option
    def value2(self):
        return self.__end_value


class ToNagaraConverter(object):
    pass

class NagaraSettingValidator(object):
    pass


class SettingFormatter(object):

    def __init__(self, settings, section_name):
        self.__settings = settings
        self.__section_name = section_name

    def format(self):
        option_lines = []
        count = 0
        for k, v in self.__settings.items():
            if count == 0:
                line = '    {0} = {1}, '.format(k, v)
                count += 1

            elif count == 1:
                kv = '{0} = {1}, '.format(k, v)
                line += kv
                count += 1

            elif count == 2:
                kv = '{0} = {1}, '.format(k, v)
                line += kv
                option_lines.append(line)
                count = 0
                line = ''
            else:
                pass
        option_lines.append(line)

        template = (
            '{0}\n'
            '{1}\n'
            '/\n'
        )
        return template.format(
            '&'+self.__section_name, '\n'.join(option_lines)
        )

    def getContent(self):
        return self.format()

class FilterParser(object):
    pass

#-------------------------------------------------------------------------------


def main():
    from core import plugin

    user_plugin_path = 'Dropbox/Office/myNagara/src/plugin_user'
    user_plugin_abspath = os.path.join(os.environ['HOME'], user_plugin_path )

    model_class = plugin.loadSettingModel('optimize', user_plugin_abspath)
    optimize = model_class()
    print optimize.dump()
    method = optimize.method
    method.ncycle = 10000
    method.optmethod = 'sd'

    # settings = dict(
    #     method = 'dynamics',
    #     dt = 0.002,
    #     time_limit = 10,
    #     temp_ctrl = {'langevin': [5]},
    # )


    fnc = FromNagaraConverter(optimize)
    fnc.toname = 'optimize'
    fnc.header = 'HogeHoge'

    fnc.convert()
    file = fnc.getFile()
    print file.read()


    # m = OptimizeConverter(nagara_setting_dict)



    # a = FromNagaraConverter()

    #a = AmberSetting(settings)

    #for key, val in a.convert().items():
    #    print '{0} = {1}'.format(key, val)
    # print a.get_input_content()


if __name__ == '__main__':
    main()


