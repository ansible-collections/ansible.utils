# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function


__metaclass__ = type

import unittest

from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
    AnsibleArgSpecValidator,
)

from .fixtures.docstring import DOCUMENTATION


class TestSortList(unittest.TestCase):
    def test_simple_pass(self):
        data = {"param_str": "string"}
        aav = AnsibleArgSpecValidator(
            data=data,
            schema=DOCUMENTATION,
            schema_format="doc",
            schema_conditionals={},
            name="test_action",
        )
        valid, errors, _updated_data = aav.validate()
        assert valid
        if not errors:
            errors = None
        assert errors is None

    def test_simple_defaults(self):
        data = {"param_str": "string"}
        aav = AnsibleArgSpecValidator(
            data=data,
            schema=DOCUMENTATION,
            schema_format="doc",
            schema_conditionals={},
            name="test_action",
        )
        expected = {
            "param_str": "string",
            "param_default": True,
            "params_bool": None,
            "params_dict": None,
        }
        valid, errors, updated_data = aav.validate()
        assert valid
        if not errors:
            errors = None
        assert errors is None
        assert expected == updated_data

    def test_simple_fail(self):
        data = {}
        aav = AnsibleArgSpecValidator(
            data=data,
            schema=DOCUMENTATION,
            schema_format="doc",
            schema_conditionals={},
            name="test_action",
        )
        valid, errors, _updated_data = aav.validate()
        assert not valid
        assert "missing required arguments: param_str" in errors

    def test_simple_fail_no_name(self):
        data = {}
        aav = AnsibleArgSpecValidator(
            data=data,
            schema=DOCUMENTATION,
            schema_format="doc",
            schema_conditionals={},
        )
        valid, errors, _updated_data = aav.validate()
        assert not valid
        assert "missing required arguments: param_str" in errors

    def test_not_doc(self):
        data = {"param_str": "string"}
        aav = AnsibleArgSpecValidator(
            data=data,
            schema={"argument_spec": {"param_str": {"type": "str"}}},
            schema_format="argspec",
            name="test_action",
        )
        valid, errors, _updated_data = aav.validate()
        assert valid
        if not errors:
            errors = None
        assert errors is None

    def test_schema_conditional(self):
        data = {"param_str": "string"}
        aav = AnsibleArgSpecValidator(
            data=data,
            schema=DOCUMENTATION,
            schema_format="doc",
            schema_conditionals={"required_together": [["param_str", "param_bool"]]},
            name="test_action",
        )
        valid, errors, _updated_data = aav.validate()
        assert not valid
        assert "parameters are required together: param_str, param_bool" in errors

    def test_unsupported_param(self):
        data = {"param_str": "string", "not_valid": "string"}
        aav = AnsibleArgSpecValidator(
            data=data,
            schema=DOCUMENTATION,
            schema_format="doc",
            name="test_action",
        )
        valid, errors, _updated_data = aav.validate()
        assert not valid
        if isinstance(errors, list):
            # for ansibleargspecvalidator 2.11 its returning errors as list
            assert "not_valid. Supported parameters include:" in errors[0]
        else:
            assert "Unsupported parameters for 'test_action' module: not_valid" in errors

    def test_other_args(self):
        data = {"param_str": "string"}
        aav = AnsibleArgSpecValidator(
            data=data,
            schema=DOCUMENTATION,
            schema_format="doc",
            name="test_action",
            other_args={"bypass_checks": True},
        )
        valid, errors, _updated_data = aav.validate()
        assert valid
        if not errors:
            errors = None
        assert errors is None

    def test_invalid_spec(self):
        data = {}
        aav = AnsibleArgSpecValidator(
            data=data,
            schema={"not_valid": True},
            schema_format="argspec",
            name="test_action",
            other_args={"bypass_checks": True},
        )
        valid, errors, _updated_data = aav.validate()
        assert not valid
        assert "Invalid schema. Invalid keys found: not_valid" in errors
