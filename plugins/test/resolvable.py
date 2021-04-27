# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Simple, dependency free convenience tests
"""
from __future__ import absolute_import, division, print_function
from ansible_collections.ansible.utils.plugins.plugin_utils.base.ipaddress_utils import _need_ipaddress

import socket

from ansible.errors import AnsibleError
from ansible.module_utils.basic import missing_required_lib

try:
    import ipaddress

    HAS_IPADDRESS = True
except ImportError:
    HAS_IPADDRESS = False

__metaclass__ = type

DOCUMENTATION = """
    name: resolvable
    author: Priyam Sahoo (@priyamsahoo)
    version_added: "2.0.1"
    short_description: Test if an IP or name can be resolved via /etc/hosts or DNS
    description:
        - This plugin checks if the provided network IP address of host name can be resolved using /etc/hosts or DNS
    options:
        interface:
            description:
            - A string that represents the IP address or the host name
            - For example:
                - "docs.ansible.com"
                - 127.0.0.1
                - ::1
            type: str
            required: True

    notes:
"""

EXAMPLES = r"""

#### Simple examples

- name: Check if docs.ansible.com is resolvable or not
  ansible.builtin.set_fact:
    data: "{{ 'docs.ansible.com' is ansible.utils.resolvable }}"

# TASK [Check if docs.ansible.com is resolvable or not] **************************
# ok: [localhost] => {
#     "ansible_facts": {
#         "data": true
#     },
#     "changed": false
# }


- set_fact:
    good_name: www.google.com
    bad_name: foo.google.com

- assert:
    that: "{{ 'www.google.com' is ansible.utils.resolvable }}"

- assert:
    that: "{{ 'foo.google.com' is not ansible.utils.resolvable }}"

# TASK [set_fact] ****************************************************************
# ok: [localhost]

# TASK [assert] ******************************************************************
# ok: [localhost] => {
#     "changed": false,
#     "msg": "All assertions passed"
# }

# TASK [assert] ******************************************************************
# ok: [localhost] => {
#     "changed": false,
#     "msg": "All assertions passed"
# }

- set_fact:
    ipv4_localhost: 127.0.0.1
    ipv6_localhost: ::1

- assert:
    that: "{{ ipv4_localhost is ansible.utils.resolvable }}"

- assert:
    that: "{{ ipv6_localhost is ansible.utils.resolvable }}"

# TASK [set_fact] ****************************************************************
# ok: [localhost] => {
#     "ansible_facts": {
#         "ipv4_localhost": "127.0.0.1",
#         "ipv6_localhost": "::1"
#     },
#     "changed": false
# }

# TASK [assert] ******************************************************************
# ok: [localhost] => {
#     "changed": false,
#     "msg": "All assertions passed"
# }

# TASK [assert] ******************************************************************
# ok: [localhost] => {
#     "changed": false,
#     "msg": "All assertions passed"
# }

"""

RETURN = """
  data:
    description:
      - If jinja test satisfies plugin expression C(true)
      - If jinja test does not satisfy plugin expression C(false)
"""

@_need_ipaddress
def resolvable(str):
    """ Test if an IP or name can be resolved via /etc/hosts or DNS """
    
    try:
        ipaddress.ip_address(str)
        ip = True
    except Exception:
        ip = False
    if ip:
        try:
            socket.gethostbyaddr(str)
            return True
        except Exception:
            return False
    else:
        try:
            socket.getaddrinfo(str, None)
            return True
        except Exception:
            return False


class TestModule(object):
    """ network jinja tests """

    test_map = {"resolvable": resolvable}

    def tests(self):
        return self.test_map