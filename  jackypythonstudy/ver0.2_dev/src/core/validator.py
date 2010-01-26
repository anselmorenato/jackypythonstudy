#  -*- encoding: utf-8 -*-
import os, sys



class SettingValidator(object):

    def __init__(self, vdata):
        self.vdata = vdata

    def checkValid(self, params):
        errors = self.__recursiveCheckValid(vdata=self.vdata, params=params)
        return errors

    def __recursiveCheckValid(self, vdata, params):
        errors = {}
        methods = dict(
            range     = self.__range,
            position  = self.__position,
            single    = self.__single,
            multiple  = self.__multiple,
            molre     = self.__molre,
            strre     = self.__strre,
            argstring = self.__argstring,
        )

        for (key, value) in params.items():
            method = vdata[key]['method']
            cond = vdata[key]['cond']
            message = "parameter error at key[%s] : " % key

            if methods.get(method):
                error = methods[method](cond, value)
                if error: errors[key] = message + error

            if method == 'list':
                error = self.__list(cond, value)
                if error:
                    errors[key] = message + error
                else:
                    for param in params[key]:
                        error = self.__recursiveCheckValid(vdata[key], params)
            elif method == 'group':
                error = self.__group(cond, value)
                if error:
                    errors[key] = message + error
                else:
                    error = self.__recursiveCheckValid(vdata[key], params[key])
                    if error: errors[key] = message + error
            else:
                error = ("value type error at key[%s], "
                         "but given type %s is invalid !" % (key, method))

    def __single(self, cond, value):
        if value in cond:
            error = ""
        else:
            error = ("valid value is a single %s,"
                     "but given value is %s."
                     % (str(cond), value) )
        return error

    def __multiple(self, cond, value):
        # cond = self.vdata[key]['cond']
        # sep = ','
        # error = ""
        # values = [v.strip() for v in value.split(sep)]
        error = ""
        for v in value:
            if v not in cond:
                error = ("valid value is a multiple %s,"
                         "but given value is %s"
                         % str(cond), value)
                break
        return error

    def __range(self, cond, value):
        if len(value) == 2 and isinstance(value, tuple):
            (min, max) = value

            if min <= value <= max:
                error = ""
            else:
                error = ("valid value is range %s <= value <= %s,"
                         "but given value is + %s."
                         % (str(min), str(max), str(value)))
        else:
            error = ("valid value is range : (min, max),"
                     "but given value is + %s." % str(value))

        return error
        
    def __position(self, cond, value):
        # expr = "pos = " + value
        # exec(expr)
        if len(value) == 3 and isinstance(value, tuple):
            error = ""
        else:
            error = ("valid value is position (value, value, value),"
                     "but given value is + %s."
                     % str(value))
        return error

    def __molre(self, cond, value): pass

    def __strre(self, cond, value): pass

    def __argstring(self, cond, value) : pass

    def __string(self,value):
        message = ''
        if isinstance(value, str):
            message = ('valid type of the value is <String>, '
                       'but given type is +%s.'
                       % str(value))
        return message

    def __list(self, cond, value):
        if isinstance(value, list):
            error = ""
        else:
            error = ("valid value is list []"
                     "but given value is + %s." % str(value))
        return error

    def __group(self, cond, value):
        if isinstance(value, dict):
            error = ""
        else:
            error = ("valid value is group"
                     "but given value is + %s." % str(value))
        return error

       # self.vdata[key][]
       # (min, max) = self.vdata[key]['cond']

#   def _isValidMethod(self, method):
#       methods = ('range', 'position', 'single', 'multiple', 'list', 
#                  'group', 'molre', 'strre', 'argstring')
#       return(method in methods)
#       
#       
#   def _runValidMethod(self, method, cond, value):
#       expr = 'result = self._' + method + '(cond, value)'
#       exec(expr)
#       return result

    def getData(self):
        return self.vdata

class ParamConverter: pass

import yaml
class Settiing(object):

    def __init__(self, yaml):
        self.__setting = yaml.load(yaml)

class StandardSettiingValidator(object):

    def __init__(self, setting):
        self.__setting = setting

    def is_valid(self):
        return True





