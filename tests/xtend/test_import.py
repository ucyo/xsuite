#!/usr/bin/env python
# coding: utf-8
"""Tests for importing folders with extensions."""


import os
from xsuite import xtend
from xsuite.tools import load_data


FILENAME = 'sresa1b_ncar_ccsm3-example.nc'
ds = load_data(FILENAME, decode_times=False)


filename = 'data/sresa1b_ncar_ccsm3-example.nc'
ds = xr.open_dataset(filename, decode_times=False)


def test_import_da():
    xtend.xtend_dataarray('xtend/da_methods')
    assert hasattr(ds, 'xtend')
    assert hasattr(ds.tas, 'xtend')
    assert hasattr(ds.tas.xtend, 'anomalies')


def test_import_ds():
    xtend.xtend_dataset('xtend/ds_methods')
    assert hasattr(ds, 'xtend')
    assert hasattr(ds.xtend, 'anomalies')


def test_import_ds_direct():
    xtend.extend._NyxDS(ds).add_methods('xtend/ds_methods')
    assert hasattr(ds, 'xtend')
    assert hasattr(ds.xtend, 'anomalies')


def test_import_da_direct():
    xtend.extend._NyxDA(ds).add_methods('xtend/da_methods')
    assert hasattr(ds, 'xtend')
    assert hasattr(ds.tas, 'xtend')
    assert hasattr(ds.tas.xtend, 'anomalies')
