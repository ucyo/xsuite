#!/usr/bin/env python
# coding: utf-8
"""Test error messages."""

import pytest
from xsuite import xcdo
import xarray as xr


filename = 'data/sresa1b_ncar_ccsm3-example.nc'
ds = xr.open_dataset(filename, decode_times=False)


def test_no_value():
    with pytest.raises(ValueError) as excinfo:
        xcdo.CDO(ds).zonmean(23).unwrap()
    assert 'does not take any arguments' in str(excinfo.value)


def test_no_input_after_noncinput():
    with pytest.raises(TypeError) as excinfo:
        xcdo.CDO(ds).sinfon().zonmean().unwrap()
    assert 'does not allow further chaining, because of' in str(excinfo.value)


@pytest.mark.parametrize("method", ['ml2pl', 'diffn', 'sellonlatbox'])
def test_mandatory_args(method):
    with pytest.raises(ValueError) as excinfo:
        getattr(xcdo.CDO(ds), method)().zonmean().unwrap()
    assert 'Arguments are mandatory for' in str(excinfo.value)


@pytest.mark.parametrize("method", ['mergetime', ])
def test_unlimited_args(method):
    with pytest.raises(TypeError) as excinfo:
        getattr(xcdo.CDO(ds), method)().zonmean().unwrap()
    assert 'because of unlimited input of method' in str(excinfo.value)


@pytest.mark.parametrize("method", ['zonmean', ])
def test_forbidden_args(method):
    with pytest.raises(ValueError) as excinfo:
        getattr(xcdo.CDO(ds), method)(231).unwrap()
    assert method + ' does not take any arguments' in str(excinfo.value)


def test_default_options_given():
    data = xcdo.CDO(ds).mermean().unwrap()
    options = data.attrs['history'].split('cdo', 1)[1].split('mermean', 1)[0]
    assert ' -O -f nc ' == options


def test_wrong_input():
    with pytest.raises(AssertionError) as excinfo:
        xcdo.CDO(filename)
    assert 'Input not a xr.Dataset' in str(excinfo.value)


@pytest.mark.parametrize("method", ['meanzo', ])
def test_wrong_method(method):
    with pytest.raises(ValueError) as excinfo:
        getattr(xcdo.CDO(ds), method)(231).unwrap()
    assert method + ' is not a cdo method' in str(excinfo.value)


@pytest.mark.parametrize("method", ['cmor', 'readCdf'])
def test_nodoc(method):
    with pytest.raises(ValueError) as excinfo:
        getattr(xcdo.CDO(ds), method)(231).unwrap()
    assert method + ' not supported' in str(excinfo.value)


@pytest.mark.parametrize("method", ['diffn', ])
def test_input2_args(method):
    with pytest.raises(TypeError) as excinfo:
        getattr(xcdo.chaining.CMDChain(filename), method)('nonvalid.input')
    assert method + ' expects a file as an argument' in str(excinfo.value)


@pytest.mark.parametrize("method", ['diffn', ])
def test_input2_only_one_args(method):
    with pytest.raises(ValueError) as excinfo:
        getattr(xcdo.chaining.CMDChain(filename), method)('nonvalid.input', 2)
    assert 'Expected only one argument for method' in str(excinfo.value)
