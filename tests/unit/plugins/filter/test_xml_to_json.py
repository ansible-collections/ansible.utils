# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import unittest

from ansible.errors import AnsibleFilterError
from ansible_collections.ansible.utils.plugins.filter.xml_to_json import xml_to_json

DATA = {
    "engine": "xmltodict"
}

VALID_DATA = "<netconf-state xmlns=\"urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring\">" \
             "<schemas><schema/></schemas></netconf-state>"

class TestXmlToJson(unittest.TestCase):
    def setUp(self):
        pass

    def test_invalid_argspec(self):
        """Check passing invalid argspec"""

        # missing required arguments
        args = [DATA]
        kwargs = {}
        with self.assertRaises(AnsibleFilterError) as error:
            xml_to_json(*args, **kwargs)
        self.assertIn(
            "Missing either 'data' or 'criteria' value in filter input, refer 'ansible.utils.xml_to_json' filter",
            str(error.exception),
        )

        # missing required arguments
        with self.assertRaises(AnsibleFilterError) as error:
            xml_to_json([DATA])
        self.assertIn(
            "Missing either 'data' or 'engine' ", str(error.exception)
        )


    def test_valid_data(self):
        """Check passing valid data as per criteria"""

        args = [VALID_DATA, "xmltodict"]
        result = xml_to_json(*args)
        self.assertEqual(result, [])
