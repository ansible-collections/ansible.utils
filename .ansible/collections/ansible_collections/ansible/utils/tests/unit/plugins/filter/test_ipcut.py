# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit test file for ipcut filter plugin
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest import TestCase

from ansible_collections.ansible.utils.plugins.filter.ipcut import _ipcut


class TestIpCut(TestCase):
    def setUp(self):
        pass

    def test_get_last_X_bits_ipv6(self):
        """Get last X bits of Ipv6 address"""

        args = ["", "1234:4321:abcd:dcba::17", -80]
        result = _ipcut(*args)
        self.assertEqual(result, "dcba:0:0:0:17")

    def test_get_first_X_bits_ipv6(self):
        """Get first X bits of Ipv6 address"""

        args = ["", "1234:4321:abcd:dcba::17", 64]
        result = _ipcut(*args)
        self.assertEqual(result, "1234:4321:abcd:dcba")

    def test_get_last_X_bits_ipv4(self):
        """Get last X bits of Ipv4 address"""

        args = ["", "10.2.3.0", -16]
        result = _ipcut(*args)
        self.assertEqual(result, "3.0")

    def test_get_first_X_bits_ipv4(self):
        """Get first X bits of Ipv4 address"""

        args = ["", "10.2.3.0", 24]
        result = _ipcut(*args)
        self.assertEqual(result, "10.2.3")
