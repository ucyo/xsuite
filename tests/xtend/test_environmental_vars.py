#!/usr/bin/env python
# coding=utf-8
"""Test environmental variables for extension of xarray."""

import xarray as xr
import os
from xsuite.tools import load_data

DA_ENV = 'XSUITE_DA_FOLDERS'
DS_ENV = 'XSUITE_DS_FOLDERS'

for var in [DA_ENV, DS_ENV]:
    if not os.getenv(var, False):
        os.environ[var] = 'xtend/da_methods:xtend/da_methods_other' if 'DA' in var else 'xtend/ds_methods'

FILENAME = 'data/sresa1b_ncar_ccsm3-example.nc'
DS = xr.open_dataset(FILENAME, decode_times=False)
FILENAME = 'sresa1b_ncar_ccsm3-example.nc'
DS = load_data(FILENAME, decode_times=False)


def test_load_from_env():
    from xsuite import xtend
    assert hasattr(DS.tas.xtend, 'anomalies')
    assert hasattr(DS.tas.xtend, 'climatology')
    assert hasattr(DS.xtend, 'anomalies')


def test_load_from_env_and_folder():
    os.environ[DA_ENV] = 'xtend/da_methods_another'
    from xsuite import xtend
    DS.tas.xtend.load_env()
    assert hasattr(DS.tas.xtend, 'climate')


def test_reload_importing():
    from xsuite import xtend
    from xsuite import xtend
