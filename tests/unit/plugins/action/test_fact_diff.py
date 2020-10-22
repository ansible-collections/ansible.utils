# -*- coding: utf-8 -*-
# Copyafter 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import copy
import re
import unittest
from mock import MagicMock
from ansible.playbook.task import Task
from ansible.template import Templar

from ansible_collections.ansible.utils.plugins.action.fact_diff import (
    ActionModule,
)


class TestUpdate_Fact(unittest.TestCase):
    def setUp(self):
        task = MagicMock(Task)
        play_context = MagicMock()
        play_context.check_mode = False
        connection = MagicMock()
        fake_loader = {}
        templar = Templar(loader=fake_loader)
        self._plugin = ActionModule(
            task=task,
            connection=connection,
            play_context=play_context,
            loader=fake_loader,
            templar=templar,
            shared_loader_obj=None,
        )
        self._plugin._task.action = "fact_diff"
        self._task_vars = {"inventory_hostname": "mockdevice"}

    def test_argspec_no_updates(self):
        """Check passing invalid argspec"""
        self._plugin._task.args = {"before": True}
        with self.assertRaises(Exception) as error:
            self._plugin.run(task_vars=self._task_vars)
        self.assertIn(
            "missing required arguments: after",
            str(error.exception),
        )

    def test_same(self):
        before = "Lorem ipsum dolor sit amet"
        after = before
        self._plugin._task.args = {"before": before, "after": after}
        result = self._plugin.run(task_vars=self._task_vars)
        self.assertFalse(result["changed"])
        self.assertEqual([], result["diff_lines"])
        self.assertEqual("", result["diff_text"])

    def test_string(self):
        before = "Lorem ipsum dolor sit amet, consectetur adipiscing elit"
        after = "Lorem ipsum dolor sit amet, AAA consectetur adipiscing elit"
        self._plugin._task.args = {"before": before, "after": after}
        result = self._plugin.run(task_vars=self._task_vars)
        self.assertTrue(result["changed"])
        self.assertIn("-" + before, result["diff_lines"])
        self.assertIn("-" + before, result["diff_text"])
        self.assertIn("+" + after, result["diff_lines"])
        self.assertIn("+" + after, result["diff_text"])

    def test_string_skip_lines(self):
        before = "Lorem ipsum dolor sit amet, consectetur adipiscing elit"
        after = "Lorem ipsum dolor sit amet, AAA consectetur adipiscing elit"
        self._plugin._task.args = {
            "before": before,
            "after": after,
            "vars": {"skip_lines": "^Lorem"},
        }
        result = self._plugin.run(task_vars=self._task_vars)
        self.assertFalse(result["changed"])
        self.assertEqual([], result["diff_lines"])
        self.assertEqual("", result["diff_text"])

    def test_same_list(self):
        before = [0, 1, 2, 3]
        after = before
        self._plugin._task.args = {"before": before, "after": after}
        result = self._plugin.run(task_vars=self._task_vars)
        self.assertFalse(result["changed"])
        self.assertEqual([], result["diff_lines"])
        self.assertEqual("", result["diff_text"])

    def test_diff_list_skip_lines(self):
        before = [0, 1, 2]
        after = [0, 1, 2, 3]
        self._plugin._task.args = {
            "before": before,
            "after": after,
            "vars": {"skip_lines": "3"},
        }
        result = self._plugin.run(task_vars=self._task_vars)
        self.assertFalse(result["changed"])
        self.assertEqual([], result["diff_lines"])
        self.assertEqual("", result["diff_text"])

    def test_diff_list(self):
        before = [0, 1, 2, 3]
        after = [0, 1, 2, 4]
        self._plugin._task.args = {"before": before, "after": after}
        result = self._plugin.run(task_vars=self._task_vars)
        self.assertTrue(result["changed"])
        self.assertIn("-3", result["diff_lines"])
        self.assertIn("-3", result["diff_text"])
        self.assertIn("+4", result["diff_lines"])
        self.assertIn("+4", result["diff_text"])

    def test_same_dict(self):
        before = {"a": {"b": {"c": {"d": [0, 1, 2]}}}}
        after = before
        self._plugin._task.args = {"before": before, "after": after}
        result = self._plugin.run(task_vars=self._task_vars)
        self.assertFalse(result["changed"])
        self.assertEqual([], result["diff_lines"])
        self.assertEqual("", result["diff_text"])

    def test_diff_dict_skip_lines(self):
        before = {"a": {"b": {"c": {"d": [0, 1, 2]}}}}
        after = {"a": {"b": {"c": {"d": [0, 1, 2, 3]}}}}
        self._plugin._task.args = {
            "before": before,
            "after": after,
            "vars": {"skip_lines": "3"},
        }
        result = self._plugin.run(task_vars=self._task_vars)
        self.assertFalse(result["changed"])
        self.assertEqual([], result["diff_lines"])
        self.assertEqual("", result["diff_text"])

    def test_diff_dict(self):
        before = {"a": {"b": {"c": {"d": [0, 1, 2, 3]}}}}
        after = {"a": {"b": {"c": {"d": [0, 1, 2, 4]}}}}
        self._plugin._task.args = {"before": before, "after": after}
        result = self._plugin.run(task_vars=self._task_vars)
        self.assertTrue(result["changed"])
        mlines = [l for l in result["diff_lines"] if re.match(r"^-\s+3$", l)]
        self.assertEqual(1, len(mlines))
        mlines = [l for l in result["diff_lines"] if re.match(r"^\+\s+4$", l)]
        self.assertEqual(1, len(mlines))
