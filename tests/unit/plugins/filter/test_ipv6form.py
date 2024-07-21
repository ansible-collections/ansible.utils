# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit test file for ipcut filter plugin
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest import TestCase

from ansible_collections.ansible.utils.plugins.filter.ipv6form import _ipv6form


class TestIpv6Form(TestCase):
    def setUp(self):
        pass

    def test_expand(self):
        """Expand given ipv6 address"""

        args = ["", "1234:4321:abcd:dcba::17", "expand"]
        result = _ipv6form(*args)
        self.assertEqual(result, "1234:4321:abcd:dcba:0000:0000:0000:0017")

    def test_compress(self):
        """Compress given ipv6 address"""

        args = ["", "1234:4321:abcd:dcba:0000:0000:0000:0017", "compress"]
        result = _ipv6form(*args)
        self.assertEqual(result, "1234:4321:abcd:dcba::17")

    def test_x509(self):
        """Compress given ipv6 address into x509 form"""

        args = ["", "1234:4321:abcd:dcba::17", "x509"]
        result = _ipv6form(*args)
        self.assertEqual(result, "1234:4321:abcd:dcba:0:0:0:17")
