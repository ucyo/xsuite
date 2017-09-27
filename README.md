# xsuite
This python module provides several extensions for xarray in one package.
Currently there are three extensions:

- `xsuite.xcdo` Support cdo command line tool from within xarray
- `xsuite.xtend` Extend xarray.Datasets and xarray.DataArrays with functions
- `xsuite.backend.xstores` Additional datastores for different formats

> cdo version 1.9.0 is currently not supported. The toolset does not support
> the `returnCdf` command anymore. Any [issue](https://code.mpimet.mpg.de/issues/7839#change-33102)
> has been opened.

## Installation
The module is compatible with `py2` and `py3` and can be installed via `pip install .`

## Usage

This repository is a collection of several extensions for `xarray`. Therefore
we will describe each extension by itself. Starting with `xcdo`.

### xcdo

The `xcdo` module integrates the [climate data operators](https://code.mpimet.mpg.de/projects/cdo)
(cdo) with `xarray`. It is possible to use all [operators](https://code.mpimet.mpg.de/projects/cdo/embedded/index.html)
provided by the cdo toolset to be used on `xr.Dataset` instances.

Here is an example:

```python
from xsuite import xcdo, load_data

ds = load_data('pre', decode_times=False)

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
import os
import xsuite
import xarray as xr
from xsuite import xtend

folder = './examples/'
print(os.listdir(folder))  # Output: ['anomalies.py', ]
xtend.xtend_dataarray(folder)

ds = xsuite.load_data('toy')
ds.tmin.xtend.anomalies()  # this will return an xr.DataArray instance
```

Two things are important for using `xtend`:
- The python scripts need to have a `main(arg0, ..)` function. This function will be
called by `xtend`.
- The first argument `arg0` in the main function must be representing
a `xr.Dataset` for `xtend.xtend_dataset()` or a `xr.DataArray` for `xtend.xtend_dataarray()`.
- The method under which the python script will be saved is the filename. Like
in the example given above the file `anomalies.py` will be called by `ds.xtend.anomalies()`.

More information can be found [here](xsuite/xtend/README.md).
