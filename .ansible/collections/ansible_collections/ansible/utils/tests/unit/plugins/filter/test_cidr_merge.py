# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit test file for cidr_merge filter plugin
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest import TestCase

from ansible.errors import AnsibleFilterError

from ansible_collections.ansible.utils.plugins.filter.cidr_merge import _cidr_merge


INVALID_DATA_MERGE = ["0.1234.34.44", "1.00000.2.000.22"]

VALID_DATA_MEREGE = ["192.168.0.0/17", "192.168.128.0/17", "192.168.128.1"]

VALID_OUTPUT_MERGE = ["192.168.0.0/16"]

VALID_DATA_SPAN = ["192.168.1.1", "192.168.1.2", "192.168.1.3", "192.168.1.4"]

VALID_OUTPUT_SPAN = "192.168.1.0/29"


class TestCidrMerge(TestCase):
    def setUp(self):
        pass

    def test_invalid_data_merge(self):
        """Check passing invalid argspec"""

        args = ["", INVALID_DATA_MERGE, "merge"]
        kwargs = {}
        with self.assertRaises(AnsibleFilterError) as error:
            _cidr_merge(*args, **kwargs)
        self.assertIn("invalid IPNetwork 0.1234.34.44", str(error.exception))

    def test_valid_data_merge(self):
        """test for cidr_merge plugin with merge"""

        args = ["", VALID_DATA_MEREGE, "merge"]
        result = _cidr_merge(*args)
        self.assertEqual(result, VALID_OUTPUT_MERGE)

    def test_valid_data_span(self):
        """test for cidr_merge plugin with span"""

        args = ["", VALID_DATA_SPAN, "span"]
        result = _cidr_merge(*args)
        self.assertEqual(result, VALID_OUTPUT_SPAN)

    def test_valid_data_with_invalid_action(self):
        """Check passing valid data as per criteria"""

        args = ["", VALID_DATA_SPAN, "span1"]
        kwargs = {}
        with self.assertRaises(AnsibleFilterError) as error:
            _cidr_merge(*args, **kwargs)
        self.assertIn("cidr_merge: invalid action 'span1'", str(error.exception))
