# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit test file for ipaddr filter plugins
"""
from __future__ import absolute_import, division, print_function


__metaclass__ = type

import unittest

import pytest

from ansible.errors import AnsibleFilterError
from ansible.template import AnsibleUndefined

from ansible_collections.ansible.utils.plugins.filter.cidr_merge import cidr_merge
from ansible_collections.ansible.utils.plugins.filter.ip4_hex import ip4_hex
from ansible_collections.ansible.utils.plugins.filter.ipaddr import _ipaddr
from ansible_collections.ansible.utils.plugins.filter.ipmath import ipmath
from ansible_collections.ansible.utils.plugins.filter.ipsubnet import ipsubnet
from ansible_collections.ansible.utils.plugins.filter.network_in_network import network_in_network
from ansible_collections.ansible.utils.plugins.filter.network_in_usable import network_in_usable
from ansible_collections.ansible.utils.plugins.filter.next_nth_usable import next_nth_usable
from ansible_collections.ansible.utils.plugins.filter.nthhost import nthhost
from ansible_collections.ansible.utils.plugins.filter.previous_nth_usable import previous_nth_usable
from ansible_collections.ansible.utils.plugins.filter.reduce_on_network import reduce_on_network
from ansible_collections.ansible.utils.plugins.filter.slaac import slaac
from ansible_collections.ansible.utils.plugins.plugin_utils.base.ipaddr_utils import ipaddr


netaddr = pytest.importorskip("netaddr")


class TestIpFilter(unittest.TestCase):
    def test_cidr_merge(self):
        with pytest.raises(AnsibleFilterError, match="cidr_merge: expected iterable, got None"):
            cidr_merge(None)

        with pytest.raises(AnsibleFilterError, match="cidr_merge: invalid action 'floop'"):
            cidr_merge([], "floop")

        self.assertEqual(cidr_merge([]), [])
        self.assertEqual(cidr_merge([], "span"), None)
        subnets = ["1.12.1.0/24"]
        self.assertEqual(cidr_merge(subnets), subnets)
        self.assertEqual(cidr_merge(subnets, "span"), subnets[0])
        subnets = ["1.12.1.0/25", "1.12.1.128/25"]
        self.assertEqual(cidr_merge(subnets), ["1.12.1.0/24"])
        self.assertEqual(cidr_merge(subnets, "span"), "1.12.1.0/24")
        subnets = ["1.12.1.0/25", "1.12.1.128/25", "1.12.2.0/24"]
        self.assertEqual(cidr_merge(subnets), ["1.12.1.0/24", "1.12.2.0/24"])
        self.assertEqual(cidr_merge(subnets, "span"), "1.12.0.0/22")
        subnets = ["1.12.1.1", "1.12.1.255"]
        self.assertEqual(cidr_merge(subnets), ["1.12.1.1/32", "1.12.1.255/32"])
        self.assertEqual(cidr_merge(subnets, "span"), "1.12.1.0/24")

    def test_ipaddr_undefined_value(self):
        """Check ipaddr filter undefined value"""
        args = ["", AnsibleUndefined(name="my_ip"), ""]
        with pytest.raises(
            AnsibleFilterError,
            match="Unrecognized type <<class 'ansible.template.AnsibleUndefined'>> for ipaddr filter <value>",
        ):
            _ipaddr(*args)

    def test_ipaddr_empty_query(self):
        self.assertEqual(ipaddr("192.0.2.230"), "192.0.2.230")
        self.assertEqual(ipaddr("192.0.2.230/30"), "192.0.2.230/30")
        self.assertEqual(ipaddr([]), [])

        self.assertEqual(ipaddr(True), False)
        self.assertEqual(ipaddr(""), False)

    def test_ipaddr_6to4_query(self):
        v6_address = "2002:c000:02e6::1/48"
        self.assertEqual(ipaddr("192.0.2.230", "6to4"), v6_address)
        self.assertEqual(ipaddr("192.0.2.230/24", "6to4"), v6_address)
        self.assertFalse(ipaddr("192.0.2.0/24", "6to4"))

        self.assertFalse(ipaddr("fd::e", "6to4"))
        self.assertFalse(ipaddr("fd::e/20", "6to4"))

        self.assertEqual(ipaddr("2002:c000:02e6::1", "6to4"), "2002:c000:02e6::1")
        self.assertEqual(ipaddr(v6_address, "6to4"), v6_address)
        self.assertEqual(
            ipaddr(
                ["192.0.2.230", "192.0.2.0/24", "fd::e", "2002:c000:02e6::1"],
                "6to4",
            ),
            [v6_address, "2002:c000:02e6::1"],
        )

    def test_ipaddr_address_query(self):
        self.assertEqual(ipaddr("192.0.2.230", "address"), "192.0.2.230")
        self.assertEqual(ipaddr("192.0.2.230/24", "address"), "192.0.2.230")
        self.assertIsNone(ipaddr("192.0.2.0/24", "address"))
        self.assertEqual(ipaddr("192.0.2.0/31", "address"), "192.0.2.0")
        self.assertEqual(ipaddr("2001::1", "address"), "2001::1")
        self.assertEqual(ipaddr("2001::1/48", "address"), "2001::1")
        self.assertEqual(ipaddr("2001::", "address"), "2001::")
        self.assertEqual(ipaddr("2001::/48", "address"), "2001::")

    def test_ipaddr_bool_query(self):
        self.assertTrue(ipaddr("192.0.2.20", "bool"))
        self.assertFalse(ipaddr("192.900.2.20", "bool"))

    def test_netmask(self):
        address = "1.1.1.1/24"
        self.assertEqual(ipaddr(address, "netmask"), "255.255.255.0")
        address = "1.1.1.1/25"
        self.assertEqual(ipaddr(address, "netmask"), "255.255.255.128")
        address = "1.12.1.34/32"
        self.assertEqual(ipaddr(address, "netmask"), "255.255.255.255")

    def test_network(self):
        address = "1.12.1.34/32"
        self.assertEqual(ipaddr(address, "network"), "1.12.1.34")
        address = "1.12.1.34/255.255.255.255"
        self.assertEqual(ipaddr(address, "network"), "1.12.1.34")
        address = "1.12.1.34"
        self.assertEqual(ipaddr(address, "network"), "1.12.1.34")
        address = "1.12.1.35/31"
        self.assertEqual(ipaddr(address, "network"), "1.12.1.34")
        address = "1.12.1.34/24"
        self.assertEqual(ipaddr(address, "network"), "1.12.1.0")

    def test_broadcast(self):
        address = "1.12.1.34/24"
        self.assertEqual(ipaddr(address, "broadcast"), "1.12.1.255")
        address = "1.12.1.34/16"
        self.assertEqual(ipaddr(address, "broadcast"), "1.12.255.255")
        address = "1.12.1.34/27"
        self.assertEqual(ipaddr(address, "broadcast"), "1.12.1.63")
        address = "1.12.1.34/32"
        self.assertEqual(ipaddr(address, "broadcast"), None)
        address = "1.12.1.35/31"
        self.assertEqual(ipaddr(address, "broadcast"), None)

    def test_first_usable(self):
        with pytest.raises(AnsibleFilterError, match="Not a network address"):
            ipaddr("1.12.1.34", "first_usable")

        address = "1.12.1.0/24"
        self.assertEqual(ipaddr(address, "first_usable"), "1.12.1.1")
        address = "1.12.1.36/24"
        self.assertEqual(ipaddr(address, "first_usable"), "1.12.1.1")
        address = "1.12.1.36/28"
        self.assertEqual(ipaddr(address, "first_usable"), "1.12.1.33")
        address = "1.12.1.36/255.255.255.240"
        self.assertEqual(ipaddr(address, "first_usable"), "1.12.1.33")
        address = "1.12.1.36/31"
        self.assertEqual(ipaddr(address, "first_usable"), "1.12.1.36")
        address = "1.12.1.37/31"
        self.assertEqual(ipaddr(address, "first_usable"), "1.12.1.36")
        address = "1.12.1.36/32"
        self.assertEqual(ipaddr(address, "first_usable"), None)

    def test_host_query(self):
        self.assertEqual(ipaddr("192.0.2.1", "host"), "192.0.2.1/32")
        address = "192.0.2.12/20"
        self.assertEqual(ipaddr(address, "host"), address)
        address = "192.0.2.0/31"
        self.assertEqual(ipaddr(address, "host"), address)
        self.assertIsNone(ipaddr("192.0.2.0/24", "host"))

    def test_last_usable(self):
        with pytest.raises(AnsibleFilterError, match="Not a network address"):
            ipaddr("1.12.1.34", "last_usable")

        address = "1.12.1.0/24"
        self.assertEqual(ipaddr(address, "last_usable"), "1.12.1.254")
        address = "1.12.1.36/24"
        self.assertEqual(ipaddr(address, "last_usable"), "1.12.1.254")
        address = "1.12.1.36/28"
        self.assertEqual(ipaddr(address, "last_usable"), "1.12.1.46")
        address = "1.12.1.36/255.255.255.240"
        self.assertEqual(ipaddr(address, "last_usable"), "1.12.1.46")
        address = "1.12.1.36/31"
        self.assertEqual(ipaddr(address, "last_usable"), "1.12.1.37")
        address = "1.12.1.37/31"
        self.assertEqual(ipaddr(address, "last_usable"), "1.12.1.37")
        address = "1.12.1.36/32"
        self.assertEqual(ipaddr(address, "last_usable"), None)

    def test_wildcard(self):
        address = "1.12.1.0/24"
        self.assertEqual(ipaddr(address, "wildcard"), "0.0.0.255")
        address = "1.12.1.0/25"
        self.assertEqual(ipaddr(address, "wildcard"), "0.0.0.127")
        address = "1.12.1.36/28"
        self.assertEqual(ipaddr(address, "wildcard"), "0.0.0.15")
        address = "1.12.1.36/255.255.255.240"
        self.assertEqual(ipaddr(address, "wildcard"), "0.0.0.15")
        address = "1.12.1.36/31"
        self.assertEqual(ipaddr(address, "wildcard"), "0.0.0.1")
        address = "1.12.1.37/31"
        self.assertEqual(ipaddr(address, "wildcard"), "0.0.0.1")
        address = "1.12.1.36/32"
        self.assertEqual(ipaddr(address, "wildcard"), "0.0.0.0")
        address = "1.12.1.254/24"
        self.assertEqual(ipaddr(address, "wildcard"), "0.0.0.255")

    def test_size_usable(self):
        address = "1.12.1.0/24"
        self.assertEqual(ipaddr(address, "size_usable"), 254)
        address = "1.12.1.0/25"
        self.assertEqual(ipaddr(address, "size_usable"), 126)
        address = "1.12.1.36/28"
        self.assertEqual(ipaddr(address, "size_usable"), 14)
        address = "1.12.1.36/255.255.255.240"
        self.assertEqual(ipaddr(address, "size_usable"), 14)
        address = "1.12.1.36/31"
        self.assertEqual(ipaddr(address, "size_usable"), 2)
        address = "1.12.1.37/31"
        self.assertEqual(ipaddr(address, "size_usable"), 2)
        address = "1.12.1.36/32"
        self.assertEqual(ipaddr(address, "size_usable"), 0)
        address = "1.12.1.254/24"
        self.assertEqual(ipaddr(address, "size_usable"), 254)

    def test_ipaddr_public_query(self):
        self.assertIsNone(ipaddr("192.168.1.12", "public"))
        self.assertIsNone(ipaddr("127.0.1.25", "public"))
        self.assertIsNone(ipaddr("255.255.240.0", "public"))
        self.assertEqual(ipaddr("76.120.99.190", "public"), "76.120.99.190")
        self.assertEqual(
            ipaddr(["192.168.1.12", "127.0.1.25", "255.255.240.0"], "public"),
            [],
        )
        self.assertEqual(
            ipaddr(
                [
                    "192.168.1.12",
                    "127.0.1.25",
                    "255.255.240.0",
                    "76.120.99.190",
                ],
                "public",
            ),
            ["76.120.99.190"],
        )

    def test_range_usable(self):
        address = "1.12.1.0/24"
        self.assertEqual(ipaddr(address, "range_usable"), "1.12.1.1-1.12.1.254")
        address = "1.12.1.0/25"
        self.assertEqual(ipaddr(address, "range_usable"), "1.12.1.1-1.12.1.126")
        address = "1.12.1.36/28"
        self.assertEqual(ipaddr(address, "range_usable"), "1.12.1.33-1.12.1.46")
        address = "1.12.1.36/255.255.255.240"
        self.assertEqual(ipaddr(address, "range_usable"), "1.12.1.33-1.12.1.46")
        address = "1.12.1.36/31"
        self.assertEqual(ipaddr(address, "range_usable"), "1.12.1.36-1.12.1.37")
        address = "1.12.1.37/31"
        self.assertEqual(ipaddr(address, "range_usable"), "1.12.1.36-1.12.1.37")
        address = "1.12.1.36/32"
        self.assertEqual(ipaddr(address, "range_usable"), None)
        address = "1.12.1.254/24"
        self.assertEqual(ipaddr(address, "range_usable"), "1.12.1.1-1.12.1.254")

    def test_address_prefix(self):
        # Regular address
        address = "1.12.1.12/24"
        self.assertEqual(ipaddr(address, "address/prefix"), address)

        # Network address - invalid
        address = "1.12.1.0/24"
        self.assertFalse(ipaddr(address, "address/prefix"))
        # But valid in a /31
        address = "1.12.1.0/31"
        self.assertEqual(ipaddr(address, "address/prefix"), address)

        # Broadcast address - invalid
        address = "1.12.1.255/24"
        self.assertFalse(ipaddr(address, "address/prefix"))
        # But valid in a /31
        address = "1.12.1.255/31"
        self.assertEqual(ipaddr(address, "address/prefix"), address)

        # /32 - always valid?
        address = "1.12.1.0/32"
        self.assertEqual(ipaddr(address, "address/prefix"), address)
        address = "1.12.1.12/32"
        self.assertEqual(ipaddr(address, "address/prefix"), address)
        address = "1.12.1.255/32"
        self.assertEqual(ipaddr(address, "address/prefix"), address)

        # No prefix means /32
        address = "1.12.1.34"
        self.assertEqual(ipaddr(address, "address/prefix"), "1.12.1.34/32")

        # Hostmask also works
        address = "1.12.1.36/255.255.255.240"
        self.assertEqual(ipaddr(address, "address/prefix"), "1.12.1.36/28")
        # But not hostmasks that don't make a valid CIDR prefix
        address = "1.12.1.36/255.255.255.88"
        self.assertFalse(ipaddr(address, "address/prefix"))

    def test_ip_prefix(self):
        address = "1.12.1.0/24"
        self.assertEqual(ipaddr(address, "ip/prefix"), None)
        address = "1.12.1.0/25"
        self.assertEqual(ipaddr(address, "ip/prefix"), None)
        address = "1.12.1.36/28"
        self.assertEqual(ipaddr(address, "ip/prefix"), "1.12.1.36/28")
        address = "1.12.1.36/255.255.255.240"
        self.assertEqual(ipaddr(address, "ip/prefix"), "1.12.1.36/28")
        address = "1.12.1.36/31"
        self.assertEqual(ipaddr(address, "ip/prefix"), "1.12.1.36/31")
        address = "1.12.1.37/31"
        self.assertEqual(ipaddr(address, "ip/prefix"), "1.12.1.37/31")
        address = "1.12.1.36/32"
        self.assertEqual(ipaddr(address, "ip/prefix"), None)
        address = "1.12.1.254/24"
        self.assertEqual(ipaddr(address, "ip/prefix"), "1.12.1.254/24")

    def test_ip_netmask(self):
        address = "1.12.1.0/24"
        self.assertEqual(ipaddr(address, "ip_netmask"), None)
        address = "1.12.1.0/25"
        self.assertEqual(ipaddr(address, "ip_netmask"), None)
        address = "1.12.1.36/28"
        self.assertEqual(ipaddr(address, "ip_netmask"), "1.12.1.36 255.255.255.240")
        address = "1.12.1.36/255.255.255.240"
        self.assertEqual(ipaddr(address, "ip_netmask"), "1.12.1.36 255.255.255.240")
        address = "1.12.1.36/31"
        self.assertEqual(ipaddr(address, "ip_netmask"), "1.12.1.36 255.255.255.254")
        address = "1.12.1.37/31"
        self.assertEqual(ipaddr(address, "ip_netmask"), "1.12.1.37 255.255.255.254")
        address = "1.12.1.36/32"
        self.assertEqual(ipaddr(address, "ip_netmask"), None)
        address = "1.12.1.254/24"
        self.assertEqual(ipaddr(address, "ip_netmask"), "1.12.1.254 255.255.255.0")

    def test_ipv6_query(self):
        self.assertEqual(ipaddr("fd00:123::97", "ipv6"), "fd00:123::97")
        self.assertEqual(ipaddr("192.0.2.230", "ipv6"), "::ffff:192.0.2.230/128")

    def test_ipaddr_link_local_query(self):
        self.assertEqual(ipaddr("169.254.0.12", "link-local"), "169.254.0.12")
        self.assertIsNone(ipaddr("192.0.2.12", "link-local"))
        self.assertEqual(ipaddr("fe80::9", "link-local"), "fe80::9")
        self.assertIsNone(ipaddr("2001::", "link-local"))

    def test_network_id(self):
        address = "1.12.1.0/24"
        self.assertEqual(ipaddr(address, "network_id"), "1.12.1.0")
        address = "1.12.1.0/25"
        self.assertEqual(ipaddr(address, "network_id"), "1.12.1.0")
        address = "1.12.1.36/28"
        self.assertEqual(ipaddr(address, "network_id"), "1.12.1.32")
        address = "1.12.1.36/255.255.255.240"
        self.assertEqual(ipaddr(address, "network_id"), "1.12.1.32")
        address = "1.12.1.36/31"
        self.assertEqual(ipaddr(address, "network_id"), "1.12.1.36")
        address = "1.12.1.37/31"
        self.assertEqual(ipaddr(address, "network_id"), "1.12.1.36")
        address = "1.12.1.36/32"
        self.assertEqual(ipaddr(address, "network_id"), "1.12.1.36")
        address = "1.12.1.254/24"
        self.assertEqual(ipaddr(address, "network_id"), "1.12.1.0")

    def test_network_prefix(self):
        address = "1.12.1.0/24"
        self.assertEqual(ipaddr(address, "network/prefix"), "1.12.1.0/24")
        address = "1.12.1.0/25"
        self.assertEqual(ipaddr(address, "network/prefix"), "1.12.1.0/25")
        address = "1.12.1.36/28"
        self.assertEqual(ipaddr(address, "network/prefix"), "1.12.1.32/28")
        address = "1.12.1.36/255.255.255.240"
        self.assertEqual(ipaddr(address, "network/prefix"), "1.12.1.32/28")
        address = "1.12.1.36/31"
        self.assertEqual(ipaddr(address, "network/prefix"), "1.12.1.36/31")
        address = "1.12.1.37/31"
        self.assertEqual(ipaddr(address, "network/prefix"), "1.12.1.36/31")
        address = "1.12.1.36/32"
        self.assertEqual(ipaddr(address, "network/prefix"), "1.12.1.36/32")
        address = "1.12.1.254/24"
        self.assertEqual(ipaddr(address, "network/prefix"), "1.12.1.0/24")

    def test_network_netmask(self):
        address = "1.12.1.0/24"
        self.assertEqual(ipaddr(address, "network_netmask"), "1.12.1.0 255.255.255.0")
        address = "1.12.1.0/25"
        self.assertEqual(ipaddr(address, "network_netmask"), "1.12.1.0 255.255.255.128")
        address = "1.12.1.36/28"
        self.assertEqual(ipaddr(address, "network_netmask"), "1.12.1.32 255.255.255.240")
        address = "1.12.1.36/255.255.255.240"
        self.assertEqual(ipaddr(address, "network_netmask"), "1.12.1.32 255.255.255.240")
        address = "1.12.1.36/31"
        self.assertEqual(ipaddr(address, "network_netmask"), "1.12.1.36 255.255.255.254")
        address = "1.12.1.37/31"
        self.assertEqual(ipaddr(address, "network_netmask"), "1.12.1.36 255.255.255.254")
        address = "1.12.1.36/32"
        self.assertEqual(ipaddr(address, "network_netmask"), "1.12.1.36 255.255.255.255")
        address = "1.12.1.254/24"
        self.assertEqual(ipaddr(address, "network_netmask"), "1.12.1.0 255.255.255.0")

    def test_network_wildcard(self):
        address = "1.12.1.0/24"
        self.assertEqual(ipaddr(address, "network_wildcard"), "1.12.1.0 0.0.0.255")
        address = "1.12.1.0/25"
        self.assertEqual(ipaddr(address, "network_wildcard"), "1.12.1.0 0.0.0.127")
        address = "1.12.1.36/28"
        self.assertEqual(ipaddr(address, "network_wildcard"), "1.12.1.32 0.0.0.15")
        address = "1.12.1.36/255.255.255.240"
        self.assertEqual(ipaddr(address, "network_wildcard"), "1.12.1.32 0.0.0.15")
        address = "1.12.1.36/31"
        self.assertEqual(ipaddr(address, "network_wildcard"), "1.12.1.36 0.0.0.1")
        address = "1.12.1.37/31"
        self.assertEqual(ipaddr(address, "network_wildcard"), "1.12.1.36 0.0.0.1")
        address = "1.12.1.36/32"
        self.assertEqual(ipaddr(address, "network_wildcard"), "1.12.1.36 0.0.0.0")
        address = "1.12.1.254/24"
        self.assertEqual(ipaddr(address, "network_wildcard"), "1.12.1.0 0.0.0.255")

    def test_next_usable(self):
        address = "1.12.1.0/24"
        self.assertEqual(ipaddr(address, "next_usable"), "1.12.1.1")
        address = "1.12.1.36/24"
        self.assertEqual(ipaddr(address, "next_usable"), "1.12.1.37")
        address = "1.12.1.36/28"
        self.assertEqual(ipaddr(address, "next_usable"), "1.12.1.37")
        address = "1.12.1.36/255.255.255.240"
        self.assertEqual(ipaddr(address, "next_usable"), "1.12.1.37")
        address = "1.12.1.36/31"
        self.assertEqual(ipaddr(address, "next_usable"), "1.12.1.37")
        address = "1.12.1.37/31"
        self.assertEqual(ipaddr(address, "next_usable"), None)
        address = "1.12.1.36/32"
        self.assertEqual(ipaddr(address, "next_usable"), None)
        address = "1.12.1.254/24"
        self.assertEqual(ipaddr(address, "next_usable"), None)

    def test_peer(self):
        address = "1.12.1.0/31"
        self.assertEqual(ipaddr(address, "peer"), "1.12.1.1")
        address = "1.12.1.1/31"
        self.assertEqual(ipaddr(address, "peer"), "1.12.1.0")
        address = "1.12.1.1/30"
        self.assertEqual(ipaddr(address, "peer"), "1.12.1.2")
        address = "1.12.1.2/30"
        self.assertEqual(ipaddr(address, "peer"), "1.12.1.1")
        with self.assertRaises(AnsibleFilterError):
            address = "1.12.1.34"
            ipaddr(address, "peer")
        with self.assertRaises(AnsibleFilterError):
            address = "1.12.1.33/29"
            ipaddr(address, "peer")
        with self.assertRaises(AnsibleFilterError):
            address = "1.12.1.32/30"
            ipaddr(address, "peer")
        with self.assertRaises(AnsibleFilterError):
            address = "1.12.1.35/30"
            ipaddr(address, "peer")
        with self.assertRaises(AnsibleFilterError):
            address = "1.12.1.34/32"
            ipaddr(address, "peer")

    def test_previous_usable(self):
        address = "1.12.1.0/24"
        self.assertEqual(ipaddr(address, "previous_usable"), None)
        address = "1.12.1.36/24"
        self.assertEqual(ipaddr(address, "previous_usable"), "1.12.1.35")
        address = "1.12.1.36/28"
        self.assertEqual(ipaddr(address, "previous_usable"), "1.12.1.35")
        address = "1.12.1.36/255.255.255.240"
        self.assertEqual(ipaddr(address, "previous_usable"), "1.12.1.35")
        address = "1.12.1.36/31"
        self.assertEqual(ipaddr(address, "previous_usable"), None)
        address = "1.12.1.37/31"
        self.assertEqual(ipaddr(address, "previous_usable"), "1.12.1.36")
        address = "1.12.1.36/32"
        self.assertEqual(ipaddr(address, "previous_usable"), None)
        address = "1.12.1.254/24"
        self.assertEqual(ipaddr(address, "previous_usable"), "1.12.1.253")

    def test_ipmath(self):
        self.assertEqual(ipmath("192.168.1.5", 5), "192.168.1.10")
        self.assertEqual(ipmath("192.168.1.5", -5), "192.168.1.0")
        self.assertEqual(ipmath("192.168.0.5", -10), "192.167.255.251")

        self.assertEqual(ipmath("192.168.1.1/24", 5), "192.168.1.6")
        self.assertEqual(ipmath("192.168.1.6/24", -5), "192.168.1.1")
        self.assertEqual(ipmath("192.168.2.6/24", -10), "192.168.1.252")

        self.assertEqual(ipmath("2001::1", 8), "2001::9")
        self.assertEqual(ipmath("2001::1", 9), "2001::a")
        self.assertEqual(ipmath("2001::1", 10), "2001::b")
        self.assertEqual(ipmath("2001::5", -3), "2001::2")
        self.assertEqual(ipmath("2001::5", -10), "2000:ffff:ffff:ffff:ffff:ffff:ffff:fffb")

        expected = "You must pass a valid IP address; invalid_ip is invalid"
        with self.assertRaises(AnsibleFilterError) as exc:
            ipmath("invalid_ip", 8)
        self.assertEqual(exc.exception.message, expected)

        expected = "You must pass an integer for arithmetic; some_number is not a valid integer"
        with self.assertRaises(AnsibleFilterError) as exc:
            ipmath("1.2.3.4", "some_number")
        self.assertEqual(exc.exception.message, expected)

    def test_ipsubnet(self):
        test_cases = (
            (("1.1.1.1/24", "30"), "64"),
            (("1.12.1.34/32", "1.12.1.34/24"), "35"),
            (("192.168.50.0/24", "192.168.0.0/16"), "51"),
            (("192.168.144.5", "192.168.0.0/16"), "36870"),
            (("192.168.144.5", "192.168.144.5/24"), "6"),
            (("192.168.144.5/32", "192.168.144.0/24"), "6"),
            (("192.168.144.16/30", "192.168.144.0/24"), "5"),
            (("192.168.144.5",), "192.168.144.5/32"),
            (("192.168.0.0/16",), "192.168.0.0/16"),
            (("192.168.144.5",), "192.168.144.5/32"),
            (("192.168.0.0/16", "20"), "16"),
            (("192.168.0.0/16", "20", "0"), "192.168.0.0/20"),
            (("192.168.0.0/16", "20", "-1"), "192.168.240.0/20"),
            (("192.168.0.0/16", "20", "5"), "192.168.80.0/20"),
            (("192.168.0.0/16", "20", "-5"), "192.168.176.0/20"),
            (("192.168.144.5", "20"), "192.168.144.0/20"),
            (("192.168.144.5", "18", "0"), "192.168.128.0/18"),
            (("192.168.144.5", "18", "-1"), "192.168.144.4/31"),
            (("192.168.144.5", "18", "5"), "192.168.144.0/23"),
            (("192.168.144.5", "18", "-5"), "192.168.144.0/27"),
            (("span", "test", "error"), False),
            (("test",), False),
            (("192.168.144.5", "500000", "-5"), False),
            (("192.168.144.5", "18", "500000"), False),
            (("200000", "18", "-5"), "0.3.13.64/27"),
        )
        for args, res in test_cases:
            self._test_ipsubnet(args, res)

    def _test_ipsubnet(self, ipsubnet_args, expected_result):
        self.assertEqual(ipsubnet(*ipsubnet_args), expected_result)

        expected = "Requested subnet size of 24 is invalid"
        with self.assertRaises(AnsibleFilterError) as exc:
            ipsubnet("1.1.1.1/25", "24")
        self.assertEqual(exc.exception.message, expected)

        with self.assertRaisesRegexp(
            AnsibleFilterError,
            "You must pass a valid subnet or IP address; invalid_subnet is invalid",
        ):
            ipsubnet("192.168.144.5", "invalid_subnet")

        with self.assertRaisesRegexp(
            AnsibleFilterError,
            "192.168.144.0/30 is not in the subnet 192.168.144.4/30",
        ):
            ipsubnet("192.168.144.1/30", "192.168.144.5/30")

    def test_nthhost(self):
        address = "1.12.1.0/24"
        self.assertFalse(nthhost(address))
        self.assertEqual(nthhost(address, 5), "1.12.1.5")
        address = "1.12.1.36/24"
        self.assertEqual(nthhost(address, 10), "1.12.1.10")
        address = "1.12.1.34"
        self.assertFalse(nthhost(address, "last_usable"), "Not a network address")
        address = "1.12.1.36/28"
        self.assertEqual(nthhost(address, 4), "1.12.1.36")
        address = "1.12.1.36/255.255.255.240"
        self.assertEqual(nthhost(address, 4), "1.12.1.36")
        address = "1.12.1.36/31"
        self.assertEqual(nthhost(address, 1), "1.12.1.37")
        address = "1.12.1.37/31"
        self.assertEqual(nthhost(address, 1), "1.12.1.37")
        address = "1.12.1.36/32"
        self.assertFalse(nthhost(address, 1))
        address = "1.12.1.254/24"
        self.assertEqual(nthhost(address, 2), "1.12.1.2")

    def test_next_nth_usable(self):
        address = "1.12.1.0/24"
        self.assertEqual(next_nth_usable(address, 5), "1.12.1.5")
        address = "1.12.1.36/24"
        self.assertEqual(next_nth_usable(address, 10), "1.12.1.46")
        address = "1.12.1.36/28"
        self.assertEqual(next_nth_usable(address, 4), "1.12.1.40")
        address = "1.12.1.36/255.255.255.240"
        self.assertEqual(next_nth_usable(address, 4), "1.12.1.40")
        address = "1.12.1.36/31"
        self.assertEqual(next_nth_usable(address, 1), "1.12.1.37")
        address = "1.12.1.37/31"
        self.assertEqual(next_nth_usable(address, 1), None)
        address = "1.12.1.36/32"
        self.assertEqual(next_nth_usable(address, 1), None)
        address = "1.12.1.254/24"
        self.assertEqual(next_nth_usable(address, 2), None)

    def test_previous_nth_usable(self):
        address = "1.12.1.0/24"
        self.assertEqual(previous_nth_usable(address, 5), None)
        address = "1.12.1.36/24"
        self.assertEqual(previous_nth_usable(address, 10), "1.12.1.26")
        address = "1.12.1.36/28"
        self.assertEqual(previous_nth_usable(address, 2), "1.12.1.34")
        address = "1.12.1.36/255.255.255.240"
        self.assertEqual(previous_nth_usable(address, 2), "1.12.1.34")
        address = "1.12.1.36/31"
        self.assertEqual(previous_nth_usable(address, 1), None)
        address = "1.12.1.37/31"
        self.assertEqual(previous_nth_usable(address, 1), "1.12.1.36")
        address = "1.12.1.36/32"
        self.assertEqual(previous_nth_usable(address, 1), None)
        address = "1.12.1.254/24"
        self.assertEqual(previous_nth_usable(address, 2), "1.12.1.252")

    def test_network_in_usable(self):
        subnet = "1.12.1.0/24"
        address = "1.12.1.10"
        self.assertEqual(network_in_usable(subnet, address), True)
        subnet = "1.12.1.0/24"
        address = "1.12.0.10"
        self.assertEqual(network_in_usable(subnet, address), False)
        subnet = "1.12.1.32/28"
        address = "1.12.1.36"
        self.assertEqual(network_in_usable(subnet, address), True)
        subnet = "1.12.1.32/28"
        address = "1.12.1.36/31"
        self.assertEqual(network_in_usable(subnet, address), True)
        subnet = "1.12.1.32/28"
        address = "1.12.1.48/31"
        self.assertEqual(network_in_usable(subnet, address), False)
        subnet = "1.12.1.32/255.255.255.240"
        address = "1.12.1.31"
        self.assertEqual(network_in_usable(subnet, address), False)
        subnet = "1.12.1.36/31"
        address = "1.12.1.36"
        self.assertEqual(network_in_usable(subnet, address), True)
        subnet = "1.12.1.37/31"
        address = "1.12.1.35"
        self.assertEqual(network_in_usable(subnet, address), False)
        subnet = "1.12.1.36/32"
        address = "1.12.1.36"
        self.assertEqual(network_in_usable(subnet, address), True)
        subnet = "1.12.1.0/24"
        address = "1.12.2.0"
        self.assertEqual(network_in_usable(subnet, address), False)

    def test_network_in_network(self):
        subnet = "1.12.1.0/24"
        address = "1.12.1.0"
        self.assertEqual(network_in_network(subnet, address), True)
        subnet = "1.12.1.0/24"
        address = "1.12.0.10"
        self.assertEqual(network_in_network(subnet, address), False)
        subnet = "1.12.1.32/28"
        address = "1.12.1.32/28"
        self.assertEqual(network_in_network(subnet, address), True)
        subnet = "1.12.1.32/28"
        address = "1.12.1.47"
        self.assertEqual(network_in_network(subnet, address), True)
        subnet = "1.12.1.32/28"
        address = "1.12.1.48/31"
        self.assertEqual(network_in_network(subnet, address), False)
        subnet = "1.12.1.32/255.255.255.240"
        address = "1.12.1.31"
        self.assertEqual(network_in_network(subnet, address), False)
        subnet = "1.12.1.36/31"
        address = "1.12.1.36"
        self.assertEqual(network_in_network(subnet, address), True)
        subnet = "1.12.1.37/31"
        address = "1.12.1.35"
        self.assertEqual(network_in_network(subnet, address), False)
        subnet = "1.12.1.36/32"
        address = "1.12.1.36"
        self.assertEqual(network_in_network(subnet, address), True)
        subnet = "1.12.1.0/24"
        address = "1.12.2.0"
        self.assertEqual(network_in_network(subnet, address), False)

    def test_reduce_on_network(self):
        subnet = "1.12.1.0/28"
        addresses = ["1.12.1.0", "1.12.0.10"]
        self.assertEqual(reduce_on_network(addresses, subnet), [addresses[0]])
        addresses = ["1.12.2.0", "1.12.1.236"]
        self.assertEqual(reduce_on_network(addresses, subnet), [])

        subnet = "1.12.1.32/28"
        addresses = ["1.12.1.32/28", "1.12.1.47", "1.12.1.48/31"]
        self.assertEqual(reduce_on_network(addresses, subnet), addresses[:-1])

        subnet = "1.12.1.36/32"
        addresses = ["1.12.1.31", "1.12.1.36", "1.12.1.35", "1.12.1.40"]
        self.assertEqual(reduce_on_network(addresses, subnet), [addresses[1]])
        subnet = "1.12.1.32/255.255.255.240"
        self.assertEqual(reduce_on_network(addresses, subnet), addresses[1:])

    def test_slaac(self):
        mac = "00:50:b6:aa:99:e2"
        self.assertFalse(slaac("192.168.1.20", mac))
        self.assertFalse(slaac("fd::9"))
        self.assertFalse(slaac("floop"))

        self.assertEqual(slaac("fd::9", mac), "fd::250:b6ff:feaa:99eb")
        self.assertEqual(
            slaac("fd00:1234:5678:9abc:def0::/20", mac),
            "fd00:1000::250:b6ff:feaa:99e2",
        )

    def test_ip4_hex(self):
        self.assertEqual(ip4_hex("192.0.2.24"), "c0000218")
        self.assertEqual(ip4_hex("192.0.2.24", "."), "c0.00.02.18")
