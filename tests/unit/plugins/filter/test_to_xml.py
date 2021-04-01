# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import unittest
from ansible.errors import AnsibleError
from ansible_collections.ansible.utils.plugins.filter.to_xml import to_xml

INVALID_DATA = '<netconf-state xmlns="urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring">'

VALID_DATA = {
    "interface-configurations": {
        "@xmlns": "http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg"
    }
}

OUTPUT = """<?xml version="1.0" encoding="utf-8"?>
<interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg"></interface-configurations>"""


class TestToXml(unittest.TestCase):
    def setUp(self):
        pass

    def test_invalid_data(self):
        """Check passing invalid argspec"""

        # missing required arguments
        args = [INVALID_DATA, "xmltodict"]
        kwargs = {}
        with self.assertRaises(AnsibleError) as error:
            to_xml(*args, **kwargs)
        print(str(error.exception))
        self.assertIn(
            "Error when using plugin 'to_xml': Input json is not valid",
            str(error.exception),
        )

    def test_valid_data(self):
        """Check passing valid data as per criteria"""
        self.maxDiff = None
        args = [VALID_DATA, "xmltodict"]
        result = to_xml(*args)
        print(result)
        self.assertEqual(result, OUTPUT)
