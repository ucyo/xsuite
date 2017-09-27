#!/usr/bin/env python
# coding=utf-8
"""Tools help defining recurring tasks."""

import pkg_resources
import xarray as xr


def load_data(key, **kwargs):
    """Load file from example data."""
    mapping = {'toy': pkg_resources.resource_filename('xsuite', 'data/toyweather.nc'),
               'pre': pkg_resources.resource_filename('xsuite', 'data/sresa1b_ncar_ccsm3-example.nc')}
    path = mapping.get(key, False)
    if not path:
        raise Exception('Unknown file.')
    return xr.open_dataset(path, **kwargs)


def open_dataset(filename_or_obj, *args, **kwargs):
    return xr.open_dataset(filename_or_obj, *args, **kwargs)
