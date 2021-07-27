# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type

import unittest
from ansible.errors import AnsibleFilterError
from ansible_collections.ansible.utils.plugins.filter.resource_list_compare import (
    resource_list_compare,
)


class TestResource_list_compare_merge(unittest.TestCase):
    def test_valid_data(self):
        """Check passing valid data as per criteria"""

        base = ["interfaces", "l2_interfaces", "l3_interfaces"]
        other = ["all"]
        args = [base, other]
        kwargs = {}
        result = resource_list_compare(*args, **kwargs)
        self.assertEqual(result["actionable"], base)

    def test_valid_data_with_not_bang(self):
        """Check passing valid data as per criteria"""

        base = ["interfaces", "l2_interfaces", "l3_interfaces"]
        other = ["!l2_interfaces", "all"]
        args = [base, other]
        expected = ["interfaces", "l3_interfaces"]
        kwargs = {}
        result = resource_list_compare(*args, **kwargs)
        self.assertEqual(result["actionable"], expected)

    def test_invalid_args_length_data(self):
        """Check passing valid data as per criteria"""

        base = {}
        args = [base]
        kwargs = {}
        with self.assertRaises(AnsibleFilterError) as error:
            resource_list_compare(*args, **kwargs)
        self.assertIn(
            "Missing either 'base' or 'other value in filter input",
            str(error.exception),
        )

    def test_invalid_base_type_data(self):
        """Check passing valid data as per criteria"""

        base = {""}
        other = ["all"]
        args = [base, other]
        kwargs = {}
        with self.assertRaises(AnsibleFilterError) as error:
            resource_list_compare(*args, **kwargs)
        self.assertIn("argument base is of type", str(error.exception))

    def test_invalid_other_type_data(self):
        """Check passing valid data as per criteria"""

        base = ["interfaces"]
        other = {"all"}
        args = [base, other]
        kwargs = {}
        with self.assertRaises(AnsibleFilterError) as error:
            resource_list_compare(*args, **kwargs)
        self.assertIn("argument target is of type", str(error.exception))

    def test_invalid_unsupported_bang(self):
        """Check passing valid data as per criteria"""

        base = ["interfaces"]
        other = ["every"]
        args = [base, other]
        kwargs = {}
        with self.assertRaises(AnsibleFilterError) as error:
            resource_list_compare(*args, **kwargs)
        self.assertIn("The following are unsupported", str(error.exception))
