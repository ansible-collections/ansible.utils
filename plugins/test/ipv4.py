# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
A test plugin file for netaddr tests
"""

from __future__ import absolute_import, division, print_function
from ansible_collections.ansible.utils.plugins.module_utils.common.ipaddress_utils import (
    ip_network, _need_ipaddress
)

__metaclass__ = type

DOCUMENTATION = """
    name: ipv4
    author: Bradley Thornton (@cidrblock)
    version_added: "2.0.1"
    short_description: Test if something in an IPv4 address or network
    description:
        - This plugin checks if the provided value is a valid host or network IP address with IPV4 addressing scheme
    options:
        ip:
            description:
            - A string that represents the value against which the test is going to be performed
            - For example: 
                - "10.1.1.1"
                - "10.0.0.0/8"
                - "fe80::216:3eff:fee4:16f3"
            type: str
            required: True
    notes:
"""

EXAMPLES = r"""

#### Simple examples

- name: Check if 10.0.0.0/8 is a valid IPV4 address
  ansible.builtin.set_fact:
    data: "{{ '10.0.0.0/8' is ansible.utils.ipv4 }}"

# TASK [Check if 10.0.0.0/8 is a valid IPV4 address] ***************************
# ok: [localhost] => {
#     "ansible_facts": {
#         "data": true
#     },
#     "changed": false
# }

- name: Check if 192.168.1.250 is a valid IPV4 address
  ansible.builtin.set_fact:
    data: "{{ '192.168.1.250' is ansible.utils.ipv4 }}"

# TASK [Check if 192.168.1.250 is a valid IPV4 address] ********************
# ok: [localhost] => {
#     "ansible_facts": {
#         "data": true
#     },
#     "changed": false
# }

- name: Check if fe80::216:3eff:fee4:16f3 is not a valid IPV4 address
  ansible.builtin.set_fact:
    data: "{{ 'fe80::216:3eff:fee4:16f3' is not ansible.utils.ipv4 }}"

# TASK [Check if fe80::216:3eff:fee4:16f3 is not a valid IPV4 address] *********
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

@_need_ipaddress
def _ipv4(ip):
    """Test if something in an IPv4 address or network"""

    try:
        return ip_network(ip).version == 4
    except Exception:
        return False

class TestModule(object):
    """ network jinja test"""

    test_map = {"ipv4": _ipv4}

    def tests(self):
        return self.test_map