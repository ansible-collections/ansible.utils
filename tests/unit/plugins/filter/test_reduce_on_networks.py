# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit test file for reduce_on_networks filter plugin
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest import TestCase

from ansible.errors import AnsibleError

from ansible_collections.ansible.utils.plugins.filter.reduce_on_networks import _reduce_on_networks


class Test_reduce_on_networks(TestCase):
    def setUp(self):
        pass

    def test_invalid_data(self):
        """Check passing invalid argspec"""

        # missing required arguments
        args = [""]
        kwargs = {}
        with self.assertRaises(AnsibleError) as error:
            _reduce_on_networks(*args, **kwargs)
        self.assertIn("missing required arguments: value", str(error.exception))

        # wrong input value type
        args = ["", ""]
        kwargs = {}
        with self.assertRaises(AnsibleError) as error:
            _reduce_on_networks(*args, **kwargs)
        self.assertIn("missing required arguments: value", str(error.exception))

        # wrong networks type
        args = ["", ["192.168.0.0"], ""]
        kwargs = {}
        with self.assertRaises(AnsibleError) as error:
            _reduce_on_networks(*args, **kwargs)
        self.assertIn("missing required arguments: value", str(error.exception))

    def test_reduce_on_networks_filter_1(self):
        """reduce_on_network filter"""
        list1 = ["192.168.0.34", "10.3.0.3", "192.168.2.34"]
        list2 = ["192.168.0.0/24", "127.0.0.0/8", "192.128.0.0/9"]
        args = ["", list1, list2]
        result = _reduce_on_network(*args)
        expected = {
            "192.168.0.34": ["192.168.0.0/24", "192.128.0.0/9"],
            "192.168.2.34": ["192.128.0.0/9"],
        }
        self.assertEqual(result, expected)

