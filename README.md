# xsuite
This python module provides several extensions for xarray in one package.
Currently there are three extensions:

- `xsuite.xcdo` Support cdo command line tool from within xarray
- `xsuite.xtend` Extend xarray.Datasets and xarray.DataArrays with functions
- `xsuite.backend.xstores` Additional datastores for different formats

## Installation
The module can be installed via `python setup.py install` or `pip install .`

## Usage

This repository is a collection of several extensions for `xarray`. Therefore
we will describe each extension by itself. Starting with `xcdo`.

### xcdo

The `xcdo` module integrates the [climate data operators](https://code.mpimet.mpg.de/projects/cdo)
(cdo) with `xarray`. It is possible to use all [operators](https://code.mpimet.mpg.de/projects/cdo/embedded/index.html)
provided by the cdo toolset to be used on `xr.Dataset` instances.

Here is an example:

```python

from xsuite import xcdo
import xarray as xr

filename = './data/sresa1b_ncar_ccsm3-example.nc'
ds = xr.open_dataset(filename, decode_times=False)

ds.xcdo.mermean().zonmean().result()  # this will return a xr.Dataset instance

```

The module supports:
- Concatenation of operators.
- Syntax checking for each operator.
- Lazy execution via `.result()` keyword.

More information can be found [here](xsuite/xcdo/README.md).


### xtend

The `xtend` module aims to provide easy on-the-fly extension of `xarray.Dataset`
and `xarray.DataArray` instances.

Here is an example:

```python

from xsuite import xtend
import xarray as xr
import os

folder = 'test/xtend/da_methods'
print(os.listdir(folder))  # Output: ['anomalies.py', ]
xtend.xtend_dataarray(folder)

filename = './data/sresa1b_ncar_ccsm3-example.nc'
ds = xr.open_dataset(filename, decode_times=False)
ds.tas.xtend.anomalies()  # this will return an xr.DataArray instance
```

Two things are important for using `xtend`:
- The python scripts need to have a `main(arg0, ..)` function. This function will be
called by `xtend`.
- The first argument `arg0` in the main function must be representing
a `xr.Dataset` for `xtend.xtend_dataset()` or a `xr.DataArray` for `xtend.xtend_dataarray()`.
- The method under which the python script will be saved is the filename. Like
in the example given above the file `anomalies.py` will be called by `ds.xtend.anomalies()`.

More information can be found [here](xsuite/xtend/README.md).

## Todo

- [ ] Add license from salem and xarray because of (./xsuite/backend/xstores/NC4DataStore.py).
