#!/usr/bin/env python
# coding: utf-8
"""Error messages for NC4DataStore"""

import pytest
from xsuite import xstores
import netCDF4 as nc4
import xarray as xr

filename = 'data/sresa1b_ncar_ccsm3-example.nc'


def test_not_nc_dataset():
    with pytest.raises(TypeError) as err:
        xstores.NC4DataStore('Not a NC Dataset')
    assert 'ds is not a NETCDF4 dataset' in str(err)


def test_without_format():
    data = nc4.Dataset(filename)
    ds = xr.Dataset.load_store(xstores.NC4DataStore(data, format=None))
    assert isinstance(ds, xr.Dataset)


def test_just_filename():
    ds = xr.Dataset.load_store(xstores.NC4DataStore(filename, format=None))
    assert isinstance(ds, xr.Dataset)
