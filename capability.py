# coding: utf-8


from tentacle.unit import Unit


class Capability:
    ''' Capability object to hold a Unit object and a range '''

    def __init__(self, unit, sensor_range):
        if not isinstance(unit, Unit):
            raise TypeError('unit must be of type tentacle.satellite.Unit')
        self.name = unit.name
        self.unit = unit.unit
        # TODO isinstance geht ned
#         if isinstance(sensor_range, type(list())) or len(sensor_range) != 2:
#             raise ValueError('range must be a list with two items')
        self.range_min = sensor_range[0]
        self.range_max = sensor_range[1]


    def get_dict(self):
        ''' return a mqtt payload of all attributes '''

        return {
            self.name: {
                'unit': self.unit,
                'range_min': self.range_min,
                'range_max': self.range_max,
            }
        }


# example
if __name__ == '__main__':
    from tentacle.unit import Temperature, Pressure
    a = Capability(Temperature(), [10,30])
    print(a.get_dict())
