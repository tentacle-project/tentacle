# coding: utf-8


from logging import info
import logging; logging.basicConfig(level=logging.DEBUG)

from json import dumps
from multiprocessing import Process
from tentacle.sensor import discover
from tentacle.client import publish


sensors = discover()
payload = {}

for sensor in sensors:
    payload = {**payload, **sensor.get_dict()}

    #TODO Decide if background daemons are better: daemon=True
    process = Process(target=sensor.measuring_loop, name=sensor.sensor_id)
    process.start()
    info(f"Started background process {process.pid}: {process.name} for {sensor.sensor_id}")

publish('tentacle/status', payload=dumps(payload))
