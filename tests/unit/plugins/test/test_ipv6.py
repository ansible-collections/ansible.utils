# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit test file for netaddr test plugin: ipv6
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest import TestCase

from ansible_collections.ansible.utils.plugins.test.ipv6 import _ipv6


class TestIpV6(TestCase):
    def setUp(self):
        pass

    def test_invalid_data(self):
        """Check passing invalid argspec"""

        # missing argument
        with self.assertRaises(TypeError) as error:
            _ipv6()
        self.assertIn("argument", str(error.exception))

    def test_valid_data(self):
        """Check passing valid data as per criteria"""

        result = _ipv6(ip="fe80::216:3eff:fee4:16f3")
        self.assertEqual(result, True)

        result = _ipv6(ip="2001:db8:a::/64")
        self.assertEqual(result, True)

        result = _ipv6(ip="10.1.1.1")
        self.assertEqual(result, False)

        result = _ipv6(ip="string")
        self.assertEqual(result, False)
