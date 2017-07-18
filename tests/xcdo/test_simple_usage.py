#!/usr/bin/env python
# coding: utf-8
"""Test simple usage."""

from xsuite import xcdo
import xarray as xr


filename = 'data/sresa1b_ncar_ccsm3-example.nc'
ds = xr.open_dataset(filename, decode_times=False)


def test_back_to_back_execution():
    xcdo.CDO(ds).zonmean().result()
    xcdo.CDO(ds).zonmean().result()


def test_chaining_str():
    hello = xcdo.cdocmd.CMDChain('hello')
    assert hello.result() == 'hello'


def test_input2():
    result = xcdo.cdocmd.CMDChain(filename).diffn(
        'data/sresa1b_ncar_ccsm3-example_2.nc').result()
    assert result == []


def test_unlimited_input():
    result = xcdo.cdocmd.CMDChain(filename).mergetime(
        'data/sresa1b_ncar_ccsm3-example_2.nc').result()
    assert isinstance(result, xr.Dataset)


def test_string_input():
    result = xcdo.cdocmd.CMDChain(filename).result()
    assert result == filename


def test_sellonlatbox():
    result = ds.xcdo.sellonlatbox(3, 20, -40, 40).result()
    assert isinstance(result, xr.Dataset)


# def test_inception():
#     level0 = xcdo.cdocmd.CMDChain(filename)
#     level1 = xcdo.cdocmd.CMDChain(level0).zonmean().result()
#     assert isinstance(level1, xr.Dataset)


def test_args():
    result = ds.xcdo.mermean().sellonlatbox(3, 20, -40, 40).result()
    assert isinstance(result, xr.Dataset)


def test_args_otherway():
    result = ds.xcdo.sellonlatbox(3, 20, -40, 40).mermean().result()
    assert isinstance(result, xr.Dataset)


def test_args_otherway_levels():
    result = ds.xcdo.sellonlatbox(3, 20, -40, 40).sellevidx(2, 4, 7).result()
    assert isinstance(result, xr.Dataset)
