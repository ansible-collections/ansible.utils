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
    "{{ '10.1.1.1' is ansible.utils.in_any_network ['10.0.0.0/8', '192.168.1.0/24'] }}",
    "{{ '8.8.8.8' is not ansible.utils.in_any_network ['10.0.0.0/8', '192.168.1.0/24', '172.16.0.0/16'] }}",
]


class TestIpaddress(unittest.TestCase):
    def setUp(self):
        self._templar = Templar(loader=None, variables=vars)

    def test_simple(self):
        """ Confirm some simple jinja tests
        """
        for test in TESTS:
            self.assertTrue(self._templar.template(test), test)

    def fail_list_needed(self):
        """ Confirm graceful fail when list is required but not provided
        """
        template_data = "{{ '10.1.1.1' is not ansible.utils.in_one_network '10.0.0.0/8' }}"
        with self.assertRaises(Exception) as error:
            self._templar.template(template_data)
        self.assertIn("'in_one_network' requires a list", str(error.exception))