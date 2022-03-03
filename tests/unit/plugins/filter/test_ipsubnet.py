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

from ansible_collections.ansible.utils.plugins.filter.ipsubnet import _ipsubnet


address = "192.168.144.5"
subnet = "192.168.0.0/16"


class TestIpSubnet(unittest.TestCase):
    def setUp(self):
        pass

    def test_ipvsubnet_address_subnet(self):
        """convert address to subnet"""
        args = ["", address, ""]
        result = _ipsubnet(*args)
        self.assertEqual(result, "192.168.144.5/32")

    def test_ipvsubnet_filter_subnet(self):
        """check if a given string is a subnet"""
        args = ["", subnet, ""]
        result = _ipsubnet(*args)
        self.assertEqual(result, "192.168.0.0/16")

    def test_ipvsubnet_filter_subnet_size(self):
        """Get the number of subnets a given subnet can be split into."""
        args = ["", subnet, "20"]
        result = _ipsubnet(*args)
        self.assertEqual(result, "16")

    def test_ipvsubnet_filter_subnet_with_1st_index(self):
        """Get the 1st subnet"""
        args = ["", subnet, "20", 0]
        result = _ipsubnet(*args)
        self.assertEqual(result, "192.168.0.0/20")

    def test_ipvsubnet_filter_subnet_with_last_index(self):
        """Get the last subnet"""
        args = ["", subnet, "20", -1]
        result = _ipsubnet(*args)
        self.assertEqual(result, "192.168.240.0/20")

    def test_ipvsubnet_filter_address_with_size(self):
        """Get biggest subnet that contains that given IP address"""
        args = ["", address, "20"]
        result = _ipsubnet(*args)
        self.assertEqual(result, "192.168.144.0/20")

    def test_ipvsubnet_filter_address_with_1st_index(self):
        """Get the 1st subnet"""
        args = ["", address, "18", 0]
        result = _ipsubnet(*args)
        self.assertEqual(result, "192.168.128.0/18")

    def test_ipvsubnet_filter_address_with_last_index(self):
        """Get the last subnet"""
        args = ["", address, "18", -1]
        result = _ipsubnet(*args)
        self.assertEqual(result, "192.168.144.4/31")

    def test_ipvsubnet_filter_lots_of_subnets_v4_bottom1(self):
        """Use the subnets call to see if it slows way down with v4"""
        args = ["", "0.0.0.0/1", "31", -1]
        result = _ipsubnet(*args)
        self.assertEqual(result, "127.255.255.254/31")

    def test_ipvsubnet_filter_lots_of_subnets_v4_bottom2(self):
        """Use the subnets call to see if it slows way down with v4"""
        args = ["", "1.0.0.0/1", "3", -1]
        result = _ipsubnet(*args)
        self.assertEqual(result, "96.0.0.0/3")

    def test_ipvsubnet_filter_lots_of_subnets_v4_top1(self):
        """Use the subnets call to see if it slows way down with v4"""
        args = ["", "128.0.0.0/1", "31", -1]
        result = _ipsubnet(*args)
        self.assertEqual(result, "255.255.255.254/31")

    def test_ipvsubnet_filter_lots_of_subnets_v4_top2(self):
        """Use the subnets call to see if it slows way down with v4"""
        args = ["", "130.0.0.0/1", "31", -1]
        result = _ipsubnet(*args)
        self.assertEqual(result, "255.255.255.254/31")

    def test_ipvsubnet_filter_lots_of_subnets_v6_bottom1(self):
        """Use the subnets call to see if it slows way down with v6"""
        args = ["", "8000::/1", "127", -1]
        result = _ipsubnet(*args)
        self.assertEqual(result, "ffff:ffff:ffff:ffff:ffff:ffff:ffff:fffe/127")

    def test_ipvsubnet_filter_lots_of_subnets_v6_bottom2(self):
        """Use the subnets call to see if it slows way down with v6"""
        args = ["", "9000::/1", "127", -1]
        result = _ipsubnet(*args)
        self.assertEqual(result, "ffff:ffff:ffff:ffff:ffff:ffff:ffff:fffe/127")

    def test_ipvsubnet_filter_lots_of_subnets_v6_top1(self):
        """Use the subnets call to see if it slows way down with v6"""
        args = ["", "::/1", "127", -1]
        result = _ipsubnet(*args)
        self.assertEqual(result, "7fff:ffff:ffff:ffff:ffff:ffff:ffff:fffe/127")

    def test_ipvsubnet_filter_lots_of_subnets_v6_top2(self):
        """Use the subnets call to see if it slows way down with v6"""
        args = ["", "1000::/1", "127", -1]
        result = _ipsubnet(*args)
        self.assertEqual(result, "7fff:ffff:ffff:ffff:ffff:ffff:ffff:fffe/127")

    def test_ipvsubnet_filter_rank_address_in_subnet(self):
        """The rank of the IP in the subnet (the IP is the 36870nth /32 of the subnet)"""
        args = ["", address, subnet]
        result = _ipsubnet(*args)
        self.assertEqual(result, "36870")

    def test_ipvsubnet_filter_rank_address_in_subnet1(self):
        """The rank of the IP in the 192.168.144.0/24"""
        args = ["", address, "192.168.144.0/24"]
        result = _ipsubnet(*args)
        self.assertEqual(result, "6")

    def test_ipvsubnet_filter_rank_address_in_subnet2(self):
        """The rank of the IP in the 192.168.144.0/24"""
        args = ["", "192.168.144.1/30", "192.168.144.0/24"]
        result = _ipsubnet(*args)
        self.assertEqual(result, "1")

    def test_ipvsubnet_filter_rank_address_in_subnet3(self):
        """The rank of the IP in the 192.168.144.0/24"""
        args = ["", "192.168.144.16/30", "192.168.144.0/24"]
        result = _ipsubnet(*args)
        self.assertEqual(result, "5")
