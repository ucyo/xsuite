#!/usr/bin/env python
# coding: utf-8
"""Tests for importing folders with extensions."""

import os
from xsuite import xtend
import pytest
from xsuite.tools import load_data

FILENAME = 'sresa1b_ncar_ccsm3-example.nc'
ds = load_data(FILENAME, decode_times=False)


def test_folder_error():
    with pytest.raises(AssertionError) as err:
        xtend.xtend_dataarray('xtend/nofolder/')
    assert 'is not a folder' in str(err)


def test_mode_err():
    with pytest.raises(ValueError) as err:
        xtend.extend._add_folder('xtend/nofolder/', mode='no')
    assert 'Can not understand mode' in str(err)


# def test_no_main():
#     with pytest.raises(AttributeError) as err:
#         xtend.xtend_dataarray('xtend/false_da_methods')
#     assert 'has no "main" function' in str(err)


def test_no_folder():
    assert not xtend.xtend_dataarray()


def test_no_pyfiles():
    assert not xtend.xtend_dataarray('data')
