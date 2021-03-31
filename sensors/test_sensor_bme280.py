# coding: utf-8


import pytest
import smbus2
import bme280
import paho.mqtt.publish as mqtt_publish
from tentacle.sensors import sensor_bme280
from tentacle.mock import mock_oserror, mock_filenotfounderror, mock_none


class Mock_Data:
    ''' mock object of the return value of bme280.sample '''
    def __init__(self, temperature, relative_humidity, pressure):
        self.temperature = temperature
        self.humidity = relative_humidity
        self.pressure = pressure
        print(self.temperature)

    def __call__(self, *args, **kwargs):
        return self


class Mock_bme280:
    ''' mock object of bme280 module '''
    def __init__(self):
        self.mock_data = Mock_Data()

    def load_calibration_params(self, *args, **kwargs):
        return None

    def sample(self, *args, **kwargs):
        return self.mock_data


def mock_return_data(temperature, pressure, humidity):
    ''' wrapper to instanciate new Mock_Data object '''
    return Mock_Data(temperature, pressure, humidity)


@pytest.fixture
def test_bme280(monkeypatch, mocker):
    ''' return a fresh tentacle.satellite.sensors.bme280 object '''

    mocker.patch.object(mqtt_publish, 'single')
    return sensor_bme280.BME280('BME280_1_0x76', 1, 0x76)


@pytest.fixture
def mock_bme280(monkeypatch, mocker):
    ''' mock of sensor_bme280.BME280 '''

    mocker.patch.object(mqtt_publish, 'single')
    monkeypatch.setattr(bme280, 'load_calibration_params', mock_none)
    monkeypatch.setattr(bme280, 'sample', mock_oserror)

    return {
        'mock': sensor_bme280.BME280('BME280_1_0x76', 1, 0x76),
        'monkeypatch': monkeypatch
    }


def test_discover_no_i2c_connection(monkeypatch):
    ''' test if discover() raises a FileNotFoundError if i2c bus is not reachable '''

    monkeypatch.setattr(smbus2, 'SMBus', mock_filenotfounderror)
    with pytest.raises(FileNotFoundError):
        assert sensor_bme280.discover() == None


def test_discover_no_sensor_connection(monkeypatch):
    ''' test if discover() raises an OSError if sensor is not reachable '''

    monkeypatch.setattr(bme280, 'load_calibration_params', mock_oserror)
    with pytest.raises(OSError):
        assert sensor_bme280.discover() == None


def test_discover_return_sensor(mock_bme280):
    ''' test if discover() returns a sensor object '''

    mock_bme280['monkeypatch'].setattr(bme280, 'load_calibration_params', mock_none)
    mock_bme280['monkeypatch'].setattr(bme280, 'sample', mock_return_data(10, 22, 33))
    result = sensor_bme280.discover()
    assert result.temperature.unit == '°C'
    assert result.temperature.range_min == -40
    assert result.temperature.range_max == 85
    assert result.relative_humidity.unit == '%RH'
    assert result.relative_humidity.range_min == 0
    assert result.relative_humidity.range_max == 100
    assert result.pressure.unit == 'hPa'
    assert result.pressure.range_min == 300
    assert result.pressure.range_max == 1100


def test_BME280_read_data_no_sensor_connection(mock_bme280):
    ''' test if read_data() raises an OSError if sensor is not reachable '''

    mock_bme280['monkeypatch'].setattr(bme280, 'load_calibration_params', mock_none)
    mock_bme280['monkeypatch'].setattr(bme280, 'sample', mock_oserror)
    with pytest.raises(OSError):
        assert mock_bme280['mock'].read_data()


def test_BME280_read_data_type_and_value_error(mock_bme280):
    ''' test if read_data() raises a TypeError if measurements have invalid format '''
    mock_bme280['monkeypatch'].setattr(bme280, 'load_calibration_params', mock_none)
    mock_bme280['monkeypatch'].setattr(bme280, 'sample', mock_return_data('string', 0, 0))
    with pytest.raises(ValueError):
        mock_bme280['mock'].read_data()

    mock_bme280['monkeypatch'].setattr(bme280, 'sample', mock_return_data({}, 0, 0))
    with pytest.raises(TypeError):
        mock_bme280['mock'].read_data()

    mock_bme280['monkeypatch'].setattr(bme280, 'sample', mock_return_data([], 0, 0))
    with pytest.raises(TypeError):
        mock_bme280['mock'].read_data()


def test_read_data_return_sensor_object(mock_bme280):
    ''' test if read_data() returns a Measurements object '''
    mock_bme280['monkeypatch'].setattr(bme280, 'load_calibration_params', mock_none)
    mock_bme280['monkeypatch'].setattr(bme280, 'sample', mock_return_data(10.23, .14, '10.8'))

    result = mock_bme280['mock'].read_data()
    assert result.temperature.value == 10.23
    assert result.temperature.unit == '°C'
    assert result.relative_humidity.value == 0.14
    assert result.relative_humidity.unit == '%RH'
    assert result.pressure.value == 10.8
    assert result.pressure.unit == 'hPa'
