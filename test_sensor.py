# coding: utf-8


import pytest
import paho.mqtt.publish as mqtt_publish
from tentacle.sensor import Sensor
from tentacle.client import MQTTClient
from tentacle.unit import Temperature, Relative_Humidity, Pressure
from tentacle.capability import Capability
from tentacle.measurement import Measurement


class Test_Sensor(Sensor):
    ''' tentacle.sensor test object '''

    def __init__(self):
        super().__init__('test_sensor_id',
                         'test_sensor_name',
                         Capability(Temperature(), [-40, 85]),
                         Capability(Relative_Humidity(), [0, 100]),
                         Capability(Pressure(unit='hPa'), [300, 1100]))


    def read_data(self):
        pass


def test_Sensor__init__return_sensor_object(mocker):
    ''' test if Sensor().__init__() creates a valid Sensor object '''

    mocker.patch.object(mqtt_publish, 'single')
    sensor = Test_Sensor()
    assert sensor.sensor_id == 'test_sensor_id'
    assert sensor.name == 'test_sensor_name'
    assert sensor.interval == 1
    assert sensor.capabilities == {
        'pressure': {
            'range_max': 1100,
            'range_min': 300,
            'unit': 'hPa'
        },
        'relative_humidity': {
            'range_max': 100,
            'range_min': 0,
            'unit': '%RH'
        },
        'temperature': {
            'range_max': 85,
            'range_min': -40,
            'unit': '°C'
        }
    }
    ['temperature', 'relative_humidity', 'pressure']
    assert sensor.temperature.name == 'temperature'
    assert sensor.temperature.unit == '°C'
    assert sensor.temperature.range_min == -40
    assert sensor.temperature.range_max == 85
    assert sensor.relative_humidity.unit == '%RH'
    assert sensor.relative_humidity.range_min == 0
    assert sensor.relative_humidity.range_max == 100
    assert sensor.pressure.unit == 'hPa'
    assert sensor.pressure.range_min == 300
    assert sensor.pressure.range_max == 1100
    assert isinstance(sensor.mqtt_client, MQTTClient)


def test_Sensor_read_data_abstractmethod():
    ''' test if Sensor().read_data() is an abstract method '''

    class Test_Sensor(Sensor):
        ''' tentacle.sensor test object without abstract methods '''
        def __init__(self):
            super().__init__('test_sensor_id',
                             'test_sensor_name')

    with pytest.raises(TypeError):
        Test_Sensor()


def test_Sensor_measuring_loop_no_measurement(monkeypatch, mocker):
    ''' test if Sensor.measuring_loop() does nothing if there are no
        measurements from Sensor.read_data() '''

    mocker.patch.object(mqtt_publish, 'single')
    sensor                  = Test_Sensor()
    monkeypatch.setattr(sensor, 'testing', True) # needed to break while loop
    spy_publish_measurement = mocker.spy(sensor.mqtt_client, 'publish_measurement')
    spy_read_data           = mocker.spy(sensor, 'read_data')

    sensor.measuring_loop()

    spy_read_data.assert_called_once()
    not spy_publish_measurement.assert_not_called()


def test_Sensor_measuring_loop(monkeypatch, mocker):
    ''' test if Sensor.measuring_loop() fulfills one while loop correctly '''

    def mock_read_data():
        measurement = Measurement([
             [Temperature(), 10.8],
             [Relative_Humidity(), 86],
             [Pressure(unit='hPa'), 1034.28]
        ])
        measurement.timestamp = 1604842762
        return measurement

    mocker.patch.object(mqtt_publish, 'single')
    sensor                  = Test_Sensor()
    monkeypatch.setattr(sensor, 'testing', True) # needed to break while loop
    monkeypatch.setattr(sensor, 'read_data', mock_read_data)
    spy_publish_measurement = mocker.spy(sensor.mqtt_client, 'publish_measurement')
    spy_read_data           = mocker.spy(sensor, 'read_data')

    sensor.measuring_loop()

    spy_read_data.assert_called_once()
    spy_publish_measurement.assert_any_call(
        'temperature',
        '{"timestamp":1604842762,"unit":"\\u00b0C","value":10.8}')
    spy_publish_measurement.assert_any_call(
        'relative_humidity',
        '{"timestamp":1604842762,"unit":"%RH","value":86}')
    spy_publish_measurement.assert_any_call(
        'pressure',
        '{"timestamp":1604842762,"unit":"hPa","value":1034.28}')
