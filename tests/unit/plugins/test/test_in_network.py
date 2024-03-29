# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit test file for netaddr test plugin: in_network
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest import TestCase

from ansible_collections.ansible.utils.plugins.test.in_network import _in_network


class TestInNetwork(TestCase):
    def setUp(self):
        pass

    def test_invalid_data(self):
        """Check passing invalid argspec"""

        # invalid argument
        with self.assertRaises(TypeError) as error:
            _in_network(ip="10.1.1.1")
        self.assertIn("argument", str(error.exception))

    def test_valid_data(self):
        """Check passing valid data as per criteria"""

        result = _in_network(ip="10.1.1.1", network="10.0.0.0/8")
        self.assertEqual(result, True)

        result = _in_network(ip="8.8.8.8", network="192.168.1.0/24")
        self.assertEqual(result, False)

        result = _in_network(ip="2001:db8:a::123", network="2001:db8:a::/64")
        self.assertEqual(result, True)

        result = _in_network(ip="2001:db8:a::123", network="10.0.0.0/8")
        self.assertEqual(result, False)
