# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

import unittest

from ansible.errors import AnsibleFilterError

from ansible_collections.ansible.utils.plugins.filter.consolidate import _consolidate


class TestConsolidate(unittest.TestCase):
    def setUp(self):
        pass

    def test_consolidate_plugin(self):
        data_sources = [
            {
                "data": [
                    {
                        "duplex": "auto",
                        "enabled": True,
                        "name": "GigabitEthernet0/0",
                        "note": ["Connected green wire"],
                        "speed": "auto",
                    },
                    {
                        "description": "Configured by Ansible - Interface 1",
                        "duplex": "auto",
                        "enabled": True,
                        "mtu": 1500,
                        "name": "GigabitEthernet0/1",
                        "note": ["Connected blue wire", "Configured by Paul"],
                        "speed": "auto",
                        "vifs": [
                            {
                                "comment": "Needs reconfiguration",
                                "description": "Eth1 - VIF 100",
                                "enabled": True,
                                "mtu": 400,
                                "vlan_id": 100,
                            },
                            {
                                "description": "Eth1 - VIF 101",
                                "enabled": True,
                                "vlan_id": 101,
                            },
                        ],
                    },
                    {
                        "description": "Configured by Ansible - Interface 2 (ADMIN DOWN)",
                        "enabled": False,
                        "mtu": 600,
                        "name": "GigabitEthernet0/2",
                    },
                ],
                "match_key": "name",
                "name": "interfaces",
            },
            {
                "data": [
                    {"name": "GigabitEthernet0/0"},
                    {
                        "mode": "access",
                        "name": "GigabitEthernet0/1",
                        "trunk": {
                            "allowed_vlans": [
                                "11",
                                "12",
                                "59",
                                "67",
                                "75",
                                "77",
                                "81",
                                "100",
                                "400-408",
                                "411-413",
                                "415",
                                "418",
                                "982",
                                "986",
                                "988",
                                "993",
                            ],
                        },
                    },
                    {
                        "mode": "trunk",
                        "name": "GigabitEthernet0/2",
                        "trunk": {
                            "allowed_vlans": [
                                "11",
                                "12",
                                "59",
                                "67",
                                "75",
                                "77",
                                "81",
                                "100",
                                "400-408",
                                "411-413",
                                "415",
                                "418",
                                "982",
                                "986",
                                "988",
                                "993",
                            ],
                            "encapsulation": "dot1q",
                        },
                    },
                ],
                "match_key": "name",
                "name": "l2_interfaces",
            },
            {
                "data": [
                    {
                        "ipv4": [{"address": "192.168.0.2/24"}],
                        "name": "GigabitEthernet0/0",
                    },
                    {"name": "GigabitEthernet0/1"},
                    {"name": "GigabitEthernet0/2"},
                    {"name": "Loopback888"},
                    {"name": "Loopback999"},
                ],
                "match_key": "name",
                "name": "l3_interfaces",
            },
        ]

        output = {
            "GigabitEthernet0/0": {
                "interfaces": {
                    "duplex": "auto",
                    "enabled": True,
                    "name": "GigabitEthernet0/0",
                    "note": ["Connected green wire"],
                    "speed": "auto",
                },
                "l2_interfaces": {"name": "GigabitEthernet0/0"},
                "l3_interfaces": {
                    "ipv4": [{"address": "192.168.0.2/24"}],
                    "name": "GigabitEthernet0/0",
                },
            },
            "GigabitEthernet0/1": {
                "interfaces": {
                    "description": "Configured by Ansible - Interface 1",
                    "duplex": "auto",
                    "enabled": True,
                    "mtu": 1500,
                    "name": "GigabitEthernet0/1",
                    "note": ["Connected blue wire", "Configured by Paul"],
                    "speed": "auto",
                    "vifs": [
                        {
                            "comment": "Needs reconfiguration",
                            "description": "Eth1 - VIF 100",
                            "enabled": True,
                            "mtu": 400,
                            "vlan_id": 100,
                        },
                        {
                            "description": "Eth1 - VIF 101",
                            "enabled": True,
                            "vlan_id": 101,
                        },
                    ],
                },
                "l2_interfaces": {
                    "mode": "access",
                    "name": "GigabitEthernet0/1",
                    "trunk": {
                        "allowed_vlans": [
                            "11",
                            "12",
                            "59",
                            "67",
                            "75",
                            "77",
                            "81",
                            "100",
                            "400-408",
                            "411-413",
                            "415",
                            "418",
                            "982",
                            "986",
                            "988",
                            "993",
                        ],
                    },
                },
                "l3_interfaces": {"name": "GigabitEthernet0/1"},
            },
            "GigabitEthernet0/2": {
                "interfaces": {
                    "description": "Configured by Ansible - Interface 2 (ADMIN DOWN)",
                    "enabled": False,
                    "mtu": 600,
                    "name": "GigabitEthernet0/2",
                },
                "l2_interfaces": {
                    "mode": "trunk",
                    "name": "GigabitEthernet0/2",
                    "trunk": {
                        "allowed_vlans": [
                            "11",
                            "12",
                            "59",
                            "67",
                            "75",
                            "77",
                            "81",
                            "100",
                            "400-408",
                            "411-413",
                            "415",
                            "418",
                            "982",
                            "986",
                            "988",
                            "993",
                        ],
                        "encapsulation": "dot1q",
                    },
                },
                "l3_interfaces": {"name": "GigabitEthernet0/2"},
            },
            "Loopback888": {
                "interfaces": {},
                "l2_interfaces": {},
                "l3_interfaces": {"name": "Loopback888"},
            },
            "Loopback999": {
                "interfaces": {},
                "l2_interfaces": {},
                "l3_interfaces": {"name": "Loopback999"},
            },
        }
        fail_missing_match_value = False
        fail_missing_match_key = False
        fail_duplicate = False
        args = [
            "",
            data_sources,
            fail_missing_match_key,
            fail_missing_match_value,
            fail_duplicate,
        ]

        result = _consolidate(*args)
        self.assertEqual(result, output)

    def test_fail_missing_match_key(self):
        data_sources = [
            {
                "data": [
                    {
                        "duplex": "auto",
                        "enabled": True,
                        "name": "GigabitEthernet0/0",
                        "note": ["Connected green wire"],
                        "speed": "auto",
                    },
                    {
                        "description": "Configured by Ansible - Interface 1",
                        "duplex": "auto",
                        "enabled": True,
                        "mtu": 1500,
                        "name": "GigabitEthernet0/1",
                        "note": ["Connected blue wire", "Configured by Paul"],
                        "speed": "auto",
                        "vifs": [
                            {
                                "comment": "Needs reconfiguration",
                                "description": "Eth1 - VIF 100",
                                "enabled": True,
                                "mtu": 400,
                                "vlan_id": 100,
                            },
                            {
                                "description": "Eth1 - VIF 101",
                                "enabled": True,
                                "vlan_id": 101,
                            },
                        ],
                    },
                    {
                        "description": "Configured by Ansible - Interface 2 (ADMIN DOWN)",
                        "enabled": False,
                        "mtu": 600,
                        "name": "GigabitEthernet0/2",
                    },
                ],
                "match_key": "name",
                "name": "interfaces",
            },
            {
                "data": [
                    {"name": "GigabitEthernet0/0"},
                    {
                        "mode": "access",
                        "name": "GigabitEthernet0/1",
                        "trunk": {
                            "allowed_vlans": [
                                "11",
                                "12",
                                "59",
                                "67",
                                "75",
                                "77",
                                "81",
                                "100",
                                "400-408",
                                "411-413",
                                "415",
                                "418",
                                "982",
                                "986",
                                "988",
                                "993",
                            ],
                        },
                    },
                    {
                        "mode": "trunk",
                        "name": "GigabitEthernet0/2",
                        "trunk": {
                            "allowed_vlans": [
                                "11",
                                "12",
                                "59",
                                "67",
                                "75",
                                "77",
                                "81",
                                "100",
                                "400-408",
                                "411-413",
                                "415",
                                "418",
                                "982",
                                "986",
                                "988",
                                "993",
                            ],
                            "encapsulation": "dot1q",
                        },
                    },
                ],
                "match_key": "name",
                "name": "l2_interfaces",
            },
            {
                "data": [
                    {
                        "ipv4": [{"address": "192.168.0.2/24"}],
                        "intf_name": "GigabitEthernet0/0",
                    },
                    {"name": "GigabitEthernet0/1"},
                    {"name": "GigabitEthernet0/2"},
                    {"name": "Loopback888"},
                    {"name": "Loopback999"},
                ],
                "match_key": "name",
                "name": "l3_interfaces",
            },
        ]

        fail_missing_match_key = True
        args = ["", data_sources, fail_missing_match_key, False, False]
        with self.assertRaises(AnsibleFilterError) as error:
            _consolidate(*args)
        self.assertIn(
            "Error when using plugin 'consolidate': 'fail_missing_match_key' reported missing match key 'name' in data source 3 in list entry 1",
            str(error.exception),
        )

    def test_fail_duplicate(self):
        data_sources = [
            {
                "data": [
                    {
                        "duplex": "auto",
                        "enabled": True,
                        "name": "GigabitEthernet0/0",
                        "note": ["Connected green wire"],
                        "speed": "auto",
                    },
                    {
                        "description": "Configured by Ansible - Interface 1",
                        "duplex": "auto",
                        "enabled": True,
                        "mtu": 1500,
                        "name": "GigabitEthernet0/1",
                        "note": ["Connected blue wire", "Configured by Paul"],
                        "speed": "auto",
                        "vifs": [
                            {
                                "comment": "Needs reconfiguration",
                                "description": "Eth1 - VIF 100",
                                "enabled": True,
                                "mtu": 400,
                                "vlan_id": 100,
                            },
                            {
                                "description": "Eth1 - VIF 101",
                                "enabled": True,
                                "vlan_id": 101,
                            },
                        ],
                    },
                    {
                        "description": "Configured by Ansible - Interface 2 (ADMIN DOWN)",
                        "enabled": False,
                        "mtu": 600,
                        "name": "GigabitEthernet0/2",
                    },
                ],
                "match_key": "name",
                "name": "interfaces",
            },
            {
                "data": [
                    {"name": "GigabitEthernet0/0"},
                    {
                        "mode": "access",
                        "name": "GigabitEthernet0/1",
                        "trunk": {
                            "allowed_vlans": [
                                "11",
                                "12",
                                "59",
                                "67",
                                "75",
                                "77",
                                "81",
                                "100",
                                "400-408",
                                "411-413",
                                "415",
                                "418",
                                "982",
                                "986",
                                "988",
                                "993",
                            ],
                        },
                    },
                    {
                        "mode": "trunk",
                        "name": "GigabitEthernet0/2",
                        "trunk": {
                            "allowed_vlans": [
                                "11",
                                "12",
                                "59",
                                "67",
                                "75",
                                "77",
                                "81",
                                "100",
                                "400-408",
                                "411-413",
                                "415",
                                "418",
                                "982",
                                "986",
                                "988",
                                "993",
                            ],
                            "encapsulation": "dot1q",
                        },
                    },
                ],
                "match_key": "name",
                "name": "l2_interfaces",
            },
            {
                "data": [
                    {
                        "ipv4": [{"address": "192.168.0.2/24"}],
                        "name": "GigabitEthernet0/0",
                    },
                    {
                        "ipv4": [{"address": "192.168.0.3/24"}],
                        "name": "GigabitEthernet0/0",
                    },
                    {"name": "GigabitEthernet0/1"},
                    {"name": "GigabitEthernet0/2"},
                    {"name": "Loopback888"},
                    {"name": "Loopback999"},
                ],
                "match_key": "name",
                "name": "l3_interfaces",
            },
        ]

        fail_missing_match_value = False
        fail_missing_match_key = False
        fail_duplicate = True
        args = [
            "",
            data_sources,
            fail_missing_match_key,
            fail_missing_match_value,
            fail_duplicate,
        ]
        with self.assertRaises(AnsibleFilterError) as error:
            _consolidate(*args)
        self.assertIn(
            "Error when using plugin 'consolidate': 'fail_duplicate' reported duplicate values in data source 3",
            str(error.exception),
        )
