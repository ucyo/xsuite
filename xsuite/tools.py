#!/usr/bin/env python
# coding=utf-8
"""Tools help defining recurring tasks."""

import os
import xarray as xr


def load_data(key, **kwargs):
    """Load file from example data."""
    mapping = {'toy':'toyweather.nc',
               'pre':'sresa1b_ncar_ccsm3-example.nc'}
    
    def get_path(hint):
        filename = mapping.get(hint, False)
        if not filename:
            raise ValueError('Unknown file')
        folder, _ = os.path.split(__file__)
        return os.path.join(folder, os.path.pardir, 'data', filename)

    path = get_path(key)
    return xr.open_dataset(path, **kwargs)


def open_dataset(filename_or_obj, *args, **kwargs):
    return xr.open_dataset(filename_or_obj, *args, **kwargs)
