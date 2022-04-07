# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type

import re
import unittest


from ansible import __version__ as ansible_version
from ansible.template import Templar
from ansible.template import AnsibleUndefined

from ansible_collections.ansible.utils.plugins.module_utils.common.get_path import (
    get_path,
)


class TestGetPath(unittest.TestCase):
    def setUp(self):
        self._environment = Templar(loader=None).environment
        self._ansible_minor_version = int(
            re.match(r"^\d+\.(?P<minor>\d+).*$", ansible_version).groupdict()['minor']
        )

    def test_get_path_pass(self):
        var = {"a": {"b": {"c": {"d": [0, 1]}}}}
        path = "a.b.c.d[0]"
        result = get_path(var, path, environment=self._environment, wantlist=False)
        if self._ansible_minor_version >= 13:
            expected = 0
        else:
            expected = "0"
        self.assertEqual(result, expected)

    def test_get_path_pass_wantlist(self):
        var = {"a": {"b": {"c": {"d": [0, 1]}}}}
        path = "a.b.c.d[0]"
        result = get_path(var, path, environment=self._environment, wantlist=True)
        if self._ansible_minor_version >= 13:
            expected = [0]
        else:
            expected = ["0"]
        self.assertEqual(result, expected)

    def test_get_path_fail(self):
        var = {"a": {"b": {"c": {"d": [0, 1]}}}}
        path = "a.b.e"
        if self._ansible_minor_version >= 13:
            result = get_path(var, path, environment=self._environment, wantlist=False)
            assert isinstance(result, AnsibleUndefined)
        else:
            with self.assertRaises(Exception) as exc:
                get_path(var, path, environment=self._environment, wantlist=False)
            expected = "dict object' has no attribute 'e'"
            self.assertIn(expected, str(exc.exception))

