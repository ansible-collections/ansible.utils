# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit test file for nthhost filter plugin
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest import TestCase

from ansible_collections.ansible.utils.plugins.filter.nthhost import _nthhost


class Test_nthhost(TestCase):
    def setUp(self):
        pass

    def test_nthhost_filter_1(self):
        """nthhost filter"""
        args = ["", "10.0.0.0/8", "305"]
        result = _nthhost(*args)
        self.assertEqual(result, "10.0.1.49")

    def test_nthhost_filter_2(self):
        """nthhost filter"""
        args = ["", "10.0.0.0/8", "-1"]
        result = _nthhost(*args)
        self.assertEqual(result, "10.255.255.255")
