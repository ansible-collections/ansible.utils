# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit test file for cidr_merge filter plugin
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import unittest
from ansible.errors import AnsibleFilterError
from ansible_collections.ansible.utils.plugins.filter.ipaddr import _ipaddr


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

VALID_DATA1 = ["192.168.32.0/24", "2001:db8:32c:faad::/64"]

VALID_OUTPUT = [
    "192.24.2.1",
    "::1",
    "192.168.32.0/24",
    "fe80::100/10",
    "2001:db8:32c:faad::/64",
]

VALID_OUTPUT1 = ["192.24.2.1", "::1", "fe80::100", "2001:db8:32c:faad::"]

VALID_OUTPUT2 = ["192.24.2.1/32", "::1/128", "fe80::100/10"]

VALID_OUTPUT3 = ["192.24.2.1", "2001:db8:32c:faad::/64"]

VALID_OUTPUT4 = ["192.168.32.0/24", "fe80::100/10"]

VALID_OUTPUT5 = ["192.168.32.0/24", "2001:db8:32c:faad::/64"]

VALID_OUTPUT6 = [256, 18446744073709551616]

VALID_OUTPUT7 = ["192.24.2.1", "192.168.32.0/24"]

VALID_OUTPUT8 = ["192.168.32.0/24", "2001:db8:32c:faad::/64"]

# ansible_default_ipv4 = {
#     "address": "192.168.0.11",
#     "alias": "eth0",
#     "broadcast": "192.168.0.255",
#     "gateway": "192.168.0.1",
#     "interface": "eth0",
#     "macaddress": "fa:16:3e:c4:bd:89",
#     "mtu": 1500,
#     "netmask": "255.255.255.0",
#     "network": "192.168.0.0",
#     "type": "ether"
# }

net_mask = "192.168.0.0/255.255.255.0"

host_prefix = ["2001:db8:deaf:be11::ef3/64", "192.0.2.48/24", "192.168.0.0/16"]


class TestIpAddr(unittest.TestCase):
    def setUp(self):
        pass

    def test_valid_data_empty(self):
        """Check passing invalid argspec"""

        args = ["", VALID_DATA, ""]
        result = _ipaddr(*args)
        self.assertEqual(result, VALID_OUTPUT)

    def test_valid_data_address(self):
        """Check passing invalid argspec"""

        args = ["", VALID_DATA, "address"]
        result = _ipaddr(*args)
        self.assertEqual(result, VALID_OUTPUT1)

    def test_valid_data_host(self):
        """Check passing invalid argspec"""

        args = ["", VALID_DATA, "host"]
        result = _ipaddr(*args)
        self.assertEqual(result, VALID_OUTPUT2)

    def test_valid_data_public(self):
        """Check passing invalid argspec"""

        args = ["", VALID_DATA, "public"]
        result = _ipaddr(*args)
        self.assertEqual(result, VALID_OUTPUT3)

    def test_valid_data_private(self):
        """Check passing invalid argspec"""

        args = ["", VALID_DATA, "private"]
        result = _ipaddr(*args)
        self.assertEqual(result, VALID_OUTPUT4)

    def test_valid_data_net(self):
        """Check passing invalid argspec"""

        args = ["", VALID_DATA, "net"]
        result = _ipaddr(*args)
        self.assertEqual(result, VALID_OUTPUT5)

    def test_valid_data_size(self):
        """Check passing invalid argspec"""

        args = ["", VALID_DATA1, "size"]
        result = _ipaddr(*args)
        self.assertEqual(result, VALID_OUTPUT6)

    def test_valid_data_network_range(self):
        """Check passing invalid argspec"""

        args = ["", VALID_DATA, "192.0.0.0/8"]
        result = _ipaddr(*args)
        self.assertEqual(result, VALID_OUTPUT7)

    def test_valid_data_with_index(self):
        """Check passing invalid argspec"""

        args = ["", VALID_DATA1, "0"]
        result = _ipaddr(*args)
        self.assertEqual(result, VALID_OUTPUT8)

    def test_invalid_data(self):
        """Check passing invalid argspec"""

        args = ["", VALID_DATA, "tftftf"]
        kwargs = {}
        with self.assertRaises(AnsibleFilterError) as error:
            _ipaddr(*args, **kwargs)
        self.assertIn("unknown filter type: tftftf", str(error.exception))

    def test_valid_data_with_prefix(self):
        """Check passing invalid argspec"""

        args = ["", net_mask, "prefix"]
        result = _ipaddr(*args)
        self.assertEqual(result, [24])

    def test_valid_data_with_host_prefix(self):
        """Check passing invalid argspec"""

        args = ["", host_prefix, "host/prefix"]
        result = _ipaddr(*args)
        self.assertEqual(
            result, ["2001:db8:deaf:be11::ef3/64", "192.0.2.48/24"]
        )

    def test_valid_data_with_network_prefix(self):
        """Check passing invalid argspec"""

        ipaddress = "192.168.0.11/255.255.255.0"

        args = ["", ipaddress, "network/prefix"]
        result = _ipaddr(*args)
        self.assertEqual(result, ["192.168.0.0/24"])

    def test_valid_data_with_subnet(self):
        """Check passing invalid argspec"""

        args = ["", host_prefix, "host/prefix"]
        result1 = _ipaddr(*args)

        args = ["", result1, "subnet"]
        result = _ipaddr(*args)
        self.assertEqual(result, ["2001:db8:deaf:be11::/64", "192.0.2.0/24"])
