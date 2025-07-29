# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest import TestCase

from ansible.errors import AnsibleError, AnsibleFilterError

from ansible_collections.ansible.utils.plugins.filter.to_xml import _to_xml


INVALID_DATA = '<netconf-state xmlns="urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring">'

VALID_DATA = {
    "interface-configurations": {
        "@xmlns": "http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg",
        "key1": "value1",
    },
}

OUTPUT_TABS = """<?xml version="1.0" encoding="utf-8"?>
<interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg">
\t<key1>value1</key1>
</interface-configurations>"""

OUTPUT_SPACES = """<?xml version="1.0" encoding="utf-8"?>
<interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg">
    <key1>value1</key1>
</interface-configurations>"""


class TestToXml(TestCase):
    def setUp(self):
        pass

    def test_invalid_data(self):
        """Check passing invalid argspec"""

        # missing required arguments
        args = ["", INVALID_DATA, "xmltodict"]
        kwargs = {}
        with self.assertRaises(AnsibleError) as error:
            _to_xml(*args, **kwargs)
        self.assertIn("we were unable to convert to dict", str(error.exception))

    def test_valid_data(self):
        """Check passing valid data as per criteria"""
        self.maxDiff = None
        args = ["", VALID_DATA, "xmltodict"]
        result = _to_xml(*args)
        self.assertEqual(result, OUTPUT_TABS)

    def test_args(self):
        """Check passing invalid argspec"""

        # missing required arguments
        args = []
        kwargs = {}
        with self.assertRaises(AnsibleFilterError) as error:
            _to_xml(*args, **kwargs)
        self.assertIn("missing required arguments: data", str(error.exception))

    def test_invalid_engine(self):
        """Check passing invalid argspec"""

        # missing required arguments
        args = ["", VALID_DATA, "test"]
        kwargs = {}
        with self.assertRaises(AnsibleError) as error:
            _to_xml(*args, **kwargs)
        self.assertIn("engine: test is not supported", str(error.exception))

    def test_indent_with_spaces(self):
        """Check passing indent with spaces and default indent_width"""
        self.maxDiff = None
        args = ["", VALID_DATA, "xmltodict", "spaces", 4]
        result = _to_xml(*args)
        self.assertEqual(result, OUTPUT_SPACES)

    def test_invalid_indent(self):
        """Check passing invalid indent value"""

        # missing required arguments
        args = ["", VALID_DATA, "xmltodict", "test"]
        kwargs = {}
        with self.assertRaises(AnsibleError) as error:
            _to_xml(*args, **kwargs)
        self.assertIn(
            "value of indent must be one of: tabs, spaces, got: test",
            str(error.exception),
        )
