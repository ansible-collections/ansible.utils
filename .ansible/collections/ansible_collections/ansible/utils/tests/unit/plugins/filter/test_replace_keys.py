# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest import TestCase

from ansible.errors import AnsibleFilterError

from ansible_collections.ansible.utils.plugins.filter.replace_keys import _replace_keys


class TestReplaceKeys(TestCase):
    def setUp(self):
        pass

    def test_replace_filter_plugin(self):
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
        target = [
            {"before": "interface_name", "after": "name"},
            {"before": "is_enabled", "after": "enabled"},
        ]
        output = [
            {
                "duplex": "auto",
                "enabled": True,
                "speed": "auto",
                "name": "eth0",
            },
            {
                "vifs": [
                    {
                        "enabled": True,
                        "description": "Eth1 - VIF 100",
                        "vlan_id": 100,
                        "mtu": 400,
                    },
                    {
                        "enabled": True,
                        "description": "Eth1 - VIF 101",
                        "vlan_id": 101,
                    },
                ],
                "description": "Configured by Ansible - Interface 1",
                "duplex": "auto",
                "enabled": True,
                "mtu": 1500,
                "speed": "auto",
                "name": "eth1",
            },
            {
                "description": "Configured by Ansible - Interface 2 (ADMIN DOWN)",
                "enabled": True,
                "mtu": 600,
                "name": "eth2",
            },
        ]
        args = ["", data, target]

        result = _replace_keys(*args)
        self.assertEqual(result, output)

    def test_replace_filter_match_starts_with_plugin(self):
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
        target = [
            {"before": "interface", "after": "name"},
            {"before": "is", "after": "enabled"},
        ]
        output = [
            {
                "duplex": "auto",
                "enabled": True,
                "speed": "auto",
                "name": "eth0",
            },
            {
                "vifs": [
                    {
                        "enabled": True,
                        "description": "Eth1 - VIF 100",
                        "vlan_id": 100,
                        "mtu": 400,
                    },
                    {
                        "enabled": True,
                        "description": "Eth1 - VIF 101",
                        "vlan_id": 101,
                    },
                ],
                "description": "Configured by Ansible - Interface 1",
                "duplex": "auto",
                "enabled": True,
                "mtu": 1500,
                "speed": "auto",
                "name": "eth1",
            },
            {
                "description": "Configured by Ansible - Interface 2 (ADMIN DOWN)",
                "enabled": True,
                "mtu": 600,
                "name": "eth2",
            },
        ]
        args = ["", data, target, "starts_with"]

        result = _replace_keys(*args)
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
        target = [
            {"before": "ame", "after": "name"},
            {"before": "enabled", "after": "enabled"},
        ]
        output = [
            {
                "duplex": "auto",
                "enabled": True,
                "speed": "auto",
                "name": "eth0",
            },
            {
                "vifs": [
                    {
                        "enabled": True,
                        "description": "Eth1 - VIF 100",
                        "vlan_id": 100,
                        "mtu": 400,
                    },
                    {
                        "enabled": True,
                        "description": "Eth1 - VIF 101",
                        "vlan_id": 101,
                    },
                ],
                "description": "Configured by Ansible - Interface 1",
                "duplex": "auto",
                "enabled": True,
                "mtu": 1500,
                "speed": "auto",
                "name": "eth1",
            },
            {
                "description": "Configured by Ansible - Interface 2 (ADMIN DOWN)",
                "enabled": True,
                "mtu": 600,
                "name": "eth2",
            },
        ]
        args = ["", data, target, "ends_with"]

        result = _replace_keys(*args)
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
        target = [
            {"before": "^interface_name$", "after": "name"},
            {"before": "is_enabled", "after": "enabled"},
        ]
        output = [
            {
                "duplex": "auto",
                "enabled": True,
                "speed": "auto",
                "name": "eth0",
            },
            {
                "vifs": [
                    {
                        "enabled": True,
                        "description": "Eth1 - VIF 100",
                        "vlan_id": 100,
                        "mtu": 400,
                    },
                    {
                        "enabled": True,
                        "description": "Eth1 - VIF 101",
                        "vlan_id": 101,
                    },
                ],
                "description": "Configured by Ansible - Interface 1",
                "duplex": "auto",
                "enabled": True,
                "mtu": 1500,
                "speed": "auto",
                "name": "eth1",
            },
            {
                "description": "Configured by Ansible - Interface 2 (ADMIN DOWN)",
                "enabled": True,
                "mtu": 600,
                "name": "eth2",
            },
        ]
        args = ["", data, target, "regex"]

        result = _replace_keys(*args)
        self.assertEqual(result, output)

    def test_invalid_data(self):
        self.maxDiff = None
        target = [{"before": "pre", "after": "post"}]
        args = ["", "string data", target]
        with self.assertRaises(AnsibleFilterError) as error:
            _replace_keys(*args)
        self.assertIn("Error when using plugin 'replace_keys'", str(error.exception))
