# coding: utf-8


import pytest
import paho.mqtt.client as mqtt
import paho.mqtt.publish as mqtt_publish
from configparser import ConfigParser
from json import dumps
from pathlib import Path
from tentacle.client import MQTTClient, publish, HOSTNAME, PORT
from tentacle import client


config = ConfigParser()
config.read(f'{Path.home()}/.config/tentacle/satellite.conf')
server = config['server']

TEST = {
    'sensor_id': 'test_sensor_id',
    'capability': {
        'temperature': {
            'unit': '°C',
            'range_min': -15,
            'range_max': 115
    } },
    'interval': 10,
    'topic': 'test/topic',
    'payload': 'test_payload',
    'qos': 2,
    'retain': True,
    'will': {
        'topic': 'tentacle/connected/test_sensor_id',
        'payload': '0',
        'qos': 2,
        'retain': True
    },
    'hostname': server.get('hostname', 'localhost'),
    'port': int(server.get('port', 1883))
}


def test_publish(mocker):
    ''' Test if publish calls paho.mqtt.publish.single with correct arguments '''

    mock_publish = mocker.patch.object(mqtt_publish, 'single')
    publish(TEST['topic'], TEST['payload'], TEST['qos'], TEST['retain'],
            TEST['will'])

    mock_publish.assert_called_once_with(TEST['topic'], payload=TEST['payload'],
                                         qos=TEST['qos'], retain=TEST['retain'],
                                         will=TEST['will'],
                                         hostname=TEST['hostname'],
                                         port=TEST['port'])


def test_MQTTClient__init__(mocker):
    ''' Test if MQTTClient.__init__ instanciates a proper object '''

    mocker.patch.object(mqtt_publish, 'single')
    mock_publish_interval = mocker.patch.object(MQTTClient, 'publish_interval')
    mock_publish_capabilities = mocker.patch.object(MQTTClient, 'publish_capabilities')
    mock_publish_connected = mocker.patch.object(MQTTClient, 'publish_connected')
    mqtt_client = MQTTClient(TEST['sensor_id'], TEST['capability'], TEST['interval'])

    assert mqtt_client.sensor_id == TEST['sensor_id']
    assert mqtt_client.capabilities == TEST['capability']
    assert mqtt_client.interval == TEST['interval']
    mock_publish_interval.assert_called_once()
    mock_publish_capabilities.assert_called_once()
    mock_publish_connected.assert_called_once()


def test_MQTTClient_publish_interval(mocker):
    ''' Test if MQTTClient.publish_interval calls publish with
        correct arguments '''

    mocker.patch.object(mqtt_publish, 'single')
    mqtt_client = MQTTClient(TEST['sensor_id'], TEST['capability'], TEST['interval'])
    mock_publish   = mocker.patch.object(client, 'publish')
    mqtt_client.publish_interval()

    mock_publish.assert_called_once_with(
        'tentacle/status/test_sensor_id/interval',
        payload='10')


def test_MQTTClient_publish_capabilities(mocker):
    ''' Test if MQTTClient.publish_capabilities calls publish with
        correct arguments '''

    mocker.patch.object(mqtt_publish, 'single')
    mqtt_client = MQTTClient(TEST['sensor_id'], TEST['capability'], TEST['interval'])
    mock_publish   = mocker.patch.object(client, 'publish')
    mqtt_client.publish_capabilities()

    mock_publish.assert_called_once_with(
        'tentacle/status/test_sensor_id/capabilities',
        payload=dumps(TEST['capability']))


def test_MQTTClient_publish_connected(mocker):
    ''' Test if MQTTClient.publish_connected calls publish with
        correct arguments '''

    mocker.patch.object(mqtt_publish, 'single')
    mqtt_client = MQTTClient(TEST['sensor_id'], TEST['capability'], TEST['interval'])
    mock_publish   = mocker.patch.object(client, 'publish')
    mqtt_client.publish_connected()

    mock_publish.assert_called_once_with(
        'tentacle/connected/test_sensor_id',
        payload='2',
        will=TEST['will'])


def test_MQTTClient_publish_measurement(mocker):
    ''' Test if MQTTClient.publish_measurement calls publish with
        correct arguments '''

    mocker.patch.object(mqtt_publish, 'single')
    mqtt_client = MQTTClient(TEST['sensor_id'], TEST['capability'], TEST['interval'])
    mock_publish   = mocker.patch.object(client, 'publish')
    mqtt_client.publish_measurement('temperature', 'value=15.4;unit=°C')

    mock_publish.assert_called_once_with(
        f'tentacle/status/test_sensor_id/measurement/temperature',
        payload = 'value=15.4;unit=°C')
