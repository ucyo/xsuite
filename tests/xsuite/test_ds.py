#!/usr/bin/env python
# coding=utf-8
"""Tests for root xsuite methods."""

import os
import xsuite
import xarray
import numpy as np
import pytest


curdir = os.path.dirname(__file__)
pathpre = (os.pardir, os.pardir, 'data', 'sresa1b_ncar_ccsm3-example.nc')
pathtoy = (os.pardir, os.pardir, 'data', 'toyweather.nc')


def test_ds():
    """Test loading a dataset."""
    f = os.path.join(curdir, *pathpre)
    assert isinstance(xsuite.open_dataset(f), xarray.Dataset)

@pytest.mark.parametrize('example,expected', [
    ('pre', os.path.join(curdir, *pathpre)),
    ('toy', os.path.join(curdir, *pathtoy)),
])
def test_example_data_load(example, expected):
    ex = xsuite.load_data(example)
    ds = xsuite.open_dataset(expected)
    assert np.array_equal(ex,ds)
