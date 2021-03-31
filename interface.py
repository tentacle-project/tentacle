# coding: utf-8


from logging import info, critical

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish


class Interface:
    ''' sensor mqtt interface '''

    def __init__(self, hostname, port, sensor):
        self.hostname = hostname self.port = port
        self.sensor = sensor
        self.sid = self.sensor.sensor_id
        self.client = mqtt.Client()
        self.connect()
        self.subscribe_set_interval()


    def connect(self):
        try:
            self.client.connect(self.hostname, self.port)
        except ConnectionRefusedError:
            critical(f"The mqtt-broker '{MQTT_HOSTNAME}' cannot be reached.\
    Is mosquitto.service running?")
            exit(1)


    def subscribe_set_interval(self):
        self.client.message_callback_add(f"tentacle/set/interval/{self.sid}",
                                         self.set_interval())


    def set_interval(self, client, userdata, message):
        if message:
            try:
                interval = int(message)
            except ValueError, TypeError:
                info(f"{message} is not a valid interval (integer seconds)")
                return
            self.sensor.set_interval(interval)




## Subscribe
#  tentacle/set/<sid>/interval          10                           False
# +tentacle/get/<sid>/temperature                                    False
# +tentacle/get/<sid>/interval                                       False
# +tentacle/get/<sid>/capabilities
# [tentacle/command/<sid>]
