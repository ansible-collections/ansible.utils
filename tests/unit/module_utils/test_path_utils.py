# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
import heapq
import os
import unittest
from ansible_collections.ansible.utils.plugins.module_utils.path_utils import (
    get_path,
    to_paths,
)
from ansible.template import Templar


class TestPathUtils(unittest.TestCase):
    def setUp(self):
        self._environment = Templar(loader=None).environment

    def test_get_path_pass(self):
        var = {"a": {"b": {"c": {"d": [0, 1]}}}}
        path = "a.b.c.d[0]"
        result = get_path(var, path, environment=self._environment)
        expected = "0"
        self.assertEqual(result, expected)

    def test_get_path_pass_wantlist(self):
        var = {"a": {"b": {"c": {"d": [0, 1]}}}}
        path = "a.b.c.d[0]"
        result = get_path(
            var, path, environment=self._environment, wantlist=True
        )
        expected = ["0"]
        self.assertEqual(result, expected)

    def test_get_path_fail(self):
        var = {"a": {"b": {"c": {"d": [0, 1]}}}}
        path = "a.b.e"
        expected = "dict object' has no attribute 'e'"
        with self.assertRaises(Exception) as exc:
            get_path(var, path, environment=self._environment)
        self.assertIn(expected, str(exc.exception))

    def test_to_paths(self):
        var = {"a": {"b": {"c": {"d": [0, 1]}}}}
        expected = {"a.b.c.d[0]": 0, "a.b.c.d[1]": 1}
        result = to_paths(var)
        self.assertEqual(result, expected)

    def test_to_paths_wantlist(self):
        var = {"a": {"b": {"c": {"d": [0, 1]}}}}
        expected = [{"a.b.c.d[0]": 0, "a.b.c.d[1]": 1}]
        result = to_paths(var, wantlist=True)
        self.assertEqual(result, expected)

    def test_to_paths_special_char(self):
        var = {"a": {"b": {"c": {"Eth1/1": True}}}}
        expected = [{"a.b.c['Eth1/1']": True}]
        result = to_paths(var, wantlist=True)
        self.assertEqual(result, expected)

    def test_to_paths_prepend(self):
        var = {"a": {"b": {"c": {"d": [0, 1]}}}}
        expected = [{"var.a.b.c.d[0]": 0, "var.a.b.c.d[1]": 1}]
        result = to_paths(var, wantlist=True, prepend="var")
        self.assertEqual(result, expected)

    def test_to_paths_prepend_fail(self):
        var = {"a": {"b": {"c": {"d": [0, 1]}}}}
        expected = "must be a string"
        with self.assertRaises(Exception) as exc:
            to_paths(var, wantlist=True, prepend=5)
        self.assertIn(expected, str(exc.exception))

    def test_roundtrip_large(self):
        """ Test the 1000 longest keys, otherwise this takes a _really_ long time
        """
        big_json_path = os.path.join(
            os.path.dirname(__file__), "fixtures", "large.json"
        )
        with open(big_json_path) as fhand:
            big_json = fhand.read()
        var = json.loads(big_json)
        paths = to_paths(var)
        to_tests = heapq.nlargest(1000, list(paths.keys()), key=len)
        for to_test in to_tests:
            gotten = get_path(var, to_test, environment=self._environment)
            self.assertEqual(gotten, paths[to_test])
