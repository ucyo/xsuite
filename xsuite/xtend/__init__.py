"""Extensions for Xarray for analysing weather data."""

from xsuite.xtend.extend import xtend_dataarray, xtend_dataset, _load_from_env

_load_from_env(mode='da')
_load_from_env(mode='ds')
