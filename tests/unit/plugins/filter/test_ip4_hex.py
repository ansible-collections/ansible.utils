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

from ansible.errors import AnsibleFilterError

from ansible_collections.ansible.utils.plugins.filter.ip4_hex import _ip4_hex


class TestIpWrap(unittest.TestCase):
    def setUp(self):
        pass

    def test_valid_data_list(self):
        """Check passing valid argspec(list)"""
        args = ["", "192.168.1.5", ""]
        result = _ip4_hex(*args)
        print(result)
        self.assertEqual(result, "c0a80105")

    def test_valid_data_string(self):
        """Check passing valid argspec(string)"""

        args = ["", "192.168.1.5", ":"]
        result = _ip4_hex(*args)
        self.assertEqual(result, "c0:a8:01:05")

    def test_args(self):
        """Check passing invalid argspec"""

        # missing required arguments
        args = []
        kwargs = {}
        with self.assertRaises(AnsibleFilterError) as error:
            _ip4_hex(*args, **kwargs)
        self.assertIn("missing required arguments: arg", str(error.exception))
