#!/usr/bin/env python
# coding: utf-8
"""Chaining of cdo operators."""

from .cdocmd import CMDWrapper
from xstores import NC4DataStore
import xarray as xr
import os
import tempfile


class BaseChain(object):
    """Enables chaining of cdo functions."""

    def __init__(self, value, options='-f nc'):
        self._value = value
        self._options = options

    def _generate(self):
        """Generate a copy of this instance."""
        new = self.__class__.__new__(self.__class__)
        new.__dict__ = self.__dict__.copy()
        return new


class CMDChain(BaseChain):

    def __init__(self, value, options='-f nc'):
        super(CMDChain, self).__init__(value, options)

    def unwrap(self):
        wrapper = self._generate()
        if isinstance(wrapper._value, str):
            return wrapper._value
        wrapper._value._last = True

        with tempfile.NamedTemporaryFile(suffix=".nc") as f:
            result = wrapper._value.unwrap(f.name)
            if wrapper._value.allow_another_chain:
                result = xr.Dataset.load_store(NC4DataStore(result))
            return result

    def __getattr__(self, attr):
        """Proxy attribute access to cdo."""

        # Check if operator can work with output of previous operator
        if isinstance(self._value, CMDWrapper):
            msg = 'Method "{}" does not allow further chaining'.format(
                self._value.method)
            if not self._value.allow_another_chain:
                raise TypeError(
                    '{}, because of non netCDF output of method.'.format(msg))
            elif self._value.unlimited_input:
                raise TypeError(
                    '{}, because of unlimited input of method.'.format(msg))
        return CMDWrapper(self._value, attr, self._options)
