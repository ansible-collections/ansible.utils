# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit test file for netaddr test plugin: in_any_network
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest import TestCase

from ansible.errors import AnsibleError

from ansible_collections.ansible.utils.plugins.test.in_any_network import _in_any_network


class TestInAnyNetwork(TestCase):
    def setUp(self):
        pass

    def test_invalid_data(self):
        """Check passing invalid argspec"""

        # invalid argument
        with self.assertRaises(AnsibleError) as error:
            _in_any_network(
                ip="10.1.1.1",
                networks={
                    "name": "networks",
                    "value": ["10.0.0.0/8", "192.168.1.0/24"],
                },
            )
        self.assertIn("unable to convert to list", str(error.exception))

    def test_valid_data(self):
        """Check passing valid data as per criteria"""

        result = _in_any_network(ip="10.1.1.1", networks=["10.0.0.0/8", "192.168.1.0/24"])
        self.assertEqual(result, True)

        result = _in_any_network(ip="8.8.8.8", networks=["10.0.0.0/8", "192.168.1.0/24"])
        self.assertEqual(result, False)
