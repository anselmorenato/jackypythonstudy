# _*_ coding: utf-8 _*_
# Copyright (C)  2009 Takakazu Ishikura

# standard modules
import os, sys

# nagara modules
if __name__ == '__main__':
    sys.path.append('../../..')
from core.exception import NagaraException
from utils.setting_helper import ConvertManager

# Exceptions ===================================================================
class AmberSettingConvertException(NagaraException): pass

#-------------------------------------------------------------------------------

class FromNagaraConverter(object):

    option = ConvertManager()

    def __init__(self, settings, task=None):
        self.__settings = settings
        self.__task = task
        self.option.convert_all(self) 
        self.__new_options = self.option.get_converted_options()
        self.__fd = None

    def get_formatted_file(self):
        return self.__fd

    def convert(self):

        fd = StringIO()
        header_content = self.get_header_content()

        obj_name = self.__task.taskobject.name
        if   obj_name == 'Energy':
            # EnergyConverter()
            pass
        elif obj_name == 'Minimize':
            # MinimizeConverter()
            pass
        elif obj_name == 'Dynamics':
            # call DynamicsConverter()
            # call EnsembleConverter()
            # or call EnsembleConverter in DynamicsConverter
            pass




        cntrl_content   = self.get_cntrl_content()
        wt_content_list = self.get_wt_content()
        fd.write(header_content + '\n')
        fd.write(cntrl_content + '\n')
        fd.write('\n'.join(wt_content_list))
        self.__fd = fd

    def get_header_content(self):
        return self.__task.name

    def get_cntrl_content(self):
        return CntrlConverter(self.__settings).get_content()

    def get_wt_content(self):
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

class GroupConverter(object):
    def __init__(self):
        pass


class MinimizeConverter(object):

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


from cStringIO import StringIO
class SettingFormatter(object):

    def __init__(self, settings, section_name):
        self.__settings = settings
        self.__section_name = section_name
        self.__file = StringIO()

    def format(self):
        option_lines = []
        count = 0
        for k, v in self.__settings.items():
            if count == 0:
                line = '    {0:10} = {1:10}, '.format(k, v)
                count += 1

            elif count == 1:
                kv = '{0:10} = {1:10}, '.format(k, v)
                line += kv
                count += 1

            elif count == 2:
                kv = '{0:10} = {1:10}, '.format(k, v)
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
        return template.format('&'+self.__section_name, '\n'.join(option_lines))

    def get_content(self):
        return self.format()

class FilterParser(self):
    pass

#-------------------------------------------------------------------------------


def main():
    settings = dict(
        method = 'dynamics',
        dt = 0.002,
        time_limit = 10,
        temp_ctrl = {'langevin': [5]},
    )

    #a = AmberSetting(settings)
    #for key, val in a.convert().items():
    #    print '{0} = {1}'.format(key, val)
    # print a.get_input_content()


if __name__ == '__main__':
    main()


