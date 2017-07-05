#!/usr/bin/env python
# coding: utf-8
"""Test xarray integration."""

import xcdo
import xarray as xr


filename = 'data/sresa1b_ncar_ccsm3-example.nc'
ds = xr.open_dataset(filename, decode_times=False)


def test_back_to_back_execution():
    ds.xcdo.zonmean().unwrap()
    ds.xcdo.zonmean().unwrap()


def test_no_options_given():
    data = ds.xcdo.mermean().unwrap()
    options = data.attrs['history'].split('cdo', 1)[1].split('mermean', 1)[0]
    assert ' -O -f nc ' == options


def test_options_given():
    data = ds.xcdo('-s').mermean().unwrap()
    options = data.attrs['history'].split('cdo', 1)[1].split('mermean', 1)[0]
    assert ' -O -s ' == options
