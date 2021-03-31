# coding: utf-8


from logging import error, info

import smbus2
import bme280

from tentacle.measurement import Measurement
from tentacle.unit import Temperature, Relative_Humidity, Pressure
from tentacle.capability import Capability
from tentacle.sensor import Sensor

import warnings


def discover(port=1, address=0x76):
    ''' Discover sensors
        @param port         i2c bus port, default 1
        @param address      i2c bus address, default 0x76

        @return sensor '''

    sensors = {}
    sensor_id = f"BME280_{port}_{address}"

    try:
        bus = smbus2.SMBus(port)
    except FileNotFoundError:
        info('Cannot communicate with I2C bus.')
        raise
        #TODO make this work, wether raise or return
        return None

    try:
        sensor = BME280(sensor_id, bus, address)
    except OSError:
        info(f"Could not connect to '{sensor_id}'.")
        #TODO make this work, wether raise or return
        raise
        return None

    return sensor


class BME280(Sensor):
    ''' bme280 to tentacle adapter '''

    def __init__(self, sensor_id, bus, address):
        super().__init__(sensor_id, 'bme280',
                         Capability(Temperature(), [-40, 85]),
                         Capability(Relative_Humidity(), [0, 100]),
                         Capability(Pressure(unit='hPa'), [300, 1100]))
        self.bus = bus
        self.address = address
        self.calibration_params = bme280.load_calibration_params(bus, address)


    def read_data(self):
        ''' read and return temperature, pressure and humidity from sensor '''
        try:
            data = bme280.sample(self.bus, self.address, self.calibration_params)
        except OSError:
            error(f"Cannot read from '{self.sensor_id}'")
            raise

        try:
            temperature = float(data.temperature)
            pressure = float(data.pressure)
            relative_humidity = float(data.humidity)
        except TypeError or ValueError:
            error(f"Invalid measurement '{self.sensor_id}': temperature: {data.temperature}, pressure: {data.pressure}, humidity: {data.humidity}")
            raise

        return Measurement([
            [Temperature(), temperature],
            [Relative_Humidity(), relative_humidity],
            [Pressure(), pressure]
        ])
