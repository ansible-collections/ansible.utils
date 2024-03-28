# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit test file for reduce_on_network filter plugin
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest import TestCase

from ansible.errors import AnsibleError

from ansible_collections.ansible.utils.plugins.filter.reduce_on_network import _reduce_on_network


class Test_reduce_on_network(TestCase):
    def setUp(self):
        pass

    def test_invalid_data(self):
        """Check passing invalid argspec"""

        # missing required arguments
        args = [""]
        kwargs = {}
        with self.assertRaises(AnsibleError) as error:
            _reduce_on_network(*args, **kwargs)
        self.assertIn("missing required arguments: value", str(error.exception))

    def test_reduce_on_network_filter_1(self):
        """reduce_on_network filter"""
        list1 = ["192.168.0.34", "10.3.0.3", "192.168.2.34"]
        args = ["", list1, "192.168.0.0/24"]
        result = _reduce_on_network(*args)
        self.assertEqual(result, ["192.168.0.34"])
