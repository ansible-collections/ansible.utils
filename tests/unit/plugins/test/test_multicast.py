# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The test plugin file for netaddr tests
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import unittest  # TestCase, assertTrue
from ansible.template import Templar

TESTS = [
    "{{ '224.0.0.1' is ansible.utils.multicast }}",
    "{{ '127.0.0.1' is not ansible.utils.multicast }}",
]


class TestIpaddress(unittest.TestCase):
    def setUp(self):
        self._templar = Templar(loader=None, variables=vars)

    def test_simple(self):
        """ Confirm some simple jinja tests
        """
        for test in TESTS:
            self.assertTrue(self._templar.template(test), test)