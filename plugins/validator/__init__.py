"""
The base class for validator
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ValditorBase(object):
    """ The base class for data validators
    Provides a  _debug function to normalize debug output
    """

    def __init__(self, data, criteria, plugin_vars={}, **kwargs):
        self._data = data
        self._criteria = criteria
        self._plugin_vars = plugin_vars
        self._result = {}
        self._kwargs = kwargs
