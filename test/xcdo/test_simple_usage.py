#!/usr/bin/env python
# coding: utf-8
"""Test simple usage."""

import xcdo
import xarray as xr


filename = 'data/sresa1b_ncar_ccsm3-example.nc'
ds = xr.open_dataset(filename, decode_times=False)


def test_back_to_back_execution():
    xcdo.CDO(ds).zonmean().unwrap()
    xcdo.CDO(ds).zonmean().unwrap()


def test_chaining_str():
    hello = xcdo.chaining.CMDChain('hello')
    assert hello.unwrap() == 'hello'


def test_input2():
    result = xcdo.chaining.CMDChain(filename).diffn(
        'data/sresa1b_ncar_ccsm3-example_2.nc').unwrap()
    assert result == []


def test_unlimited_input():
    result = xcdo.chaining.CMDChain(filename).mergetime(
        'data/sresa1b_ncar_ccsm3-example_2.nc').unwrap()
    assert isinstance(result, xr.Dataset)


def test_string_input():
    result = xcdo.chaining.CMDChain(filename).unwrap()
    assert result == filename


def test_sellonlatbox():
    result = ds.xcdo.sellonlatbox(3, 20, -40, 40).unwrap()
    assert isinstance(result, xr.Dataset)


# def test_inception():
#     level0 = xcdo.chaining.CMDChain(filename)
#     level1 = xcdo.chaining.CMDChain(level0).zonmean().unwrap()
#     assert isinstance(level1, xr.Dataset)


def test_args():
    result = ds.xcdo.mermean().sellonlatbox(3, 20, -40, 40).unwrap()
    assert isinstance(result, xr.Dataset)


def test_args_otherway():
    result = ds.xcdo.sellonlatbox(3, 20, -40, 40).mermean().unwrap()
    assert isinstance(result, xr.Dataset)


def test_args_otherway_levels():
    result = ds.xcdo.sellonlatbox(3, 20, -40, 40).sellevidx(2, 4, 7).unwrap()
    assert isinstance(result, xr.Dataset)
