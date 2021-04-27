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
import ansible_collections.ansible.utils.plugins.plugin_utils.base.ipaddress_utils as ipaddress
from ansible.template import Templar

TESTS = [
    "{{ '10.1.1.1' is ansible.utils.ip }}",
    "{{ 'string' is not ansible.utils.ip }}",
    "{{ '300.1.1.1' is not ansible.utils.ip }}",
]


class TestIpaddress(unittest.TestCase):
    def setUp(self):
        self._templar = Templar(loader=None, variables=vars)

    def test_simple(self):
        """ Confirm some simple jinja tests
        """
        for test in TESTS:
            self.assertTrue(self._templar.template(test), test)

    def test_no_lib(self):
        """ Confirm missing lib
        """
        ipaddress.HAS_IPADDRESS = False
        template_data = "{{ '10.1.1.1' is ansible.utils.ip }}"
        with self.assertRaises(Exception) as error:
            self._templar.template(template_data)
        self.assertIn("'ip' requires 'ipaddress'", str(error.exception))