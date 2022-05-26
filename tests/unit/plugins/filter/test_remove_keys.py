# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

import unittest

from ansible.errors import AnsibleFilterError

from ansible_collections.ansible.utils.plugins.filter.remove_keys import _remove_keys


class TestReplaceKeys(unittest.TestCase):
    def setUp(self):
        pass

    def test_remove_filter_plugin(self):
        data = [
            {
                "duplex": "auto",
                "enabled": True,
                "interface_name": "eth0",
                "speed": "auto",
                "extra": "remove extra",
            },
            {
                "description": "Configured by Ansible - Interface 1",
                "duplex": "auto",
                "interface_name": "eth1",
                "is_enabled": True,
                "mtu": 1500,
                "speed": "auto",
                "vifs": [
                    {
                        "description": "Eth1 - VIF 100",
                        "is_enabled": True,
                        "mtu": 400,
                        "vlan_id": 100,
                        "comment": ["comment A", "comment B"],
                    },
                    {
                        "description": "Eth1 - VIF 101",
                        "is_enabled": True,
                        "vlan_id": 101,
                    },
                ],
            },
            {
                "description": "Configured by Ansible - Interface 2 (ADMIN DOWN)",
                "interface_name": "eth2",
                "is_enabled": True,
                "mtu": 600,
            },
        ]
        target = ["extra", "comment"]
        output = [
            {
                "duplex": "auto",
                "enabled": True,
                "interface_name": "eth0",
                "speed": "auto",
            },
            {
                "is_enabled": True,
                "vifs": [
                    {
                        "is_enabled": True,
                        "description": "Eth1 - VIF 100",
                        "vlan_id": 100,
                        "mtu": 400,
                    },
                    {
                        "is_enabled": True,
                        "description": "Eth1 - VIF 101",
                        "vlan_id": 101,
                    },
                ],
                "description": "Configured by Ansible - Interface 1",
                "duplex": "auto",
                "mtu": 1500,
                "interface_name": "eth1",
                "speed": "auto",
            },
            {
                "is_enabled": True,
                "interface_name": "eth2",
                "description": "Configured by Ansible - Interface 2 (ADMIN DOWN)",
                "mtu": 600,
            },
        ]
        args = ["", data, target]

        result = _remove_keys(*args)
        self.assertEqual(result, output)

    def test_remove_filter_match_starts_with_plugin(self):
        data = [
            {
                "duplex": "auto",
                "enabled": True,
                "interface_name": "eth0",
                "speed": "auto",
            },
            {
                "description": "Configured by Ansible - Interface 1",
                "duplex": "auto",
                "interface_name": "eth1",
                "is_enabled": True,
                "mtu": 1500,
                "speed": "auto",
                "vifs": [
                    {
                        "description": "Eth1 - VIF 100",
                        "is_enabled": True,
                        "mtu": 400,
                        "vlan_id": 100,
                    },
                    {
                        "description": "Eth1 - VIF 101",
                        "is_enabled": True,
                        "vlan_id": 101,
                    },
                ],
            },
            {
                "description": "Configured by Ansible - Interface 2 (ADMIN DOWN)",
                "interface_name": "eth2",
                "is_enabled": True,
                "mtu": 600,
            },
        ]
        target = ["is_"]
        output = [
            {
                "duplex": "auto",
                "enabled": True,
                "interface_name": "eth0",
                "speed": "auto",
            },
            {
                "vifs": [
                    {
                        "description": "Eth1 - VIF 100",
                        "vlan_id": 100,
                        "mtu": 400,
                    },
                    {"description": "Eth1 - VIF 101", "vlan_id": 101},
                ],
                "description": "Configured by Ansible - Interface 1",
                "duplex": "auto",
                "mtu": 1500,
                "interface_name": "eth1",
                "speed": "auto",
            },
            {
                "interface_name": "eth2",
                "description": "Configured by Ansible - Interface 2 (ADMIN DOWN)",
                "mtu": 600,
            },
        ]
        args = ["", data, target, "starts_with"]

        result = _remove_keys(*args)
        self.assertEqual(result, output)

    def test_replace_filter_match_ends_with_plugin(self):
        data = [
            {
                "duplex": "auto",
                "enabled": True,
                "interface_name": "eth0",
                "speed": "auto",
            },
            {
                "description": "Configured by Ansible - Interface 1",
                "duplex": "auto",
                "interface_name": "eth1",
                "is_enabled": True,
                "mtu": 1500,
                "speed": "auto",
                "vifs": [
                    {
                        "description": "Eth1 - VIF 100",
                        "is_enabled": True,
                        "mtu": 400,
                        "vlan_id": 100,
                    },
                    {
                        "description": "Eth1 - VIF 101",
                        "is_enabled": True,
                        "vlan_id": 101,
                    },
                ],
            },
            {
                "description": "Configured by Ansible - Interface 2 (ADMIN DOWN)",
                "interface_name": "eth2",
                "is_enabled": True,
                "mtu": 600,
            },
        ]
        target = ["_enabled"]
        output = [
            {
                "duplex": "auto",
                "enabled": True,
                "interface_name": "eth0",
                "speed": "auto",
            },
            {
                "vifs": [
                    {
                        "description": "Eth1 - VIF 100",
                        "vlan_id": 100,
                        "mtu": 400,
                    },
                    {"description": "Eth1 - VIF 101", "vlan_id": 101},
                ],
                "description": "Configured by Ansible - Interface 1",
                "duplex": "auto",
                "mtu": 1500,
                "interface_name": "eth1",
                "speed": "auto",
            },
            {
                "interface_name": "eth2",
                "description": "Configured by Ansible - Interface 2 (ADMIN DOWN)",
                "mtu": 600,
            },
        ]
        args = ["", data, target, "ends_with"]

        result = _remove_keys(*args)
        self.assertEqual(result, output)

    def test_replace_filter_match_regex_plugin(self):
        data = [
            {
                "duplex": "auto",
                "enabled": True,
                "interface_name": "eth0",
                "speed": "auto",
            },
            {
                "description": "Configured by Ansible - Interface 1",
                "duplex": "auto",
                "interface_name": "eth1",
                "is_enabled": True,
                "mtu": 1500,
                "speed": "auto",
                "vifs": [
                    {
                        "description": "Eth1 - VIF 100",
                        "is_enabled": True,
                        "mtu": 400,
                        "vlan_id": 100,
                    },
                    {
                        "description": "Eth1 - VIF 101",
                        "is_enabled": True,
                        "vlan_id": 101,
                    },
                ],
            },
            {
                "description": "Configured by Ansible - Interface 2 (ADMIN DOWN)",
                "interface_name": "eth2",
                "is_enabled": True,
                "mtu": 600,
            },
        ]
        target = ["^desc"]
        output = [
            {
                "duplex": "auto",
                "enabled": True,
                "interface_name": "eth0",
                "speed": "auto",
            },
            {
                "is_enabled": True,
                "vifs": [
                    {"is_enabled": True, "vlan_id": 100, "mtu": 400},
                    {"is_enabled": True, "vlan_id": 101},
                ],
                "duplex": "auto",
                "mtu": 1500,
                "interface_name": "eth1",
                "speed": "auto",
            },
            {"is_enabled": True, "interface_name": "eth2", "mtu": 600},
        ]
        args = ["", data, target, "regex"]

        result = _remove_keys(*args)
        self.assertEqual(result, output)

    def test_invalid_data(self):
        self.maxDiff = None
        target = [{"before": "pre", "after": "post"}]
        args = ["", "string data", target]
        with self.assertRaises(AnsibleFilterError) as error:
            _remove_keys(*args)
        self.assertIn("Error when using plugin 'remove_keys'", str(error.exception))
