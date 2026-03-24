# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for ipaddress_utils helpers.
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest import TestCase

from ansible_collections.ansible.utils.plugins.plugin_utils.base.ipaddress_utils import (
    _is_subnet_of,
    ip_network,
)


class TestIsSubnetOf(TestCase):
    def test_ipv4_subnet_true(self):
        a = ip_network("10.1.1.0/24")
        b = ip_network("10.0.0.0/8")
        self.assertTrue(_is_subnet_of(a, b))

    def test_ipv4_subnet_false_disjoint(self):
        a = ip_network("192.168.1.0/24")
        b = ip_network("10.0.0.0/8")
        self.assertFalse(_is_subnet_of(a, b))

    def test_ipv4_subnet_false_reverse(self):
        a = ip_network("10.0.0.0/8")
        b = ip_network("10.1.1.0/24")
        self.assertFalse(_is_subnet_of(a, b))

    def test_ipv4_same_network(self):
        n = ip_network("10.0.0.0/8")
        self.assertTrue(_is_subnet_of(n, n))

    def test_ipv6_subnet_true(self):
        a = ip_network("2001:db8:0:1::/64")
        b = ip_network("2001:db8::/48")
        self.assertTrue(_is_subnet_of(a, b))

    def test_ipv6_subnet_false(self):
        a = ip_network("2001:db8:2::/64")
        b = ip_network("2001:db8:1::/48")
        self.assertFalse(_is_subnet_of(a, b))

    def test_mixed_ip_versions(self):
        a = ip_network("10.0.0.0/8")
        b = ip_network("2001:db8::/32")
        self.assertFalse(_is_subnet_of(a, b))

    def test_invalid_arguments_return_false(self):
        self.assertFalse(_is_subnet_of(None, ip_network("10.0.0.0/8")))
        self.assertFalse(_is_subnet_of(ip_network("10.0.0.0/8"), None))
