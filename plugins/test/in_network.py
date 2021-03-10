# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
A test plugin file for netaddr tests
"""

from __future__ import absolute_import, division, print_function
from ansible_collections.ansible.utils.plugins.module_utils.common.ipaddress_utils import (
    ip_network, _is_subnet_of, _need_ipaddress
)

__metaclass__ = type

DOCUMENTATION = """
    name: in_network
    author: Bradley Thornton (@cidrblock)
    version_added: "2.0.1"
    short_description: Test if IP address falls in the network
    description:
        - This plugin checks if the provided IP address belongs to the provided network
    options:
        ip:
            description:
            - A string that represents an IP address
            - For example: "10.1.1.1"
            type: str
            required: True
        network:
            description:
            - A string that represents the network address in CIDR form
            - For example: "10.0.0.0/8"
            type: str
            required: True

    notes:
"""

EXAMPLES = r"""

#### Simple examples

- name: Check if 10.1.1.1 is in 10.0.0.0/8
    ansible.builtin.set_fact:
      data: "{{ '10.1.1.1' is ansible.utils.in_network '10.0.0.0/8' }}"

# TASK [Check if 10.1.1.1 is in 10.0.0.0/8] ***********************************
# ok: [localhost] => {
#     "ansible_facts": {
#         "data": true
#     },
#     "changed": false
# }

- name: Check if 10.1.1.1 is not in 192.168.1.0/24
      ansible.builtin.set_fact:
        data: "{{ '10.1.1.1' is not ansible.utils.in_network '192.168.1.0/24' }}"

# TASK [Check if 10.1.1.1 is not in 192.168.1.0/24] ****************************
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
def _in_network(ip, network):
    """Test if an address or network is in a network"""

    try:
        return _is_subnet_of(ip_network(ip), ip_network(network))
    except Exception:
        return False

class TestModule(object):
    """ network jinja tests
    """

    test_map = {"in_network": _in_network,}

    def tests(self):
        return self.test_map