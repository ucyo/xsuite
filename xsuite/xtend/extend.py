#!/usr/bin/env python
# coding=utf-8
"""Extensions for Xarray for analysing weather data."""

import functools
import importlib as ilib
import os
import sys
import xarray as xr


_DA_ENV = 'XSUITE_DA_METHODS'
_DS_ENV = 'XSUITE_DS_METHODS'


@xr.register_dataarray_accessor('xtend')
class _NyxDA(object):
    def __init__(self, data):
        self._data = data

    def add_methods(self, folder):
        return _add_folder(folder, mode='da')

    def load_env(self):
        return _load_from_env(mode='da')


@xr.register_dataset_accessor('xtend')
class _NyxDS(object):
    def __init__(self, data):
        self._data = data

    def add_methods(self, folder):
        return _add_folder(folder, mode='ds')

    def load_env(self):
        return _load_from_env(mode='ds')


def _patch(func, funcname, mode):
    classobject = _NyxDA if mode == 'da' else _NyxDS

    @functools.wraps(func)
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
        folder = os.environ.get(env, False)
    if not folder:
        return False
    assert os.path.isdir(folder), '"{}" is not a folder'.format(folder)
    folder = os.path.realpath(folder)

    pythonfiles = [x[:-3] for x in os.listdir(folder)
                   if x.endswith('.py') and x[0] != '_']
    if not pythonfiles:
        return False
    sys.path.insert(0, folder)
    for method in pythonfiles:
        try:
            lib = ilib.import_module(method, package='xtend')
            _patch(getattr(lib, 'main'), method, mode)
        except SystemError as err:
            print('ERR importing {}: {}'.format(method, str(err)))
        except AttributeError as err:
            msg = 'Method "{}/{}.py" has no "main" function'.format(
                folder, method)
            raise AttributeError(msg)
    return True


def _load_from_env(mode=None):
    if mode is None:
        _ = [_load_from_env(x) for x in ['da', 'ds']]
        return None
    ENVVAR = _DA_ENV if mode == 'da' else _DS_ENV
    env = os.environ.get(ENVVAR, False)
    if not env:
        return None
    folders = env.split(':')
    for folder in folders:
        _add_folder(folder, mode)
