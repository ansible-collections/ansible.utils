# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
# from tests.unit.plugins.filter.test_from_xml import OUTPUT

__metaclass__ = type

import unittest
from ansible.errors import AnsibleError
from ansible.module_utils.common.text.converters import to_text
from ansible_collections.ansible.utils.plugins.filter.expand_usable_range import _expand_usable_range

INVALID_DATA = ['helloworld', '192.168.1.25/24', '192.0.2.0/23/24', '10.0.0.0/322']

VALID_DATA = ['10.0.0.8/30', '192.0.2.0/28']

VALID_OUTPUT_1 = {'number_of_ips': 4, 'usable_ips': ['10.0.0.8', '10.0.0.9', '10.0.0.10', '10.0.0.11']}
VALID_OUTPUT_2 = {'number_of_ips': 16, 'usable_ips': ['192.0.2.0', '192.0.2.1', '192.0.2.2', '192.0.2.3', 
                                                        '192.0.2.4', '192.0.2.5', '192.0.2.6', '192.0.2.7', 
                                                        '192.0.2.8', '192.0.2.9', '192.0.2.10', '192.0.2.11', 
                                                        '192.0.2.12', '192.0.2.13', '192.0.2.14', '192.0.2.15']}

class TestFromXml(unittest.TestCase):
    def setUp(self):
        pass

    def test_missing_data(self):
        """Check passing missing argspec"""

        # missing required arguments
        ip = ""
        with self.assertRaises(AnsibleError) as error:
            _expand_usable_range(ip)
        self.assertIn(
            "Error while using plugin 'expand_usable_range': Address cannot be empty",
            str(error.exception),
        )

    def test_invalid_data(self):
        """Check passing invalid argspec"""

        # invalid required arguments
        
        ip = INVALID_DATA[0]
        with self.assertRaises(AnsibleError) as error:
            _expand_usable_range(ip)
        self.assertIn(
            "Expected 4 octets",
            str(error.exception),
        )

        ip = INVALID_DATA[1]
        with self.assertRaises(AnsibleError) as error:
            _expand_usable_range(ip)
        self.assertIn(
            "{} has host bits set".format(ip),
            str(error.exception),
        )

        ip = INVALID_DATA[2]
        with self.assertRaises(AnsibleError) as error:
            _expand_usable_range(ip)
        self.assertIn(
            "Only one '/' permitted",
            str(error.exception),
        )

        ip = INVALID_DATA[3]
        with self.assertRaises(AnsibleError) as error:
            _expand_usable_range(ip)
        self.assertIn(
            "not a valid netmask",
            str(error.exception)
        )

    def test_valid_data(self):
        """Check passing valid data as per criteria"""
        
        ip = VALID_DATA[0]
        result = _expand_usable_range(ip)
        self.assertEqual(result, VALID_OUTPUT_1)

        ip = VALID_DATA[1]
        result = _expand_usable_range(ip)
        self.assertEqual(result, VALID_OUTPUT_2)
