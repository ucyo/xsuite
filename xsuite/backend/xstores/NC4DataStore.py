#!/usr/bin/env python
# coding: utf-8
"""DataStore for reading netCDF4.Dataset objects."""

from functools import partial
from xarray.backends import NetCDF4DataStore
from xarray.backends.netCDF4_ import is_remote_uri, close_on_error, _nc4_group

import netCDF4 as nc
import os


class NC4DataStore(NetCDF4DataStore):
    """DataStore for opening in-memory netCDF4.Dataset objects.
    """

    # Ref @ https://github.com/fmaussion/salem/blob/master/salem/sio.py#L884
    def __init__(self, ds, mode='r', format='NETCDF4', group=None,
                 writer=None, clobber=True, diskless=False, persist=False,
                 autoclose=False):
        if not isinstance(ds, (nc.Dataset, str)):
            raise TypeError('Object is neither a string nor a NETCDF4 dataset')
        if isinstance(ds, str) and not os.path.isfile(ds):
            raise TypeError(
                'ds is not a NETCDF4 dataset, but {}'.format(type(ds)))

        if isinstance(ds, str):
            self._filename = ds
            filename = ds
            ds = None
        else:
            filename = ds.filepath() if os.path.isfile(ds.filepath()) else ""
            self._filename = filename

        if format is None:
            format = 'NETCDF4'
        opener = partial(_open_netcdf4_group, filename, mode=mode,
                         group=group, clobber=clobber, diskless=diskless,
                         persist=persist, format=format, ds=ds)
        self.ds = opener()
        self._autoclose = autoclose
        self._isopen = True
        self.format = format
        self.is_remote = is_remote_uri(filename)
        self._mode = 'a' if mode == 'w' else mode
        self._opener = partial(opener, mode=self._mode)
        super(NetCDF4DataStore, self).__init__(writer)


def _open_netcdf4_group(filename, mode, group=None, ds=None, **kwargs):
    """
    This code is adapted from xarray's _open_netcdf4_group func.
    """
    # Ref @ https://github.com/fmaussion/salem/blob/master/salem/sio.py#L865
    if ds is None:
        ds = nc.Dataset(filename, mode=mode, **kwargs)

    with close_on_error(ds):
        ds = _nc4_group(ds, group, mode)

    for var in ds.variables.values():
        # we handle masking and scaling ourselves
        var.set_auto_maskandscale(False)
    return ds
