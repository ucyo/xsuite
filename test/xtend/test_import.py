#!/usr/bin/env python
# coding: utf-8
"""Tests for importing folders with extensions."""


import xarray as xr
from xsuite import xtend

filename = 'data/sresa1b_ncar_ccsm3-example.nc'
ds = xr.open_dataset(filename, decode_times=False)


def test_import_da():
    xtend.xtend_dataarray('test/xtend/da_methods')
    assert hasattr(ds, 'xtend')
    assert hasattr(ds.tas, 'xtend')
    assert hasattr(ds.tas.xtend, 'anomalies')


def test_import_ds():
    xtend.xtend_dataset('test/xtend/ds_methods')
    assert hasattr(ds, 'xtend')
    assert hasattr(ds.xtend, 'anomalies')


def test_import_ds_direct():
    xtend._NyxDS(ds).add_methods('test/xtend/ds_methods')
    assert hasattr(ds, 'xtend')
    assert hasattr(ds.xtend, 'anomalies')


def test_import_da_direct():
    xtend._NyxDA(ds).add_methods('test/xtend/da_methods')
    assert hasattr(ds, 'xtend')
    assert hasattr(ds.tas, 'xtend')
    assert hasattr(ds.tas.xtend, 'anomalies')