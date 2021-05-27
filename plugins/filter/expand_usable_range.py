# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Filter plugin file for expand_usable_range
"""

from __future__ import absolute_import, division, print_function, unicode_literals
from ipaddress import IPv4Network

from ansible_collections.ansible.utils.plugins.plugin_utils.base.ipaddress_utils import (
    _validate_args,
)

__metaclass__ = type

DOCUMENTATION = """
    name: expand_usable_range
    author: Priyam Sahoo (@priyamsahoo)
    version_added: "2.2.0"
    short_description: Expand the usable IP addresses
    description:
        - For a given IP Address in CIDR form, this plugins generates a list of usable IP addresses belonging to the network.
    options:
        ip:
            description:
            - A string that represents an IP address of network in CIDR form
            - For example: "10.0.0.0/24"
            type: str
            required: True
    notes:
"""

EXAMPLES = r"""

#### Simple examples

- name: Expand and produce list of usable IP addresses in 10.0.0.0/28
  ansible.builtin.set_fact:
    data: "{{ '10.0.0.0/28' | ansible.utils.expand_usable_range }}"

# TASK [Expand and produce list of usable IP addresses in 10.0.0.0/28] ************************
# ok: [localhost] => {
#     "ansible_facts": {
#         "data": {
#             "number_of_ips": 16,
#             "usable_ips": [
#                 "10.0.0.0",
#                 "10.0.0.1",
#                 "10.0.0.2",
#                 "10.0.0.3",
#                 "10.0.0.4",
#                 "10.0.0.5",
#                 "10.0.0.6",
#                 "10.0.0.7",
#                 "10.0.0.8",
#                 "10.0.0.9",
#                 "10.0.0.10",
#                 "10.0.0.11",
#                 "10.0.0.12",
#                 "10.0.0.13",
#                 "10.0.0.14",
#                 "10.0.0.15"
#             ]
#         }
#     },
#     "changed": false
# }

- name: Expand and produce list of usable IP addresses in 10.1.1.1
  ansible.builtin.set_fact:
    data: "{{ '10.1.1.1' | ansible.utils.expand_usable_range }}"

# TASK [Expand and produce list of usable IP addresses in 10.1.1.1] ***************************
# ok: [localhost] => {
#     "ansible_facts": {
#         "data": {
#             "number_of_ips": 1,
#             "usable_ips": [
#                 "10.1.1.1"
#             ]
#         }
#     },
#     "changed": false
# }

"""

RETURN = """
    data:
        description:
        - Total number of usable IP addresses under the key C(number_of_ips)
        - List of usable IP addresses under the key C(usable_ips)
"""

from ansible.errors import AnsibleError, AnsibleFilterError
from ansible.module_utils.basic import missing_required_lib
# from ansible.module_utils.six import ensure_str
from ansible.module_utils.common.text.converters import to_text

try:
    import ipaddress
    HAS_IPADDRESS = True
except ImportError:
    HAS_IPADDRESS = False


def _expand_usable_range(ip):
    """Expand the usable IP addresses"""

    params = {"ip": ip}
    _validate_args("expand_usable_range", DOCUMENTATION, params)

    if not HAS_IPADDRESS:
        raise AnsibleError(missing_required_lib("ipaddress"))

    try:
        ips = [to_text(usable_ips) for usable_ips in ipaddress.IPv4Network(to_text(ip))]
        no_of_ips = len(ips)
    except Exception as e:
        raise AnsibleFilterError("Error while using plugin 'expand_usable_range': {msg}".format(msg = to_text(e)))
    
    return {"usable_ips": ips, "number_of_ips": no_of_ips}

    # if not HAS_NETADDR:
    #     raise AnsibleError(missing_required_lib("netaddr"))

    # try:
    # ips = [usable_ips for usable_ips in netaddr.IPNetwork(ip)]
    # no_of_ips = len(ips)
    # except Exception as e:
        # raise AnsibleFilterError(f"Error while using plugin 'expand_usable_range': {str(e)}")
    
    # return {"usable_ips": ips, "number_of_ips": no_of_ips}


class FilterModule(object):
    """ expand_usable_range  """

    def filters(self):

        """a mapping of filter names to functions"""
        return {"expand_usable_range": _expand_usable_range}

