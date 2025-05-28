# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest import TestCase

from ansible._internal._templating._jinja_common import UndefinedMarker

from ansible._internal._templating._engine import TemplateEngine

from ansible_collections.ansible.utils.plugins.module_utils.common.get_path import get_path

from ansible._internal._templating._utils import TemplateContext

from ansible._internal._templating._utils import LazyOptions
from ansible.parsing.yaml.objects import AnsibleUnicode

class TestGetPath(TestCase):
    def setUp(self):
        self.engine = TemplateEngine(loader=None)
        self._environment = self.engine.environment

    def test_get_path_pass(self):
        var = {"a": {"b": {"c": {"d": [0, 1]}}}}
        path = "a.b.c.d[0]"

        ctx = TemplateContext(
            template_value=AnsibleUnicode(path),
            templar=self.engine,
            options=LazyOptions.DEFAULT,
        )
        token = TemplateContext._contextvar.set(ctx)

        try:
            result = get_path(var, path, environment=self._environment, wantlist=False)
            self.assertEqual(result, 0)
        finally:
            TemplateContext._contextvar.reset(token)

    def test_get_path_pass_wantlist(self):
        var = {"a": {"b": {"c": {"d": [0, 1]}}}}
        path = "a.b.c.d[0]"

        ctx = TemplateContext(
            template_value=AnsibleUnicode(path),
            templar=self.engine,
            options=LazyOptions.DEFAULT,
        )
        token = TemplateContext._contextvar.set(ctx)

        try:
            result = get_path(var, path, environment=self._environment, wantlist=True)
            self.assertEqual(result, [0])
        finally:
            TemplateContext._contextvar.reset(token)

    def test_get_path_fail(self):
        var = {"a": {"b": {"c": {"d": [0, 1]}}}}
        path = "a.b.e"
    
        ctx = TemplateContext(
            template_value=AnsibleUnicode(path),
            templar=self.engine,
            options=LazyOptions.DEFAULT,
        )
        token = TemplateContext._contextvar.set(ctx)
    
        try:
            result = get_path(var, path, environment=self._environment, wantlist=False)
            self.assertIsInstance(result, UndefinedMarker)
        finally:
            TemplateContext._contextvar.reset(token)
