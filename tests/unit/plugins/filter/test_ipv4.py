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

from ansible_collections.ansible.utils.plugins.filter.ipv4 import _ipv4


VALID_DATA = [
    "192.24.2.1",
    "host.fqdn",
    "::1",
    "",
    "192.168.32.0/24",
    "fe80::100/10",
    "42540766412265424405338506004571095040/64",
    True,
]


VALID_OUTPUT = ["192.24.2.1", "192.168.32.0/24"]

VALID_OUTPUT1 = ["::ffff:192.24.2.1/128", "::ffff:192.168.32.0/120"]

VALID_OUTPUT2 = ["192.24.2.1"]


class TestIp4(unittest.TestCase):
    def setUp(self):
        pass

    def test_ipv4_undefined_value(self):
        """Check ipv4 filter undefined value"""
        args = ["", AnsibleUndefined(name="my_ip"), ""]
        with pytest.raises(
            AnsibleFilterError,
            match="Unrecognized type <<class 'ansible.template.AnsibleUndefined'>> for ipv4 filter <value>",
        ):
            _ipv4(*args)

    def test_ipv4_filter_empty_query(self):
        """Check ipv4 filter empty query"""
        args = ["", VALID_DATA, ""]
        result = _ipv4(*args)
        self.assertEqual(result, VALID_OUTPUT)

    def test_ipv4_ipv6_conversion(self):
        """Check ipv4 to ipv6 conversion"""
        args = ["", VALID_DATA, "ipv6"]
        result = _ipv4(*args)
        self.assertEqual(result, VALID_OUTPUT1)

    def test_ipv4_filter_address_query(self):
        """Check ipv4 filter address query"""
        args = ["", VALID_DATA, "address"]
        result = _ipv4(*args)
        self.assertEqual(result, VALID_OUTPUT2)
