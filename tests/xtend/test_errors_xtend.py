#!/usr/bin/env python
# coding: utf-8
"""Tests for importing folders with extensions."""

import os
import pytest
from xsuite import xtend
from xsuite.tools import load_data

DS = load_data('pre', decode_times=False)


def test_folder_error():
    with pytest.raises(AssertionError) as err:
        xtend.xtend_dataarray('xtend/nofolder/')
    assert 'is not a folder' in str(err)


def test_mode_err():
    with pytest.raises(ValueError) as err:
        xtend.extend._add_folder('xtend/nofolder/', mode='no')
    assert 'Can not understand mode' in str(err)


def test_no_folder():
    assert not xtend.xtend_dataarray()

def test_no_main():
    with pytest.raises(AttributeError) as err:
        folder, _ = os.path.split(os.path.abspath(__file__))
        xtend.extend._add_folder(os.path.join(folder, 'false_da_methods'), mode='da')
        getattr(DS.tas.xtend, 'false_declaration_anomalies')
    assert "no attribute" in str(err)
