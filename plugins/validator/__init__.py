"""
The base class for validator
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ValditorBase(object):
    """ The base class for data validators
    Provides a  _debug function to normalize debug output
    """

    def __init__(self, task_args, task_vars, debug):
        self._debug = debug
        self._task_args = task_args
        self._task_vars = task_vars