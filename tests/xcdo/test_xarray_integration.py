#!/usr/bin/env python
# coding: utf-8
"""Test xarray integration."""

from xsuite.tools import load_data
from xsuite import xcdo


ds = load_data('pre', decode_times=False)


def test_back_to_back_execution():
    ds.xcdo.zonmean().result()
    ds.xcdo.zonmean().result()


def test_no_options_given():
    data = ds.xcdo.mermean().result()
    options = data.attrs['history'].split('cdo', 1)[1].split('mermean', 1)[0]
    assert ' -O -f nc ' == options


def test_options_given():
    data = ds.xcdo('-s').mermean().result()
    options = data.attrs['history'].split('cdo', 1)[1].split('mermean', 1)[0]
    assert ' -O -s ' == options
