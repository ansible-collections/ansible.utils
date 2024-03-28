# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest import TestCase

from ansible.errors import AnsibleFilterError

from ansible_collections.ansible.utils.plugins.filter.fact_diff import _fact_diff


class TestUpdate_Fact(TestCase):
    def setUp(self):
        pass

    def test_same(self):
        """Ensure two equal string don't create a diff"""
        before = "Lorem ipsum dolor sit amet"
        after = before
        result = _fact_diff("", before, after)
        self.assertEqual("[]", result)

    def test_string(self):
        """Compare two strings"""
        before = "Lorem ipsum dolor sit amet, consectetur adipiscing elit"
        after = "Lorem ipsum dolor sit amet, AAA consectetur adipiscing elit"
        result = _fact_diff("", before, after)
        self.assertIn("-" + before, result)
        self.assertIn("+" + after, result)

    def test_string_skip_lines(self):
        """Compare two string, with skip_lines"""
        before = "Lorem ipsum dolor sit amet, consectetur adipiscing elit"
        after = "Lorem ipsum dolor sit amet, AAA consectetur adipiscing elit"
        result = _fact_diff("", before, after, plugin={"vars": {"skip_lines": "^Lorem"}})
        print(result)
        self.assertEqual("[]", result)

    def test_same_list(self):
        """Compare two lists that are the same"""
        before = "[0, 1, 2, 3]"
        after = before
        result = _fact_diff("", before, after)
        self.assertEqual("[]", result)

    def test_diff_list_skip_lines(self):
        """Compare two lists, with skip_lines"""
        before = [0, 1, 2]
        after = [0, 1, 2, 3]
        result = _fact_diff("", before, after, plugin={"vars": {"skip_lines": "3"}})
        self.assertEqual("[]", result)

    def test_diff_list(self):
        """Compare two lists with differences"""
        before = [0, 1, 2, 3]
        after = [0, 1, 2, 4]
        result = _fact_diff("", before, after)
        self.assertIn("-3", result)
        self.assertIn("+4", result)

    def test_same_dict(self):
        """Compare two dicts that are the same"""
        before = {"a": {"b": {"c": {"d": [0, 1, 2]}}}}
        after = before
        result = _fact_diff("", before, after)
        self.assertEqual("[]", result)

    def test_diff_dict_skip_lines(self):
        """Compare two dicts, with skip_lines"""
        before = {"a": {"b": {"c": {"d": [0, 1, 2]}}}}
        after = {"a": {"b": {"c": {"d": [0, 1, 2, 3]}}}}
        result = _fact_diff("", before, after, {"vars": {"skip_lines": "3"}})
        self.assertEqual("[]", result)

    def test_diff_dict(self):
        """Compare two dicts that are different"""
        self.maxDiff = None
        before = {"a": {"b": {"c": {"d": [0, 1, 2, 3]}}}}
        after = {"a": {"b": {"c": {"d": [0, 1, 2, 4]}}}}
        result = _fact_diff("", before, after)
        self.assertIn("-                    3", result)
        self.assertIn("+                    4", result)

    def test_invalid_regex(self):
        """Check with invalid regex"""
        before = after = True
        with self.assertRaises(AnsibleFilterError) as error:
            result = _fact_diff("", before, after, {"vars": {"skip_lines": "+"}})
        self.assertIn(
            "The regex '+', is not valid.",
            str(error.exception),
        )

    def test_argspec(self):
        """Validate argspec"""
        before = True
        with self.assertRaises(AnsibleFilterError) as error:
            result = _fact_diff("", before)
        self.assertIn(
            "missing required arguments: after",
            str(error.exception),
        )

    def test_diff_dict_common(self):
        """Compare two dicts that with common option"""
        self.maxDiff = None
        before = {"a": {"b": {"c": {"d": [0, 1, 2, 3]}}}}
        after = {"a": {"b": {"c": {"d": [0, 1, 2, 4]}}}}
        result = _fact_diff("", before, after, common=True)
        self.assertIn("                    0", result)
        self.assertIn("                    1", result)
        self.assertIn("                    2", result)
