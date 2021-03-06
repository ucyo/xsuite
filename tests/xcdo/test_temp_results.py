#!/usr/bin/env python
# coding: utf-8
"""Test simple usage."""
from xsuite.tools import load_data

from xsuite import xcdo
import pytest


ds = load_data('pre', decode_times=False)


@pytest.mark.parametrize("method,expected",
                         [('zonmean', '-{method}  {input1} {output}'),
                          ])
def test_wrapperobj(method, expected):
    wrapperobj = getattr(xcdo.CDO(ds), method)()._value
    assert wrapperobj.rcmdstring == expected


@pytest.mark.parametrize("method,expected",
                         [('sellonlatbox',
                           '-{method},{args}  {input1} {output}'),
                          ])
def test_wrapperobjwithargs(method, expected):
    wrapperobj = getattr(xcdo.CDO(ds), method)(2)._value
    assert wrapperobj.rcmdstring == expected


@pytest.mark.parametrize('method', ['zonmean'])
def test_new_instance(method):
    result = getattr(xcdo.CDO(ds), method)()._value
    clone = result._generate()
    assert result.__dict__ == clone.__dict__
