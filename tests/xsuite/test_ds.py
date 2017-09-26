#!/usr/bin/env python
# coding=utf-8
"""Tests for root xsuite methods."""

import os
import xsuite
import xarray
import numpy as np
import pytest
import pkg_resources


curdir = os.path.dirname(__file__)
pathpre = pkg_resources.resource_filename('xsuite', 'data/sresa1b_ncar_ccsm3-example.nc')
pathtoy = pkg_resources.resource_filename('xsuite', 'data/toyweather.nc')


def test_ds():
    """Test loading a dataset."""
    assert isinstance(xsuite.open_dataset(pathpre), xarray.Dataset)

@pytest.mark.parametrize('example,expected', [
    ('pre', pathpre),
    ('toy', pathtoy),
])
def test_example_data_load(example, expected):
    ex = xsuite.load_data(example)
    ds = xsuite.open_dataset(expected)
    assert np.array_equal(ex,ds)
