#!/usr/bin/env python
# coding=utf-8
"""Tests for root xsuite methods."""

import os
import xsuite
import xarray


curdir = os.path.dirname(__file__)
relpath = (os.pardir, os.pardir, 'data', 'sresa1b_ncar_ccsm3-example.nc')


def test_ds():
    """Test loading a dataset."""
    f = os.path.join(curdir, *relpath)
    assert isinstance(xsuite.open_dataset(f), xarray.Dataset)
