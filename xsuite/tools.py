#!/usr/bin/env python
# coding=utf-8
"""Tools help defining recurring tasks."""

import os
import xarray as xr


def load_data(filename, **kwargs):
    """Load file from example data."""
    folder, _ = os.path.split(__file__)
    filename = os.path.join(folder, os.path.pardir, 'data', filename)
    return xr.open_dataset(filename, **kwargs)


def open_dataset(filename_or_obj, *args, **kwargs):
    return xr.open_dataset(filename_or_obj, *args, **kwargs)
