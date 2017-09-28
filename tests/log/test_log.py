#!/usr/bin/env python
# coding=utf-8
"""Tests for logging module."""

import os
import logging
import pytest
from xsuite.setup_logging import setup_logging as setup

FOLDER = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(FOLDER, 'log.yml')


@pytest.mark.parametrize('loc', [LOG])
def test_extFile(loc):
    os.environ['LOG_CFG'] = loc
    setup()
    del os.environ['LOG_CFG']
    logger = logging.getLogger(__name__)
    print(logger.getEffectiveLevel)
    assert not logger.isEnabledFor(logging.WARNING)
    assert logging.getLevelName(logger.getEffectiveLevel()) == 'ERROR'
