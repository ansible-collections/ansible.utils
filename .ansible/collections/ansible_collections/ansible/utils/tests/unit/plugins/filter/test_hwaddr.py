# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit test file for hwaddr filter plugin
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest import TestCase

from ansible_collections.ansible.utils.plugins.filter.hwaddr import _hwaddr


class Test_hwaddr(TestCase):
    def setUp(self):
        pass

    def test_hwaddr_filter_1(self):
        """hwaddr filter"""
        args = ["", "1a:2b:3c:4d:5e:6f"]
        result = _hwaddr(*args)
        self.assertEqual(result, "1a:2b:3c:4d:5e:6f")

    def test_hwaddr_filter_2(self):
        """hwaddr filter"""
        args = ["", "1a:2b:3c:4d:5e:6f", "cisco"]
        result = _hwaddr(*args)
        self.assertEqual(result, "1a2b.3c4d.5e6f")
