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
    name: ipv4_hostmask
    author: Bradley Thornton (@cidrblock)
    version_added: "2.0.1"
    short_description: Test if an address is a hostmask
    description:
        - This plugin checks if the provided ip address is a hostmask or not
    options:
        ip:
            description:
            - A string that represents the value against which the test is going to be performed
            - For example: 
                - "0.1.255.255"
                - "255.255.255.0"
            type: str
            required: True
    notes:
"""

EXAMPLES = r"""

#### Simple examples

- name: Check if 0.0.0.255 is a hostmask
  ansible.builtin.set_fact:
    data: "{{ '0.0.0.255' is ansible.utils.ipv4_hostmask }}"

# TASK [Check if 0.0.0.255 is a hostmask] ***********************************************
# ok: [localhost] => {
#     "ansible_facts": {
#         "data": true
#     },
#     "changed": false
# }

- name: Check if 255.255.255.0 is a hostmask
  ansible.builtin.set_fact:
    data: "{{ '255.255.255.0' is not ansible.utils.ipv4_hostmask }}"

# TASK [Check if 255.255.255.0 is a hostmask] *********************************
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
def _ipv4_hostmask(ip):
    """Test if an address is a hostmask"""
    
    try:
        ipaddr = ip_network("10.0.0.0/{ip}".format(ip=ip))
        return str(ipaddr.hostmask) == ip
    except Exception:
        return False


class TestModule(object):
    """ network jinja test"""

    test_map = {"ipv4_hostmask": _ipv4_hostmask}

    def tests(self):
        return self.test_map