#!/usr/bin/env python
# coding: utf-8
"""Tests for importing folders with extensions."""


import os
from xsuite import xtend
from xsuite.tools import load_data


ds = load_data('pre', decode_times=False)


def test_import_da():
    folder = os.path.join(os.path.dirname(__file__), 'da_methods')
    xtend.xtend_dataarray(folder)    
    assert hasattr(ds, 'xtend')
    assert hasattr(ds.tas, 'xtend')
    assert hasattr(ds.tas.xtend, 'anomalies')


def test_import_ds():
    folder = os.path.join(os.path.dirname(__file__), 'ds_methods')
    xtend.xtend_dataset(folder)    
    assert hasattr(ds, 'xtend')
    assert hasattr(ds.xtend, 'anomalies')


def test_import_ds_direct():
    folder = os.path.join(os.path.dirname(__file__), 'ds_methods')
    xtend.extend._NyxDS(ds)._add_methods(folder)
    assert hasattr(ds, 'xtend')
    assert hasattr(ds.xtend, 'anomalies')


def test_import_da_direct():
    folder = os.path.join(os.path.dirname(__file__), 'da_methods')
    xtend.extend._NyxDA(ds)._add_methods(folder)
    assert hasattr(ds, 'xtend')
    assert hasattr(ds.tas, 'xtend')
    assert hasattr(ds.tas.xtend, 'anomalies')
