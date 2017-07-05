"""Extensions for Xarray for analysing weather data."""

import functools as _functools
import xarray as _xr
import importlib as _ilib
import os as _os
import sys as _sys


@_xr.register_dataarray_accessor('xtend')
class _NyxDA(object):
    def __init__(self, data):
        self._data = data

    def add_methods(self, folder):
        return _add_folder(folder, mode='da')


@_xr.register_dataset_accessor('xtend')
class _NyxDS(object):
    def __init__(self, data):
        self._data = data

    def add_methods(self, folder):
        return _add_folder(folder, mode='ds')


def _patch(func, funcname, mode):
    classobject = _NyxDA if mode == 'da' else _NyxDS

    @_functools.wraps(func)
    def method(accessor, *args, **kwargs):
        return func(accessor._data, *args, **kwargs)
    setattr(classobject, funcname, method)
    return func


def xtend_dataarray(da_folder=None):
    return _add_folder(da_folder, 'da')


def xtend_dataset(ds_folder=None):
    return _add_folder(ds_folder, 'ds')


def _add_folder(folder, mode=None):
    if not isinstance(mode, str) or mode.lower() not in ['ds', 'da']:
        raise ValueError('Can not understand mode {}'.format(mode))
    mode = mode.lower()
    env = 'XTEND_DS' if mode == 'ds' else 'XTEND_DA'

    if not folder:
        folder = _os.environ.get(env, False)
    if not folder:
        return False
    assert _os.path.isdir(folder), '"{}" is not a folder'.format(folder)
    folder = _os.path.realpath(folder)

    pythonfiles = [x[:-3] for x in _os.listdir(folder)
                   if x.endswith('.py') and x[0] != '_']
    if not pythonfiles:
        return False
    _sys.path.insert(0, folder)
    for method in pythonfiles:
        try:
            lib = _ilib.import_module(method, package='xtend')
            _patch(getattr(lib, 'main'), method, mode)
        except SystemError as err:
            print('ERR importing {}: {}'.format(method, str(err)))
        except AttributeError as err:
            msg = 'Method "{}/{}.py" has no "main" function'.format(
                folder, method)
            raise AttributeError(msg)
    return True
