# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

import unittest

from ansible.errors import AnsibleFilterError

from ansible_collections.ansible.utils.plugins.filter.validate import validate


DATA = {
    "GigabitEthernet0/0/0/0": {
        "auto_negotiate": False,
        "counters": {
            "in_crc_errors": 0,
            "in_errors": 0,
            "rate": {"in_rate": 0, "out_rate": 0},
        },
        "description": "configured using Ansible",
        "duplex_mode": "full",
        "enabled": True,
        "line_protocol": "up",
        "mtu": 1514,
        "oper_status": "down",
        "type": "GigabitEthernet",
    },
    "GigabitEthernet0/0/0/1": {
        "auto_negotiate": False,
        "counters": {
            "in_crc_errors": 10,
            "in_errors": 0,
            "rate": {"in_rate": 0, "out_rate": 0},
        },
        "description": "# interface is configures with Ansible",
        "duplex_mode": "full",
        "enabled": False,
        "line_protocol": "up",
        "mtu": 1514,
        "oper_status": "up",
        "type": "GigabitEthernet",
    },
}

CRITERIA_CRC_ERROR_CHECK = {
    "type": "object",
    "patternProperties": {
        "^.*": {
            "type": "object",
            "properties": {
                "counters": {"properties": {"in_crc_errors": {"type": "number", "maximum": 0}}}
            },
        }
    },
}

CRITERIA_ENABLED_CHECK = {
    "type": "object",
    "patternProperties": {"^.*": {"type": "object", "properties": {"enabled": {"enum": [True]}}}},
}

CRITERIA_OPER_STATUS_UP_CHECK = {
    "type": "object",
    "patternProperties": {
        "^.*": {
            "type": "object",
            "properties": {"oper_status": {"type": "string", "pattern": "up"}},
        }
    },
}

CRITERIA_IN_RATE_CHECK = {
    "type": "object",
    "patternProperties": {
        "^.*": {
            "type": "object",
            "properties": {
                "counters": {
                    "properties": {
                        "rate": {"properties": {"in_rate": {"type": "number", "maximum": 0}}}
                    }
                }
            },
        }
    },
}


class TestValidate(unittest.TestCase):
    def setUp(self):
        pass

    def test_invalid_argspec(self):
        """Check passing invalid argspec"""

        # missing required arguments
        args = [DATA]
        kwargs = {}
        with self.assertRaises(AnsibleFilterError) as error:
            validate(*args, **kwargs)
        self.assertIn(
            "Missing either 'data' or 'criteria' value in filter input, refer 'ansible.utils.validate' filter",
            str(error.exception),
        )

        # missing required arguments
        with self.assertRaises(AnsibleFilterError) as error:
            validate([DATA])
        self.assertIn("Missing either 'data' or 'criteria' value", str(error.exception))

        args = [DATA, [CRITERIA_IN_RATE_CHECK]]
        kwargs = {"engine": "ansible.utils.sample"}
        with self.assertRaises(AnsibleFilterError) as error:
            validate(*args, **kwargs)
        self.assertIn(
            "For engine 'ansible.utils.sample' error loading",
            str(error.exception),
        )

        args = ["invalid data", [CRITERIA_IN_RATE_CHECK]]
        kwargs = {"engine": "ansible.utils.jsonschema"}
        with self.assertRaises(AnsibleFilterError) as error:
            validate(*args, **kwargs)
        self.assertIn("'data' option value is invalid", str(error.exception))

        args = [DATA, "invalid criteria"]
        kwargs = {"engine": "ansible.utils.jsonschema"}
        with self.assertRaises(AnsibleFilterError) as error:
            validate(*args, **kwargs)
        self.assertIn("'criteria' option value is invalid", str(error.exception))

    def test_invalid_validate_plugin_config_options(self):
        """Check passing invalid validate plugin options"""

        args = [
            DATA,
            [
                CRITERIA_CRC_ERROR_CHECK,
                CRITERIA_ENABLED_CHECK,
                CRITERIA_OPER_STATUS_UP_CHECK,
            ],
        ]
        kwargs = {"engine": "ansible.utils.jsonschema", "draft": "draft0"}
        with self.assertRaises(AnsibleFilterError) as error:
            validate(*args, **kwargs)
        self.assertIn(
            "value of draft must be one of: draft3, draft4, draft6, draft7, got: draft0",
            str(error.exception),
        )

    def test_valid_data(self):
        """Check passing valid data as per criteria"""

        args = [DATA, CRITERIA_IN_RATE_CHECK]
        kwargs = {"engine": "ansible.utils.jsonschema"}
        result = validate(*args, **kwargs)
        self.assertEqual(result, [])
