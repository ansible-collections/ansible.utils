# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit test file for network_in_network filter plugin
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest import TestCase

from ansible_collections.ansible.utils.plugins.filter.network_in_network import _network_in_network


class Test_network_in_network(TestCase):
    def setUp(self):
        pass

    def test_network_in_network_filter_1(self):
        """network_in_network filter"""
        args = ["", "192.168.0.0/24", "192.168.0.1"]
        result = _network_in_network(*args)
        self.assertEqual(result, True)

    def test_network_in_network_filter_2(self):
        """network_in_network filter"""
        args = ["", "192.168.0.0/24", "10.0.0.1"]
        result = _network_in_network(*args)
        self.assertEqual(result, False)

    def test_network_in_network_filter_3(self):
        """network_in_network filter"""
        args = ["", "192.168.0.0/16", "192.168.0.0/24"]
        result = _network_in_network(*args)
        self.assertEqual(result, True)
