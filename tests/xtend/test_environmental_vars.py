#!/usr/bin/env python
# coding=utf-8
"""Test environmental variables for extension of xarray."""

import os
import pkg_resources
from xsuite.tools import load_data
import xsuite

DA_ENV = 'XSUITE_DA_METHODS'
DS_ENV = 'XSUITE_DS_METHODS'
DIR = os.path.dirname(os.path.abspath(__file__))
DA_ENV_ENTRY = "{}:{}".format(os.path.join(DIR, 'da_methods'),
                              os.path.join(DIR, 'da_methods_other'))
DS_ENV_ENTRY = os.path.join(DIR, 'ds_methods')

def setup_env():
    for var in [DA_ENV, DS_ENV]:
        os.environ[var] = DA_ENV_ENTRY if 'DA' in var else DS_ENV_ENTRY
setup_env()


DS = load_data('pre', decode_times=False)


def test_load_from_env():
    from xsuite import xtend
    assert hasattr(DS.tas.xtend, 'anomalies')
    assert hasattr(DS.xtend, 'anomalies')


def test_load_from_env_and_folder_DA():
    os.environ[DA_ENV] = os.path.join(os.path.dirname(__file__), 'da_methods_another')
    from xsuite import xtend
    DS.tas.xtend._load_env()
    assert hasattr(DS.tas.xtend, 'climate')

def test_load_from_env_and_folder_DS():
    os.environ[DS_ENV] = os.path.join(os.path.dirname(__file__), 'ds_methods_another')
    from xsuite import xtend
    DS.xtend._load_env()
    assert hasattr(DS.xtend, 'anom')


def test_reload_importing():
    from xsuite import xtend
    from xsuite import xtend
    assert True  # Reimport worked


def test_load_env():
    setup_env()
    xsuite.xtend._load_from_env()
    assert hasattr(DS.tas.xtend, 'anomalies')
    assert hasattr(DS.tas.xtend, 'climatology')
    assert hasattr(DS.xtend, 'anomalies')

def test_no_env():
    os.environ[DA_ENV] = ''
    xsuite.xtend._load_from_env('da')
    assert True

def test_remove_env():
    del os.environ[DA_ENV]
    xsuite.xtend._load_from_env('da')
    assert True

def test_no_python_file():
    data = pkg_resources.resource_filename('xsuite', 'data/toyweather.nc')
    folder, _ = os.path.split(data)
    assert not xsuite.xtend.xtend_dataset(folder)
