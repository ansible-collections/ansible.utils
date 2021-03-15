# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
A test plugin file for netaddr tests
"""

from __future__ import absolute_import, division, print_function
from ansible_collections.ansible.utils.plugins.plugin_utils.base.ipaddress_utils import (
    ip_network, _need_ipaddress
)

__metaclass__ = type

DOCUMENTATION = """
    name: ip
    author: Priyam Sahoo (@priyamsahoo)
    version_added: "2.0.1"
    short_description: Test if something in an IP address or network
    description:
        - This plugin checks if the provided value is a valid host or network IP address
    options:
        ip:
            description:
            - A string that represents the value against which the test is going to be performed
            - For example: 
                - "10.1.1.1"
                - "hello-world"
            type: str
            required: True
    notes:
"""

EXAMPLES = r"""

#### Simple examples

- name: Check if 10.1.1.1 is a valid IP address
  ansible.builtin.set_fact:
    data: "{{ '10.1.1.1' is ansible.utils.ip }}"

# TASK [Check if 10.1.1.1 is a valid IP address] *****************************
# ok: [localhost] => {
#     "ansible_facts": {
#         "data": true
#     },
#     "changed": false
# }

- name: Check if "hello-world" is not a valid IP address
  ansible.builtin.set_fact:
    data: "{{ 'hello-world' is not ansible.utils.ip }}"

# TASK [Check if "hello-world" is not a valid IP address] ********************
# ok: [localhost] => {
#     "ansible_facts": {
#         "data": true
#     },
#     "changed": false
# }


- name: Check if 300.1.1.1 is a valid IP address
  ansible.builtin.set_fact:
    data: "{{ '300.1.1.1' is ansible.utils.ip }}"

# TASK [Check if 300.1.1.1 is a valid IP address] ****************************
# ok: [localhost] => {
#     "ansible_facts": {
#         "data": false
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
def _ip(ip):
    """ Test if something in an IP address or network """

    try:
        ip_network(ip)
        return True
    except Exception:
        return False

class TestModule(object):
    """ network jinja test"""

    test_map = {"ip": _ip}

    def tests(self):
        return self.test_map