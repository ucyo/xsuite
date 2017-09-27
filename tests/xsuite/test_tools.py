#!/usr/bin/env python
# coding=utf-8
"""Test tools submodule."""

import pytest
from xsuite.tools import load_data

def test_raise_exc():
    with pytest.raises(Exception) as err:
        load_data('unknown')
    assert 'Unknown file' in str(err)
