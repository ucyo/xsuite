# xarray-datastores

Which can be loaded from the xr.Dataset directly by
[`xr.Dataset.load_store()`](https://github.com/pydata/xarray/blob/master/xarray/core/dataset.py#L375)

The AbstractClass is defined as [`xr.backends.common.AbstractDataStore(Mapping)`](https://github.com/pydata/xarray/blob/master/xarray/backends/common.py#L79)

## Examples
BPCHDataStore @
https://github.com/darothen/xbpch/blob/master/xbpch/core.py#L218

MDSDataStore @
https://github.com/xgcm/xmitgcm/blob/master/xmitgcm/mds_store.py#L261

Official Stores @
https://github.com/pydata/xarray/blob/master/xarray/backends/__init__.py

### Examples from issues
netCDF4.Dataset class @
https://github.com/fmaussion/salem/blob/master/salem/sio.py#L884

## Special Issues
Datetime conversion @
https://github.com/pydata/xarray/blob/6b18d77b5581be4d91cb12da95a530f92ab867b5/xarray/conventions.py#L376
