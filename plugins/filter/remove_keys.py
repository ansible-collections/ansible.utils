#
# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

"""
The remove_keys filter plugin
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: remove_keys
    author: Sagar Paul (@KB-perByte)
    version_added: "2.5.0"
    short_description: Remove specific keys from a data recursively.
    description:
        - This plugin removes specific keys from a provided data recursively.
        - Using the parameters below- C(data|ansible.utils.remove_keys(target([....])))
    options:
      data:
        description:
        - This option represents a list of dictionaries or a dictionary with any level of nesting data.
        - For example C(config_data|ansible.utils.remove_keys(target([....]))), in this case C(config_data) represents this option.
        type: raw
        required: True
      target:
        description: Specify the target keys to remove in list format.
        type: list
        elements: str
        required: True
      matching_parameter:
        description: Specify the matching configuration of target keys and data attributes.
        type: str
        choices: ["starts_with","ends_with","regex"]
"""

EXAMPLES = r"""

#### Simple examples with out any engine. plugin will use default value as xmltodict

tasks:
  - name: convert given XML to native python dictionary
    ansible.builtin.set_fact:
      data: "
        <netconf-state xmlns=\"urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring\"><schemas><schema/></schemas></netconf-state>
            "

  - debug:
      msg:  "{{ data|ansible.utils.from_xml }}"

##TASK######
# TASK [convert given XML to native python dictionary] *****************************************************************************************************
# task path: /Users/amhatre/ansible-collections/playbooks/test_utils.yaml:5
# ok: [localhost] => {
#     "ansible_facts": {
#         "data": " <netconf-state xmlns=\"urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring\"><schemas><schema/></schemas></netconf-state> "
#     },
#     "changed": false
# }
#
# TASK [debug] *************************************************************************************************************************
# task path: /Users/amhatre/ansible-collections/playbooks/test_utils.yaml:13
# Loading collection ansible.utils from /Users/amhatre/ansible-collections/collections/ansible_collections/ansible/utils
# ok: [localhost] => {
#     "msg": {
#         "netconf-state": {
#             "@xmlns": "urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring",
#             "schemas": {
#                 "schema": null
#             }
#         }
#     }
# }

#### example2 with engine=xmltodict

tasks:
  - name: convert given XML to native python dictionary
    ansible.builtin.set_fact:
      data: "
        <netconf-state xmlns=\"urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring\"><schemas><schema/></schemas></netconf-state>
            "

  - debug:
      msg:  "{{ data|ansible.utils.from_xml('xmltodict') }}"

##TASK######
# TASK [convert given XML to native python dictionary] *****************************************************************************************************
# task path: /Users/amhatre/ansible-collections/playbooks/test_utils.yaml:5
# ok: [localhost] => {
#     "ansible_facts": {
#         "data": " <netconf-state xmlns=\"urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring\"><schemas><schema/></schemas></netconf-state> "
#     },
#     "changed": false
# }
#
# TASK [debug] *************************************************************************************************************************
# task path: /Users/amhatre/ansible-collections/playbooks/test_utils.yaml:13
# Loading collection ansible.utils from /Users/amhatre/ansible-collections/collections/ansible_collections/ansible/utils
# ok: [localhost] => {
#     "msg": {
#         "netconf-state": {
#             "@xmlns": "urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring",
#             "schemas": {
#                 "schema": null
#             }
#         }
#     }
# }
"""

from ansible.errors import AnsibleFilterError
from ansible_collections.ansible.utils.plugins.plugin_utils.remove_keys import (
    remove_keys,
)
from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
    AnsibleArgSpecValidator,
)

try:
    from jinja2.filters import pass_environment
except ImportError:
    from jinja2.filters import environmentfilter as pass_environment


@pass_environment
def _remove_keys(*args, **kwargs):
    """remove specific keys from a data recursively"""

    keys = ["data", "target", "matching_parameter"]
    data = dict(zip(keys, args[1:]))
    data.update(kwargs)
    aav = AnsibleArgSpecValidator(data=data, schema=DOCUMENTATION, name="remove_keys")
    valid, errors, updated_data = aav.validate()
    if not valid:
        raise AnsibleFilterError(errors)
    return remove_keys(**updated_data)


class FilterModule(object):
    """remove_keys"""

    def filters(self):

        """a mapping of filter names to functions"""
        return {"remove_keys": _remove_keys}
