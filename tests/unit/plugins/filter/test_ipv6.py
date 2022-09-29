# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit test file for ipwrap filter plugin
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

import unittest

import pytest

from ansible.errors import AnsibleFilterError
from ansible.template import AnsibleUndefined

from ansible_collections.ansible.utils.plugins.filter.ipv6 import _ipv6


VALID_DATA = [
    "192.24.2.1",
    "::ffff:192.168.32.0/120",
    "",
    "::ffff:192.24.2.1/128",
    "192.168.32.0/24",
    "fe80::100/10",
    True,
]


VALID_OUTPUT = [
    "::ffff:192.168.32.0/120",
    "::ffff:192.24.2.1/128",
    "fe80::100/10",
]

VALID_OUTPUT1 = ["192.168.32.0/24", "192.24.2.1/32"]

VALID_OUTPUT2 = ["::ffff:192.168.32.0", "::ffff:192.24.2.1", "fe80::100"]


class TestIp6(unittest.TestCase):
    def setUp(self):
        pass

    def test_ipv6_undefined_value(self):
        """Check ipv6 filter undefined value"""
        args = ["", AnsibleUndefined(name="my_ip"), ""]
        with pytest.raises(
            AnsibleFilterError,
            match="Unrecognized type <<class 'ansible.template.AnsibleUndefined'>> for ipv6 filter <value>",
        ):
            _ipv6(*args)

    def test_ipv6_filter_empty_query(self):
        """Check ipv6 filter empty query"""
        args = ["", VALID_DATA, ""]
        result = _ipv6(*args)
        self.assertEqual(result, VALID_OUTPUT)

    def test_ipv6_ipv4_conversion(self):
        """Check ipv6 to ipv4 conversion"""
        args = ["", VALID_DATA, "ipv4"]
        result = _ipv6(*args)
        self.assertEqual(result, VALID_OUTPUT1)

    def test_ipv6_filter_address_query(self):
        """Check ipv6 filter address query"""
        args = ["", VALID_DATA, "address"]
        result = _ipv6(*args)
        self.assertEqual(result, VALID_OUTPUT2)
