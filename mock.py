# coding: utf-8


def mock_oserror(*args, **kwargs):
    ''' mock helper to raise an OSError '''
    raise OSError


def mock_filenotfounderror(*args, **kwargs):
    ''' mock helper to raise a FileNotFoundError '''
    raise FileNotFoundError


def mock_none(*args, **kwargs):
    ''' mock helper to return none '''
    return None
