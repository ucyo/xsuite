#!/usr/bin/env python
# coding: utf-8
"""Calculate anomalies within a xr.DataArray."""


def main(dataarray):
    """Return monthly anomalies for dataarray."""
    climatology = dataarray.groupby('time.month').mean('time')
    anomalies = dataarray.groupby('time.month') - climatology
    return anomalies
