# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
A test plugin file for netaddr tests
"""

from __future__ import absolute_import, division, print_function
from ansible_collections.ansible.utils.plugins.module_utils.common.ipaddress_utils import _error_not_list
from ansible_collections.ansible.utils.plugins.test.in_network import _in_network

__metaclass__ = type

DOCUMENTATION = """
    name: in_one_network
    author: Bradley Thornton (@cidrblock)
    version_added: "2.0.1"
    short_description: Test if IP address belongs in any one of the networks in the list
    description:
        - This plugin checks if the provided IP address belongs to the provided list network addresses
    options:
        ip:
            description:
            - A string that represents an IP address
            - For example: "10.1.1.1"
            type: str
            required: True
        network:
            description:
            - A list of string and each string represents a network address in CIDR form
            - For example: ['10.0.0.0/8', '192.168.1.0/24']
            type: str
            required: True

    notes:
"""

EXAMPLES = r"""

#### Simple examples

- name: Set network list
  ansible.builtin.set_fact:
    networks:
      - "10.0.0.0/8"
      - "192.168.1.0/24"

- name: Check if 10.1.1.1 is in the provided network list
  ansible.builtin.set_fact:
    data: "{{ '10.1.1.1' is ansible.utils.in_one_network networks }}"

# TASK [Check if 10.1.1.1 is in the provided network list] **********************
# ok: [localhost] => {
#     "ansible_facts": {
#         "data": true
#     },
#     "changed": false

- name: Set network list
  ansible.builtin.set_fact:
    networks:
      - "10.0.0.0/8"
      - "10.1.1.0/24"

- name: Check if 10.1.1.1 is not in the provided network list
  ansible.builtin.set_fact:
    data: "{{ '10.1.1.1' is not ansible.utils.in_one_network networks }}"

# TASK [Check if 10.1.1.1 is in not the provided network list] ************************
# ok: [localhost] => {
#     "ansible_facts": {
#         "data": true
#     },
#     "changed": false
# }

"""

RETURN = """
  data:
    description:
      - If jinja test satisfies plugin expression C(true)
      - If jinja test does not satisfy plugin expression C(false)
"""

def _in_one_network(ip, networks):
    """Test if an IP or network is in one network"""

    _error_not_list("in_one_network", networks)
    bools = [_in_network(ip, network) for network in networks]
    if bools.count(True) == 1:
        return True
    return False

class TestModule(object):
    """ network jinja test"""

    test_map = {"in_one_network": _in_one_network}

    def tests(self):
        return self.test_map