The base convention os the [mqtt-smarthome](https://github.com/mqtt-smarthome/mqtt-smarthome/blob/master/Architecture.md) convention.

```
# Host
to be filled with info


# Satellite
## Subscribe
-----------------------------------------------------------------------------------------------------
 topic/message                                                  Retain Flag      QoS
-----------------------------------------------------------------------------------------------------
 tentacle/set/<sid>/interval                                    False
 10

 tentacle/get/<sid>                                             False
 [capabilities, interval]

 tentacle/get                                                   False
 discover

 tentacle/get/sensors                                           False
 discover

 tentacle/command/<sid>

## Publish
-----------------------------------------------------------------------------------------------------
imp topic/message                                                  Retain Flag      QoS
-----------------------------------------------------------------------------------------------------
    tentacle/status
    json-string {
       'sensors': {
           'BME280_1_118': {
               'name': 'BME280',
               'interval': 1,
               'capabilities': {
                   'temperature': {
                       'unit': '°C',
                       'range_min: -120,
                       'range_max: 10
                   },
                   [ capability_2: ... ]
               }
           },
           [ sensor_id_2: ... ]
       },
    }

    tentacle/status/<sid>/interval
    5                                                              True

    tentacle/status/<sid>/capabilities                  True
    json-string {
       'capabilities': {
           'temperature': {
               'unit': '°C',
               'range_min: -120,
               'range_max: 10
           },
           [ capability_2: ... ]
       }
    }

    tentacle/connected/<sid>
    0, 1 or 2, see link on top                          False & Last Will and Testament

    tentacle/status/<sid>/measurement/temperature       Trie if measurement is
    a state, False if measurement is a one-shot-event
    json-string {
       'timestamp': 14203598325058,
       'unit': '°C'',
       'value': 10.4
    }
```
