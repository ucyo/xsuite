#!/usr/bin/env python
# coding: utf-8
"""Error messages for NC4DataStore"""

import os
import pytest
from xsuite.backend import xstores
import netCDF4 as nc4
import xarray as xr

filename = os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir, 'data', 'sresa1b_ncar_ccsm3-example.nc')
# filename = 'data/sresa1b_ncar_ccsm3-example.nc'


def test_not_nc_dataset():
    with pytest.raises(TypeError) as err:
        xstores.NC4DataStore('Not a NC Dataset')
    assert 'ds is not a NETCDF4 dataset' in str(err)


def test_not_str_or_dataset():
    with pytest.raises(TypeError) as err:
        xstores.NC4DataStore(32)
    assert 'Object is neither a string nor a NETCDF4' in str(err)


def test_without_format():
    data = nc4.Dataset(filename)
    ds = xr.Dataset.load_store(xstores.NC4DataStore(data, format=None))
    assert isinstance(ds, xr.Dataset)


def test_just_filename():
    ds = xr.Dataset.load_store(xstores.NC4DataStore(filename, format=None))
    assert isinstance(ds, xr.Dataset)
