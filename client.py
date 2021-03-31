# coding: utf-8


from configparser import ConfigParser
from json import dumps
from pathlib import Path
from logging import debug, critical
import paho.mqtt.publish


config = ConfigParser()
config.read(f'{Path.home()}/.config/tentacle/satellite.conf')
server = config['server']

HOSTNAME = server.get('hostname', 'localhost')
PORT     = int(server.get('port', 1883))


def publish(topic, payload, qos=2, retain=True, will=None):
    ''' wrapper for the paho.mqtt.publish.single method with convenient defaults '''

    try:
        paho.mqtt.publish.single(topic,
                                 payload=payload,
                                 qos=qos,
                                 retain=retain,
                                 will=will,
                                 hostname=HOSTNAME,
                                 port=PORT)
        debug(f'published on "{topic}": {payload}, qos={qos}, retain={retain}, will={will}')
    except ConnectionRefusedError:
        critical(f'Cannot connect to mqtt.')


class MQTTClient:
    ''' mqtt-smarthome compliant sensor client
    mqtt-smarthome: https://github.com/mqtt-smarthome '''

    def __init__(self, sensor_id, capabilities, interval):
        self.sensor_id    = sensor_id
        self.capabilities = capabilities
        self.interval     = interval
        self.publish_interval()
        self.publish_capabilities()
        self.publish_connected()


    def publish_interval(self):
        ''' publish the measurement interval in seconds '''

        publish(f'tentacle/status/{self.sensor_id}/interval',
                payload=str(self.interval))


    def publish_capabilities(self):
        ''' publish the capabilities, i.e. temperature;pressure;humidity '''

        publish(f"tentacle/status/{self.sensor_id}/capabilities",
                payload=dumps(self.capabilities))


    def publish_connected(self):
        ''' publish connected status: 2 = connected, 0 = disconnected '''

        topic = f'tentacle/connected/{self.sensor_id}'
        publish(topic,
                payload='2',
                will={'topic': topic,
                      'payload': '0',
                      'qos': 2,
                      'retain': True})


    def publish_measurement(self, capability, payload):
        ''' publish a mesaurement with payload value=24.5;unit=°C '''

        publish(f'tentacle/status/{self.sensor_id}/measurement/{capability}', payload=payload)
