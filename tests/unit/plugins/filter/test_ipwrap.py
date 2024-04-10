# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit test file for ipwrap filter plugin
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest import TestCase

import pytest

from ansible.errors import AnsibleFilterError
from ansible.template import AnsibleUndefined

from ansible_collections.ansible.utils.plugins.filter.ipwrap import _ipwrap


VALID_DATA = [
    "192.24.2.1",
    "host.fqdn",
    "::1",
    "",
    "192.168.32.0/24",
    "fe80::100/10",
    "42540766412265424405338506004571095040/64",
    True,
]


VALID_OUTPUT = [
    "192.24.2.1",
    "host.fqdn",
    "[::1]",
    "",
    "192.168.32.0/24",
    "[fe80::100]/10",
    "[2001:db8:32c:faad::]/64",
    True,
]


class TestIpWrap(TestCase):
    def setUp(self):
        pass

    def test_ipwrap_undefined_value(self):
        """Check ipwrap filter undefined value"""
        args = ["", AnsibleUndefined(name="my_ip"), ""]
        with pytest.raises(
            AnsibleFilterError,
            match="Unrecognized type <<class 'ansible.template.AnsibleUndefined'>> for ipwrap filter <value>",
        ):
            _ipwrap(*args)

    def test_valid_data_list(self):
        """Check passing valid argspec(list)"""
        args = ["", VALID_DATA, ""]
        result = _ipwrap(*args)
        print(result)
        self.assertEqual(result, VALID_OUTPUT)

    def test_valid_data_string(self):
        """Check passing valid argspec(string)"""

        args = ["", "::1", ""]
        result = _ipwrap(*args)
        self.assertEqual(result, "[::1]")
