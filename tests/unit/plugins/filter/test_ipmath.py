# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit test file for ipmath filter plugin
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest import TestCase

from ansible.errors import AnsibleFilterError

from ansible_collections.ansible.utils.plugins.filter.ipmath import _ipmath


class TestIpAddr(TestCase):
    def setUp(self):
        pass

    def test_find_next_fifth_address(self):
        """Get the next fifth address based on an IP address"""

        args = ["", "192.168.1.5", 5]
        result = _ipmath(*args)
        self.assertEqual(result, "192.168.1.10")

    def test_find_previous_fifth_address(self):
        """Get the previous fifth address"""

        args = ["", "192.168.1.5", -10]
        result = _ipmath(*args)
        self.assertEqual(result, "192.168.0.251")

    def test_find_next_fifth_address_cidr(self):
        """Get the next fifth address CIDR notation"""

        args = ["", "192.168.1.1/24", 5]
        result = _ipmath(*args)
        self.assertEqual(result, "192.168.1.6")

    def test_find_previous_fifth_address_cidr(self):
        """Get the previous fifth address CIDR notation"""

        args = ["", "192.168.1.6/24", -5]
        result = _ipmath(*args)
        self.assertEqual(result, "192.168.1.1")

    def test_find_next_fifth_address_ipv6(self):
        """Get the next fifth address in ipv6"""

        args = ["", "2001::1", 10]
        result = _ipmath(*args)
        self.assertEqual(result, "2001::b")

    def test_find_previous_fifth_address_ipv6(self):
        """Get the previous fifth address in ipv6"""

        args = ["", "2001::5", -10]
        result = _ipmath(*args)
        self.assertEqual(result, "2000:ffff:ffff:ffff:ffff:ffff:ffff:fffb")

    def test_invalid_data(self):
        """Check passing invalid data"""

        args = ["", "2001::1.999.0", 10]
        kwargs = {}
        with self.assertRaises(AnsibleFilterError) as error:
            _ipmath(*args, **kwargs)
        self.assertIn("You must pass a valid IP address", str(error.exception))
