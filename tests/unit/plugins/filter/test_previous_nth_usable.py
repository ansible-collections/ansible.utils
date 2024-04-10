# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit test file for ipwrap filter plugin
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest import TestCase

from ansible_collections.ansible.utils.plugins.filter.previous_nth_usable import (
    _previous_nth_usable,
)


class Test_previous_Nth_Usable(TestCase):
    def setUp(self):
        pass

    def test_previous_nth_usable_filter(self):
        """previous_nth_usable filter"""
        args = ["", "192.168.122.10/24", 2]
        result = _previous_nth_usable(*args)
        self.assertEqual(result, "192.168.122.8")

    def test_previous_nth_usable_with_empty_return_string(self):
        """Check ipv4 to ipv6 conversion"""
        args = ["", "192.168.122.1/24", 2]
        result = _previous_nth_usable(*args)
        self.assertEqual(result, None)
