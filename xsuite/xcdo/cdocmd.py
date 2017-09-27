#!/usr/bin/env python
# coding: utf-8
"""Class for cdo operators."""

import re
import os
import tempfile

from cdo import Cdo
import xarray as xr
from xsuite.xcdo.helpers import mapping, nodoc
from xsuite.backend.xstores import NC4DataStore


class CMD(object):

    def __init__(self, method):
        if not getattr(Cdo(), method, False):
            raise ValueError('{} is not a cdo method'.format(method))
        elif method in nodoc.keys():
            raise ValueError('Command {} not supported'.format(method))
        self.method = method
        self._mappedmethod = mapping.get(self.method, self.method)
        self._regex = self.__class__._regex(self._mappedmethod)
        self.params, self.cmdstring = self._specify_format()

    def _specify_format(self):
        p = re.compile(self._regex)
        m = p.search(getattr(Cdo(), self.method).__doc__)
        elements, cmdstring = m.groupdict(), m.group()
        cmdstring = cmdstring.replace(elements['method'], self.method)
        elements['method'] = self.method
        return elements, cmdstring

    @classmethod
    def _regex(cls, method):
        _regex = "(?P<method>" + method + \
            "|<operator>)(?P<args>[\s+|[\,|\[][\[?\,\w*]*\]*)(?:\s+)(?P<input1>in?file[s|1]?)(?:\s+)?(?P<input2>in?file2)?(?:\s+)?(?P<output>ou?t?file)?"
        return _regex

    @property
    def filtered(self):
        params = self.params
        result = {k: v for k, v in params.items() if v and v != ' '}

        # The method in regex cmdstring might be a mapping
        result['method'] = self.method
        return result

    @property
    def rcmdstring(self):
        result = self.cmdstring
        for k, v in self.filtered.items():
            if k == 'method':
                result = result.replace(v, '-{' + k + '}')
            if k == 'args':
                result = result.replace(v, ',{' + k + '}')
            else:
                result = result.replace(v, '{' + k + '}')
        return result


class CMDWrapper(CMD):

    def __init__(self, value, method, options='-O -f nc'):
        self._value = value
        super(CMDWrapper, self).__init__(method)
        self._setup_unwrap()
        self._last = False
        self._options = options

    def _setup_unwrap(self):
        self.unlimited_input = self.params.get('input1', '') in ['ifiles','infiles']
        self.allow_another_chain = 'output' in self.filtered.keys()
        self.allow_args = 'args' in self.filtered.keys(
        ) or 'input2' in self.filtered.keys() or self.unlimited_input
        self.opt_args = '[' == self.params.get('args', False)[0]
        self.mandatory_args = ('args' in self.filtered.keys() or
                               'input2' in self.filtered.keys()) and not self.opt_args

    def _generate(self):
        """Generate a copy of this instance."""
        new = self.__class__.__new__(self.__class__)
        new.__dict__ = self.__dict__.copy()
        return new

    def __call__(self, *args, **kwargs):
        """Invoke the method with value as the first argument and return a new
        Chain object with the return value.
        """
        if (self.mandatory_args or 'input2' in self.filtered.keys()) and not args:
            raise ValueError(
                'Arguments are mandatory for {}'.format(self.method))
        elif not self.allow_args and args:
            raise ValueError(
                'Method {} does not take any arguments'.format(self.method))

        # Sometimes instead of arguments the operator expects another datafile.
        # In this case the args must be provided and will be interpreted as
        # path to the second file
        if 'input2' in self.filtered.keys():
            if len(args) > 1:
                raise ValueError(
                    'Expected only one argument for method {}'.format(self.method))
            if not os.path.isfile(args[0]):
                raise TypeError(
                    'Method {} expects a file as an argument'.format(self.method))
        self.args = args
        self.kwargs = kwargs
        return CMDChain(self)

    def unwrap(self, tmpfile):
        if self._last:
            if isinstance(self._value, CMDWrapper):
                self.input1 = self._value.unwrap(tmpfile)
            elif isinstance(self._value, xr.Dataset):
                self._value.to_netcdf(tmpfile)
                self.input1 = tmpfile
            else:
                self.input1 = self._value
            if 'input2' in self.filtered.keys():
                self.input1 = [self.input1, ','.join([str(x) for x in self.args])]
                self.args = None
            if self.unlimited_input:
                self.input1 = [self.input1] + list(self.args)
                self.args = None
            if self.args:
                self.args = ','.join([str(x) for x in self.args])
                return getattr(Cdo(), self.method)(self.args, input=self.input1, options=self._options, returnCdf=True)
            else:
                return getattr(Cdo(), self.method)(input=self.input1, options=self._options, returnCdf=True)
        self.output = ''
        if self.args:
            self.args = ','.join([str(x) for x in self.args])
        if isinstance(self._value, CMDWrapper):
            self.input1 = self._value.unwrap(tmpfile)
        elif isinstance(self._value, xr.Dataset):
            self._value.to_netcdf(tmpfile)
            self.input1 = tmpfile
        else:
            self.input1 = self._value
        return self.rcmdstring.format(**self.__dict__)

class BaseChain(object):
    """Enables chaining of cdo functions."""

    def __init__(self, value, options='-f nc'):
        self._value = value
        self._options = options

    def _generate(self):
        """Generate a copy of this instance."""
        new = self.__class__.__new__(self.__class__)
        new.__dict__ = self.__dict__.copy()
        return new


class CMDChain(BaseChain):

    def __init__(self, value, options='-f nc'):
        super(CMDChain, self).__init__(value, options)

    def result(self):
        wrapper = self._generate()
        if isinstance(wrapper._value, str):
            return wrapper._value
        wrapper._value._last = True

        with tempfile.NamedTemporaryFile(suffix=".nc") as f:
            result = wrapper._value.unwrap(f.name)
            if wrapper._value.allow_another_chain:
                result = xr.Dataset.load_store(NC4DataStore(result))
            return result

    def __getattr__(self, attr):
        """Proxy attribute access to cdo."""

        # Check if operator can work with output of previous operator
        if isinstance(self._value, CMDWrapper):
            msg = 'Method "{}" does not allow further chaining'.format(
                self._value.method)
            if not self._value.allow_another_chain:
                raise TypeError(
                    '{}, because of non netCDF output of method.'.format(msg))
            elif self._value.unlimited_input:
                raise TypeError(
                    '{}, because of unlimited input of method.'.format(msg))
        return CMDWrapper(self._value, attr, self._options)
