# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit test file for slaac filter plugin
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest import TestCase

from ansible_collections.ansible.utils.plugins.filter.slaac import _slaac


class Test_slaac(TestCase):
    def setUp(self):
        pass

    def test_slaac_filter_1(self):
        """slaac filter"""
        args = [
            "",
            "fdcf:1894:23b5:d38c:0000:0000:0000:0000",
            "c2:31:b3:83:bf:2b",
        ]
        result = _slaac(*args)
        self.assertEqual(result, "fdcf:1894:23b5:d38c:c031:b3ff:fe83:bf2b")
