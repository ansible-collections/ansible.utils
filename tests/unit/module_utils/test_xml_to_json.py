# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import unittest
from ansible.errors import AnsibleError
from ansible_collections.ansible.utils.plugins.filter.xml_to_json import (
    xml_to_json,
)

INVALID_DATA = '<netconf-state xmlns="urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring">'

VALID_DATA = (
    '<netconf-state xmlns="urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring">'
    "<schemas><schema/></schemas></netconf-state>"
)


class TestXmlToJson(unittest.TestCase):
    def setUp(self):
        pass

    def test_invalid_data(self):
        """Check passing invalid argspec"""

        # missing required arguments
        args = [INVALID_DATA, "xmltodict"]
        kwargs = {}
        with self.assertRaises(AnsibleError) as error:
            xml_to_json(*args, **kwargs)
        print(str(error.exception))
        self.assertIn(
            "Error when using plugin 'xml_to_json': Input Xml is not valid",
            str(error.exception),
        )

    def test_valid_data(self):
        """Check passing valid data as per criteria"""
        self.maxDiff = None
        output = """{"netconf-state": {"@xmlns": "urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring",
        "schemas": {"schema": null}}}"""
        args = [VALID_DATA, "xmltodict"]
        result = xml_to_json(*args)
        self.assertEqual(result, output)
