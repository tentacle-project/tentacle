# coding: utf-8


from abc import ABC, abstractmethod
from glob import glob
from importlib import import_module
from json import dumps
from logging import info
from os.path import dirname, basename
from time import sleep

import paho.mqtt.client as mqtt

from tentacle.client import MQTTClient


def discover():
    ''' import sensor modules from sensors submodule and run a discovery for each '''

    info('Discovering sensors')
    sensors = []
    for sensor_file in glob(dirname(__file__) + '/sensors/sensor_*.py'): # get all sensor_*.py modules in sensors subfolder

        sensor_module = basename(sensor_file)[:-3]
        new_sensor = import_module('tentacle.sensors.' + sensor_module).discover()

        if new_sensor:
            sensors.append(new_sensor)
            info(f"Found {new_sensor.name} with id {new_sensor.sensor_id}")

    return None if not sensors else sensors


class Sensor(ABC):
    ''' Abstract sensor class to implement a measuring loop for each sensor class '''

    def __init__(self, sensor_id, name, *capabilities):
        self.testing       = False
        self.sensor_id     = sensor_id
        self.name          = name
        self.interval      = 1
        self.capabilities  = {}
        for capability in capabilities:
            self.capabilities = {**self.capabilities, **capability.get_dict()}
            setattr(self, capability.name, capability)
        self.mqtt_client   = MQTTClient(sensor_id, self.capabilities, self.interval)


    def get_dict(self):
        ''' return a mqtt payload of all attributes '''

        return {
            'sensors': {
                self.sensor_id: {
                    'name': self.name,
                    'capabilities': self.capabilities
                 }
             }
        }


    @abstractmethod
    def read_data(self):
        ''' Abstract method: Read all sensor measurings and return them.

            >>> sensor_bme280.read_data()
            Measurement([
                [Temperature(), 10.8],
                [Relative_Humidity(), 67],
                [Pressure(), 1024.23]
            ])
            '''
        pass




    def measuring_loop(self):
        ''' Read sensor measuring once every self.interval and publish an update
            if there is a change  '''
        print(self)

        while True:
            measurement = self.read_data()

            if measurement:
                info(f'Publishing data')
                for capability, payload in measurement.to_mqtt().items():
                    self.mqtt_client.publish_measurement(capability, payload)

            if self.testing:
                break

            sleep(self.interval)


# examples
if __name__ == '__main__':

    from tentacle.capability import Capability
    from tentacle.unit import Temperature, Relative_Humidity, Pressure

    sensor = Sensor('sensor_id', 'bme280',
        Capability(Temperature(), [-40, 85]),
        Capability(Relative_Humidity(), [0, 100]),
        Capability(Pressure(unit='hPa'), [300, 1100]))
    print(sensor.capabilities)
