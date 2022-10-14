# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Test plugin file for netaddr tests: ipv6
"""

from __future__ import absolute_import, division, print_function

from ansible_collections.ansible.utils.plugins.plugin_utils.base.ipaddress_utils import (
    _need_ipaddress,
    ip_network,
)
from ansible_collections.ansible.utils.plugins.plugin_utils.base.utils import _validate_args


__metaclass__ = type

DOCUMENTATION = """
    name: ipv6
    author: Priyam Sahoo (@priyamsahoo)
    version_added: "2.2.0"
    short_description: Test if something is an IPv6 address or network
    description:
        - This plugin checks if the provided value is a valid host or network IP address with IPv6 addressing scheme
    options:
        ip:
            description:
            - A string that represents the value against which the test is going to be performed
            - 'For example: C(10.1.1.1), C(10.0.0.0/8), or C(fe80::216:3eff:fee4:16f3)'
            type: str
            required: True
    notes:
"""

EXAMPLES = r"""

#### Simple examples

- name: Check if fe80::216:3eff:fee4:16f3 is a valid IPv6 address
  ansible.builtin.set_fact:
    data: "{{ 'fe80::216:3eff:fee4:16f3' is ansible.utils.ipv6 }}"

# TASK [Check if fe80::216:3eff:fee4:16f3 is a valid IPv6 address] *************
# ok: [localhost] => {
#     "ansible_facts": {
#         "data": true
#     },
#     "changed": false
# }

- name: Check if 2001:db8:a::/64 is a valid IPv6 address
  ansible.builtin.set_fact:
    data: "{{ '2001:db8:a::/64' is ansible.utils.ipv6 }}"

# TASK [Check if 2001:db8:a::/64 is a valid IPv6 address] **********************
# ok: [localhost] => {
#     "ansible_facts": {
#         "data": true
#     },
#     "changed": false
# }

- name: Check if 192.169.1.250 is not a valid IPv6 address
  ansible.builtin.set_fact:
    data: "{{ '192.169.1.250' is not ansible.utils.ipv6 }}"

# TASK [Check if 192.169.1.250 is not a valid IPv6 address] ********************
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
def _ipv6(ip):
    """Test if something in an IPv6 address or network"""

    params = {"ip": ip}
    _validate_args("ipv6", DOCUMENTATION, params)

    try:
        return ip_network(ip).version == 6
    except Exception:
        return False


class TestModule(object):
    """network jinja test"""

    test_map = {"ipv6": _ipv6}

    def tests(self):
        return self.test_map
