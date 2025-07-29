# (c) 2022 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

import pytest

from ansible.errors import AnsibleError
from ansible.module_utils._text import to_text

from ansible_collections.ansible.utils.plugins.plugin_utils.base.validate import _load_validator


@pytest.fixture(name="test_rule")
def criterion():
    return {"name": "Rule name", "rule": "Rule regex", "action": "warn"}


@pytest.fixture(name="validator")
def config_validator():
    engine, result = _load_validator(engine="ansible.utils.config", data="", criteria=[])
    return engine


@pytest.mark.parametrize("key", ["name", "rule", "action"])
def test_check_args_missing_key(validator, test_rule, key):
    del test_rule[key]
    original = to_text(test_rule)
    validator._criteria.append(test_rule)

    try:
        validator._check_args()
        error = ""
    except AnsibleError as exc:
        error = to_text(exc)

    assert error == 'Criteria {rule} missing "{key}" key'.format(rule=original, key=key)


def test_invalid_yaml(validator):
    test_rule = "[This is not valid YAML"
    validator._criteria = test_rule

    try:
        validator._check_args()
        error = ""
    except AnsibleError as exc:
        error = to_text(exc)

    expected_error = "'criteria' option value is invalid, value should be valid YAML."
    # Don't test for exact error string, varies with Python version
    assert error.startswith(expected_error)


def test_invalid_action(validator, test_rule):
    test_rule["action"] = "flunge"
    original = to_text(test_rule)
    validator._criteria.append(test_rule)

    try:
        validator._check_args()
        error = ""
    except AnsibleError as exc:
        error = to_text(exc)

    expected_error = 'Action in criteria {item} is not one of "warn" or "fail"'.format(
        item=original,
    )
    assert error == expected_error


def test_invalid_regex(validator, test_rule):
    test_rule["rule"] = "reg(ex"
    validator._criteria.append(test_rule)

    try:
        validator._check_args()
        error = ""
    except AnsibleError as exc:
        error = to_text(exc)

    expected_error = 'Failed to compile regex "reg(ex":'
    # Don't test for exact error string, varies with Python version
    assert error.startswith(expected_error)


def test_valid_warning(validator, test_rule):
    validator._criteria.append(test_rule)
    validator._data = "This line matches Rule regex."

    validator.validate()
    assert "errors" not in validator._result
    assert len(validator._result["warnings"]) == 1


def test_valid_error(validator, test_rule):
    test_rule["action"] = "fail"
    validator._criteria.append(test_rule)
    validator._data = "This line matches Rule regex."

    validator.validate()
    assert len(validator._result["errors"]) == 1
    assert "warnings" not in validator._result
