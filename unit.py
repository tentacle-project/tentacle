# coding: utf-8


from calendar import timegm
from datetime import datetime


class Measurement:
    ''' measurement object to hold one or more units a value and a timestamp '''


    def __init__(self, unit, value):
        self.timestamp    = timegm(datetime.utcnow().utctimetuple())
        self.unit         = unit
        self.value        = value


class Unit:
    def __init__(self, name, unit):
        self.name = name
        self.unit = unit


class Temperature(Unit):
    def __init__(self, unit='°C'):
        super().__init__('temperature', unit)


class Pressure(Unit):
    def __init__(self, unit='hPa'):
        super().__init__('pressure', unit)


class Relative_Humidity(Unit):
    def __init__(self, unit='%RH'):
        super().__init__('relative_humidity', unit)


SI_UNITS = {
    'temperature':       Temperature(),
    'relative_humidity': Relative_Humidity(),
    'pressure':          Pressure()
}
