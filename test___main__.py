# coding: utf-8


import pytest
import multiprocessing
from tentacle import sensor


def test___main__(mocker):
    ''' test if tentacle.__main__
        - calls tentacle.sensor.discover once
    '''

    mock_sensor_discover = mocker.patch.object(sensor, 'discover')
    mock_multiprocessing_process = mocker.patch.object(multiprocessing, 'Process')
    import tentacle.__main__      # hack to "simulate" `python -m tentacle`

    mock_sensor_discover.assert_called_once()
