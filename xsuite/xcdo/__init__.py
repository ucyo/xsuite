#!/usr/bin/env python
# coding: utf-8
"""Xarray accessor for cdo operators."""

import xarray as xr
import tempfile
from xsuite.xcdo.cdocmd import CMDChain as Chain


@xr.register_dataset_accessor('xcdo')
class CDO(object):

    def __init__(self, ds, options='-f nc'):
        assert isinstance(ds, xr.Dataset), 'Input not a xr.Dataset'
        # tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.nc')
        # ds.to_netcdf(tmp.name)
        self._chain = Chain(ds, options=options)

    def __getattr__(self, attr):
        return getattr(self._chain, attr)

    def __call__(self, options):
        self._chain._options = options
        return self
