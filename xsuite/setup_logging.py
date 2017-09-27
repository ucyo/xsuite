#!/usr/bin/env python
# coding=utf-8
"""Logging setup for Logger."""


import logging
from logging import config
import os
import yaml


def setup_logging(path=None, level=logging.INFO, env_key='LOG_CFG'):
    """Setup logging configuration."""
    value = os.getenv(env_key, None)
    if value:
        path = value
    if path and os.path.exists(path):
        with open(path, 'rt') as f:
            configuration = yaml.safe_load(f.read())
    else:
        configuration = yaml.load(YAMLCONFIG)
    config.dictConfig(configuration)

YAMLCONFIG = """ 
version: 1
disable_existing_loggers: False

formatters:
    simple:
        format: "%(asctime)s - %(funcName)s@%(name)s - %(levelname)s - %(message)s"

handlers:
    console:
        class: logging.StreamHandler
        level: ERROR
        formatter: simple
        stream: ext://sys.stdout
    document:
        class: logging.handlers.RotatingFileHandler
        level: NOTSET
        formatter: simple
        maxBytes: 10485760  # 10 MiB
        backupCount: 20
        encoding: utf8
        filename: run.log

root:
    level: DEBUG
    handlers: [console, document]
"""
