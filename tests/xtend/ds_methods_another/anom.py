#!/usr/bin/env python
# coding: utf-8
"""Reverse the ordering of a xr.Dataset."""


def main(dataset):
    """Return monthly anomalies for dataarray."""
    climatology = dataset.groupby('time.month').mean('time')
    anomalies = dataset.groupby('time.month') - climatology
    return anomalies
