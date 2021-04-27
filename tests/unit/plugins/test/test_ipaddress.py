# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The test plugin file for netaddr tests
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import unittest  # TestCase, assertTrue
import ansible_collections.ansible.utils.plugins.test.ipaddress_tests as ipaddress
from ansible.template import Templar

TESTS = [
    # "{{ '10.1.1.1' is ansible.utils.in_network '10.0.0.0/8' }}",
    # "{{ '10.1.1.1' is not ansible.utils.in_network '192.168.1.0/24' }}",
    # "{{ '2001:db8:a::123' is ansible.utils.in_network '2001:db8:a::/64' }}",
    # "{{ '2001:db8:a::123' is not ansible.utils.in_network '10.0.0.0/8' }}",
    # "{{ '2001:db8:a::123' is not ansible.utils.in_network 'string' }}",
    # "{{ '10.1.1.1' is ansible.utils.in_one_network ['10.0.0.0/8', '192.168.1.0/24'] }}",
    # "{{ '10.1.1.1' is not ansible.utils.in_one_network ['10.0.0.0/8', '10.1.1.0/24'] }}",
    # "{{ '10.1.1.1' is ansible.utils.in_any_network ['10.0.0.0/8', '192.168.1.0/24'] }}",
    # "{{ '8.8.8.8' is not ansible.utils.in_any_network ['10.0.0.0/8', '192.168.1.0/24', '172.16.0.0/16'] }}",
    # "{{ '10.1.1.1' is ansible.utils.ip }}",
    # "{{ 'string' is not ansible.utils.ip }}",
    # "{{ '300.1.1.1' is not ansible.utils.ip }}",
    # "{{ '10.1.1.1' is ansible.utils.ip_address }}",
    # "{{ 'string' is not ansible.utils.ip_address }}",
    # "{{ '10.0.0.0/8' is not ansible.utils.ip_address }}",
    # "{{ '10.1.1.1' is ansible.utils.ipv4 }}",
    # "{{ 'fe80::216:3eff:fee4:16f3' is not ansible.utils.ipv4 }}",
    # "{{ '10.1.1.1' is ansible.utils.ipv4_address }}",
    # "{{ '10.1.1.1/31' is not ansible.utils.ipv4_address }}",
    # "{{ '0.1.255.255' is ansible.utils.ipv4_hostmask }}",
    # "{{ '255.255.255.0' is not ansible.utils.ipv4_hostmask }}",
    # "{{ '255.255.255.0' is ansible.utils.ipv4_netmask }}",
    # "{{ '255.255.255.128' is ansible.utils.ipv4_netmask }}",
    # "{{ '255.255.255.127' is not ansible.utils.ipv4_netmask }}",
    # "{{ 'fe80::216:3eff:fee4:16f3' is ansible.utils.ipv6 }}",
    # "{{ '2001:db8:a::/64' is ansible.utils.ipv6 }}",
    # "{{ 'fe80::216:3eff:fee4:16f3' is ansible.utils.ipv6_address }}",
    # "{{ '2001:db8:a::123/64' is not ansible.utils.ipv6_address }}",
    # "{{ '::FFFF:10.1.1.1' is ansible.utils.ipv6_ipv4_mapped }}",
    # "{{ '::AAAA:10.1.1.1' is not ansible.utils.ipv6_ipv4_mapped }}",
    # "{{ 'string' is not ansible.utils.ipv6_ipv4_mapped }}",
    # "{{ '2002:c0a8:6301:1::1' is ansible.utils.ipv6_sixtofour }}",
    # "{{ '2001:c0a8:6301:1::1' is not ansible.utils.ipv6_sixtofour }}",
    # "{{ 'string' is not ansible.utils.ipv6_sixtofour }}",
    # "{{ '2001::c0a8:6301:1' is ansible.utils.ipv6_teredo }}",
    # "{{ '2002::c0a8:6301:1' is not ansible.utils.ipv6_teredo }}",
    # "{{ 'string' is not ansible.utils.ipv6_teredo }}",
    # "{{ '127.10.10.10' is ansible.utils.loopback }}",
    # "{{ '10.1.1.1' is not ansible.utils.loopback }}",
    # "{{ '::1' is ansible.utils.loopback }}",
    # "{{ '02:16:3e:e4:16:f3' is ansible.utils.mac }}",
    # "{{ '02-16-3e-e4-16-f3' is ansible.utils.mac }}",
    # "{{ '0216.3ee4.16f3' is ansible.utils.mac }}",
    # "{{ '02163ee416f3' is ansible.utils.mac }}",
    # "{{ 'string' is not ansible.utils.mac }}",
    # "{{ '224.0.0.1' is ansible.utils.multicast }}",
    # "{{ '127.0.0.1' is not ansible.utils.multicast }}",
    # "{{ '10.1.1.1' is ansible.utils.private }}",
    # "{{ '8.8.8.8' is not ansible.utils.private }}",
    # "{{ '8.8.8.8' is ansible.utils.public }}",
    # "{{ '10.1.1.1' is not ansible.utils.public }}",
    # "{{ '253.0.0.1' is ansible.utils.reserved }}",
    # "{{ '128.146.1.7' is not ansible.utils.reserved }}",
    # "{{ '10.1.1.0/24' is ansible.utils.subnet_of '10.0.0.0/8' }}",
    # "{{ '192.168.1.0/24' is not ansible.utils.subnet_of '10.0.0.0/8' }}",
    # "{{ '10.0.0.0/8' is ansible.utils.supernet_of '10.1.1.0/24' }}",
    # "{{ '0.0.0.0' is ansible.utils.unspecified }}",
    # "{{ '0:0:0:0:0:0:0:0' is ansible.utils.unspecified }}",
    # "{{ '::' is ansible.utils.unspecified }}",
    # "{{ '::1' is not ansible.utils.unspecified }}",
]


class TestIpaddress(unittest.TestCase):
    def setUp(self):
        self._templar = Templar(loader=None, variables=vars)

    def test_simple(self):
        """ Confirm some simple jinja tests
        """
        for test in TESTS:
            self.assertTrue(self._templar.template(test), test)

    def test_no_lib(self):
        """ Confirm missing lib
        """
        ipaddress.HAS_IPADDRESS = False
        template_data = "{{ '10.1.1.1' is ansible.utils.ip }}"
        with self.assertRaises(Exception) as error:
            self._templar.template(template_data)
        self.assertIn("'ip' requires 'ipaddress'", str(error.exception))

    def test_fail_subnet(self):
        """ Confirm non ip obj passed to is_subnet_of
        """
        self.assertFalse(ipaddress._is_subnet_of("a", "b"))

    def fail_list_needed(self):
        """ Confirm graceful fail when list is required but not provided
        """
        template_data = "{{ '10.1.1.1' is not ansible.utils.in_one_network '10.0.0.0/8' }}"
        with self.assertRaises(Exception) as error:
            self._templar.template(template_data)
        self.assertIn("'in_one_network' requires a list", str(error.exception))