if __name__ == '__main__':
    import yaml

    
    valid_yaml_data = """
integrator:
    {default: verlet, type: string, method: single
    cond: [verlet, velocity, gear]

restraint:
    type: bool
    default: false
    method: multiple
    cond: [off, shake, angle, bond, dihedral]
    child:
time_step:
    default: 5
    type: int
    method: range
    cond: [0, 100]
cavity:
    default: false
    type: bool
    method: list
    cond:  None
pb:
    default: pb_group
    type: group
implicit:
    implicit:
        default: 5, type: int, method: single

group:
    - restraint
    - constraint
    - potential
    - 
restraint:
    all:
        free
    group0:
        freeze
    group1:
        shake
    group2:
        positional
restraint_method:
    harmonic
    shake
    water_cap


potential:
    all: 
        

group:
    type:
        - atom
        - bond
        - angle
        - torsion
        - pair
        - grouped(as fragmen)
        - fragment(with fmo)
    method:
        - restraint:
            - atom, bond, angle, torsion, pair, grouped
        - property divide
        - fragment MO
        - potential(QM/MM)
        - 




restraint:
    restraint: {default: false, type: bool}
    true:
        restraint_group: {default: string, } 


ensemble:
    ensemble: {default:[temp, press], type: [string], cond: [temp, press, ener]}
    temp:
        temp: {default: langevin, type: string, cond: [weak, lang, andersen]}
        langevin:
            gamma: {default: 2.0, type: float}
        weak:
            weak_par: {default: 2.0, type: float}
    press:
        press: {default: langevin}

implicit:
    implicit: {default: false, type: bool, cond: none}
    true:



    ensemble(key):
        - templeture(value, key):
            langevin(value, key):
                gamma(key): 2(value)

        - pressure(value, key):
            hoover(value, key):
                par(key): 5(value)

    """

    # valid_data = validyaml.load(valid_yaml_data)

    user_yaml_data = """
integrator: velocity_verle
time_step: 10
restraint: [group1, group2]
restraint_setting:
    group1:
    group2:

    
constraint: [shake, algle]
cavity:
    - size: 25, position: [3.0, 3.0, 3.0]
    - size: 15, position: [5.0, 5.0, 5.2]
    - size:  5, position: [-3.2,0.0, 9.3]
gb:
    method: HTCII
    salt: 0.0

ensemble:
    - temp, press
    templeture:
    - [tempreture, pressure]
    - tempreture:
        - tempreture: 

    pressure:
    volume:



    """

    # def ensemble(templeture, pressure): pass

    # def temp(weak | langevin | anderson): pass

    # def langevin(gamma): pass

    # def pressure(parr, hoover): pass

#    # this format is ok.
#    ensemble(key):
#        templeture(value, key):
#            langevin(value, key):
#                gamma(key): 2(value)
#
#        pressure(value, key):
#            hoover(value, key):
#                par(key): 5(value)
#
#    ensemble: [*langevin, *pressure]
#    &langevin langevin:
#        gamma: 2
#
#
#    # this format is ok.
#    ensemble(key):
#        # select scheme
#        ensemble(key): [templeture, pressure](value)
#        tempreture(key):
#            tempreture(key): langiven(value)
#            langevin(key):
#                gamma(key): 2(value)
#        pressure(key):
#            pressures(key): hoover(value)
#            hoover(value):
#                par(key): 5(value)
#
#    ensemble(key):
#        # select scheme
#        - ensemble(key): [templeture, pressure](value)
#        - tempreture(key):
#            - tempreture(key): langiven(value)
#            - langevin(key):
#                  gamma(key): 2(value)
#            - weak(key):
#                par_weak(key): 5(value)
#          pressure(key):
#            - pressures(key): hoover(value)
#              hoover(value):
#                  par(key): 5(value)
#
#    setting = dict(
#        ensemble = ['templeture', 'pressure'],
#        templeture_method = 'langevin',
#    )
#
#    # this format is ok.
#    ensemble:
#        value:
#        child:
#        ensemble(key): [templeture, pressure](value)
#        tempreture(key):
#            tempreture(key): langiven(value)
#            langevin(key):
#                gamma(key): 2(value)
#        pressure(key):
#            pressures(key): hoover(value)
#            hoover(value):
#                par(key): 5(value)
#
#    setting = dict(
#        ensemble = dict(
#            attribute = ['templeture', 'pressure']
#            templeture = dict(
#                templeture = 'langaevin',
#                langevin = {'gamma': 5}
#                weak = {'constant': 2}
#
#            )
#
#        )
#    )
#
#    ensemble.attribute => [temp, press]
#    ensemble.temp => langevin
#    ensemble.press => parinnelo
#    ensemble.langevin = 2
#    ensemble.weak = 2
#    ensemble.parrinello => 5
#
#    ensemble.name
#    ensemble.attribute = [temp, press]
#    ensemble.templeture = langevin
#    ensemble.tempreture.langevin.
#
#    ensemble(key):
#        # select scheme
#        - ensemble(key): [templeture, pressure](value)
#        - tempreture(key):
#            - tempreture(key): langiven(value)
#            - langevin(key):
#                gamma(key): 2(value)
#        - pressure(key):
#            - pressures(key): hoover(value)
#            - hoover(value):
#                par(key): 5(value)
#
#
#    user_data = yaml.load(user_yaml_data)
#
#    vdata = SettingValidator(valid_data)
#    #print vdata.checkValid(test_data)
#
#    if not d.checkValid(test_data):
#        print "aaaa"
#
#"""
