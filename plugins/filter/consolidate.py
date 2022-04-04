#
# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

"""
The consolidate filter plugin
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: consolidate
    author: Sagar Paul (@KB-perByte)
    version_added: "2.5.0"
    short_description: Keep specific keys from a data recursively.
    description:
        - This plugin keep only specified keys from a provided data recursively.
        - Matching parameter defaults to equals unless C(matching_parameter) is explicitly mentioned.
        - Using the parameters below- C(data|ansible.utils.keep_keys(target([....])))
    options:
      data_source:
        description:
        - This option represents a list of dictionaries or a dictionary with any level of nesting data.
        - For example C(config_data|ansible.utils.keep_keys(target([....]))), in this case C(config_data) represents this option.
        type: list
        elements: dict
        suboptions:
          data:
            description: Specify the target keys to keep in list format.
            type: raw
          match_key:
            description: Specify the target keys to keep in list format.
            type: str
          prefix:
            description: Specify the target keys to keep in list format.
            type: str
      fail_missing_match_key:
        description: Specify the target keys to keep in list format.
        type: bool
      fail_missing_match_value:
        description: Specify the target keys to keep in list format.
        type: bool
      fail_duplicate:
        description: Specify the matching configuration of target keys and data attributes.
        type: bool
"""

EXAMPLES = r"""

##example.yaml
interfaces:
  - name: eth0
    enabled: true
    duplex: auto
    speed: auto
    note:
      - Connected green wire
  - name: eth1
    description: Configured by Ansible - Interface 1
    mtu: 1500
    speed: auto
    duplex: auto
    enabled: true
    note:
      - Connected blue wire
      - Configured by Paul
    vifs:
    - vlan_id: 100
      description: Eth1 - VIF 100
      mtu: 400
      enabled: true
      comment: Needs reconfiguration
    - vlan_id: 101
      description: Eth1 - VIF 101
      enabled: true
  - name: eth2
    description: Configured by Ansible - Interface 2 (ADMIN DOWN)
    mtu: 600
    enabled: false

##Playbook
vars_files:
  - "example.yaml"
tasks:
  - name: keep selective keys from dict/list of dict data
    ansible.builtin.set_fact:
      data: "{{ interfaces }}"

  - debug:
      msg:  "{{ data|ansible.utils.keep_keys(target=['description', 'name', 'mtu', 'duplex', 'enabled', 'vifs', 'vlan_id']) }}"

##Output
# TASK [keep selective keys from python dict/list of dict] ****************************************************************************************
# ok: [localhost] => {
#     "ansible_facts": {
#         "data": [
#             {
#                 "duplex": "auto",
#                 "enabled": true,
#                 "name": "eth0",
#                 "note": [
#                     "Connected green wire"
#                 ],
#                 "speed": "auto"
#             },
#             {
#                 "description": "Configured by Ansible - Interface 1",
#                 "duplex": "auto",
#                 "enabled": true,
#                 "mtu": 1500,
#                 "name": "eth1",
#                 "note": [
#                     "Connected blue wire",
#                     "Configured by Paul"
#                 ],
#                 "speed": "auto",
#                 "vifs": [
#                     {
#                         "comment": "Needs reconfiguration",
#                         "description": "Eth1 - VIF 100",
#                         "enabled": true,
#                         "mtu": 400,
#                         "vlan_id": 100
#                     },
#                     {
#                         "description": "Eth1 - VIF 101",
#                         "enabled": true,
#                         "vlan_id": 101
#                     }
#                 ]
#             },
#             {
#                 "description": "Configured by Ansible - Interface 2 (ADMIN DOWN)",
#                 "enabled": false,
#                 "mtu": 600,
#                 "name": "eth2"
#             }
#         ]
#     },
#     "changed": false
# }
# Read vars_file 'example.yaml'

# TASK [debug] *************************************************************************************************************
# ok: [localhost] => {
#     "msg": [
#         {
#             "duplex": "auto",
#             "enabled": true,
#             "name": "eth0"
#         },
#         {
#             "description": "Configured by Ansible - Interface 1",
#             "duplex": "auto",
#             "enabled": true,
#             "mtu": 1500,
#             "name": "eth1",
#             "vifs": [
#                 {
#                     "description": "Eth1 - VIF 100",
#                     "enabled": true,
#                     "mtu": 400,
#                     "vlan_id": 100
#                 },
#                 {
#                     "description": "Eth1 - VIF 101",
#                     "enabled": true,
#                     "vlan_id": 101
#                 }
#             ]
#         },
#         {
#             "description": "Configured by Ansible - Interface 2 (ADMIN DOWN)",
#             "enabled": false,
#             "mtu": 600,
#             "name": "eth2"
#         }
#     ]
# }

##example.yaml
interfaces:
  - name: eth0
    enabled: true
    duplex: auto
    speed: auto
    note:
      - Connected green wire
  - name: eth1
    description: Configured by Ansible - Interface 1
    mtu: 1500
    speed: auto
    duplex: auto
    enabled: true
    note:
      - Connected blue wire
      - Configured by Paul
    vifs:
    - vlan_id: 100
      description: Eth1 - VIF 100
      mtu: 400
      enabled: true
      comment: Needs reconfiguration
    - vlan_id: 101
      description: Eth1 - VIF 101
      enabled: true
  - name: eth2
    description: Configured by Ansible - Interface 2 (ADMIN DOWN)
    mtu: 600
    enabled: false

##Playbook
vars_files:
  - "example.yaml"
tasks:
  - name: keep selective keys from dict/list of dict data
    ansible.builtin.set_fact:
      data: "{{ interfaces }}"

  - debug:
      msg:  "{{ data|ansible.utils.keep_keys(target=['desc', 'name'], matching_parameter= 'starts_with') }}"

##Output
# TASK [keep selective keys from python dict/list of dict] **************************
# ok: [localhost] => {
#     "ansible_facts": {
#         "data": [
#             {
#                 "duplex": "auto",
#                 "enabled": true,
#                 "name": "eth0",
#                 "note": [
#                     "Connected green wire"
#                 ],
#                 "speed": "auto"
#             },
#             {
#                 "description": "Configured by Ansible - Interface 1",
#                 "duplex": "auto",
#                 "enabled": true,
#                 "mtu": 1500,
#                 "name": "eth1",
#                 "note": [
#                     "Connected blue wire",
#                     "Configured by Paul"
#                 ],
#                 "speed": "auto",
#                 "vifs": [
#                     {
#                         "comment": "Needs reconfiguration",
#                         "description": "Eth1 - VIF 100",
#                         "enabled": true,
#                         "mtu": 400,
#                         "vlan_id": 100
#                     },
#                     {
#                         "description": "Eth1 - VIF 101",
#                         "enabled": true,
#                         "vlan_id": 101
#                     }
#                 ]
#             },
#             {
#                 "description": "Configured by Ansible - Interface 2 (ADMIN DOWN)",
#                 "enabled": false,
#                 "mtu": 600,
#                 "name": "eth2"
#             }
#         ]
#     },
#     "changed": false
# }
# Read vars_file 'example.yaml'

# TASK [debug] **********************************************************************************
# ok: [localhost] => {
#     "msg": [
#         {
#             "name": "eth0"
#         },
#         {
#             "description": "Configured by Ansible - Interface 1",
#             "name": "eth1",
#             "vifs": [
#                 {
#                     "description": "Eth1 - VIF 100"
#                 },
#                 {
#                     "description": "Eth1 - VIF 101"
#                 }
#             ]
#         },
#         {
#             "description": "Configured by Ansible - Interface 2 (ADMIN DOWN)",
#             "name": "eth2"
#         }
#     ]
# }
"""

from ansible.errors import AnsibleFilterError
from ansible_collections.ansible.utils.plugins.plugin_utils.consolidate import (
    consolidate,
)
from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
    AnsibleArgSpecValidator,
)

try:
    from jinja2.filters import pass_environment
except ImportError:
    from jinja2.filters import environmentfilter as pass_environment

import debugpy

debugpy.listen(3000)
debugpy.wait_for_client()


@pass_environment
def _consolidate(*args, **kwargs):
    """keep specific keys from a data recursively"""

    keys = [
        "data_source",
        "fail_missing_match_key",
        "fail_missing_match_value",
        "fail_duplicate",
    ]
    data = dict(zip(keys, args[1:]))
    data.update(kwargs)
    aav = AnsibleArgSpecValidator(
        data=data, schema=DOCUMENTATION, name="consolidate"
    )
    valid, errors, updated_data = aav.validate()
    if not valid:
        raise AnsibleFilterError(errors)
    return consolidate(**updated_data)


class FilterModule(object):
    """keep_keys"""

    def filters(self):

        """a mapping of filter names to functions"""
        return {"consolidate": _consolidate}
