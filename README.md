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
