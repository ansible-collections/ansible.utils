# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit test file for network_in_usable filter plugin
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

import unittest

from ansible_collections.ansible.utils.plugins.filter.network_in_usable import _network_in_usable


class Test_Network_In_Usable(unittest.TestCase):
    def setUp(self):
        pass

    def test_network_in_usable_filter_1(self):
        """network_in_usable filter"""
        args = ["", "192.168.0.0/24", "192.168.0.1"]
        result = _network_in_usable(*args)
        self.assertEqual(result, True)

    def test_network_in_usable_filter_2(self):
        """network_in_usable filter"""
        args = ["", "192.168.0.0/24", "192.168.0.255"]
        result = _network_in_usable(*args)
        self.assertEqual(result, False)

    def test_network_in_usable_filter_3(self):
        """network_in_usable filter"""
        args = ["", "192.168.0.0/16", "192.168.0.255"]
        result = _network_in_usable(*args)
        self.assertEqual(result, True)
