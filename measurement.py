# coding: utf-8


from calendar import timegm
from datetime import datetime
from json import dumps

#TODO im pretty shure in future we will nee some thing different maybe with
# abstract classes or extending classes
class Measurement:
    ''' measurement object to hold one or more units a value and a timestamp '''
    def __init__(self, measurements): # Measurement([unit, value])
        self.timestamp = timegm(datetime.utcnow().utctimetuple())
        self.capabilities = []
        for measurement in measurements:
            unit = measurement[0]
            unit.value = measurement[1]
            setattr(self, unit.name, unit)
            self.capabilities.append(unit.name)


    def __iter__(self):
        ''' return each associated capability '''
        for attritbute in self.capabilities:
            yield getattr(self, attritbute)


    def to_mqtt(self):
        ''' return a mqtt payload of all attributes for each associated capability '''
        capabilities = {}
        for capability in self:
            capabilities[capability.name] = dumps({'timestamp': self.timestamp,
                                                        'unit': capability.unit,
                                                        'value': capability.value},
                                                  separators=(',',':'))
        return capabilities


# Example usage
if __name__ == '__main__':

    from json import loads
    from tentacle.unit import Temperature, Pressure
    measurement = Measurement([[Temperature(), 2], [Pressure(), 133742]])

    for capability_name, payload in measurement.to_mqtt().items():
        print(capability_name, payload)
        print(capability_name, loads(payload))
# 
#     print(measurement.timestamp)
#     for capability in measurement:
#         print(capability.name, capability.unit, capability.value)
