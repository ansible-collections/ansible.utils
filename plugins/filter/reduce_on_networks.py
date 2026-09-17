# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
filter plugin file for ipaddr filters: reduce_on_networks
"""
from __future__ import absolute_import, division, print_function

from functools import partial

from ansible.errors import AnsibleFilterError

from ansible_collections.ansible.utils.plugins.filter.reduce_on_network import (
    reduce_on_network,
)
from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
    AnsibleArgSpecValidator,
)


__metaclass__ = type


try:
    from jinja2.filters import pass_environment
except ImportError:
    from jinja2.filters import environmentfilter as pass_environment


DOCUMENTATION = """
    name: reduce_on_networks
    author: Jonny007-MKD
    version_added: "6.0.0"
    short_description: This filter reduces a list of addresses to only the addresses that match any of the given networks.
    description:
    - This filter reduces a list of addresses to only the addresses that match any of the given networks.
    - To check whether multiple addresses belong to any of the networks, use the reduce_on_networks filter.
    - To check which of the IP address of a host can be used to talk to another host, use the reduce_on_networks filter.
    options:
        value:
            description: the list of addresses to filter on.
            type: list
            elements: str
            required: True
        networks:
            description: The networks to validate against.
            type: list
            elements: str
            required: True
    notes:
"""

EXAMPLES = r"""

- name: To check whether multiple addresses belong to any of the networks, use the reduce_on_networks filter.
  debug:
    msg: "{{ ['192.168.0.34', '10.3.0.3', '192.168.2.34'] | ansible.utils.reduce_on_networks( ['192.168.0.0/24', '192.128.0.0/9', '127.0.0.1/8'] ) }}"

# TASK [To check whether multiple addresses belong to any of the networks, use the reduce_on_networks filter.] ***********
# task path: /Users/amhatre/ansible-collections/playbooks/test_reduce_on_network.yaml:7
# Loading collection ansible.utils from /Users/amhatre/ansible-collections/collections/ansible_collections/ansible/utils
# ok: [localhost] => {
#     "msg": {
#         "192.168.0.34": [
#             "192.168.0.0/24",
#             "192.128.0.0/9"
#         ],
#         "192.168.2.34": [
#             "192.128.0.0/9"
#         ]
#     }
# }
"""

RETURN = """
  data:
    type: dict
    key type: str
    value type: list of str
    description:
      - Returns the filtered addresses belonging to any of the networks. The dict's key is the address, the value is a list of the matching networks
"""


@pass_environment
def _reduce_on_networks(*args, **kwargs):
    """This filter returns a dict of the filtered addresses belonging to any of the networks"""
    keys = ["value", "networks"]
    data = dict(zip(keys, args[1:]))
    data.update(kwargs)
    aav = AnsibleArgSpecValidator(data=data, schema=DOCUMENTATION, name="reduce_on_networks")
    valid, errors, updated_data = aav.validate()
    if not valid:
        raise AnsibleFilterError(errors)
    return reduce_on_networks(**updated_data)


def reduce_on_networks(value, networks):
    """
    Reduces a list of addresses to only the addresses that match any of the given networks.
    :param: value: The list of addresses to filter on.
    :param: network: The list of networks to validate against.
    :return: A dict of the reduced addresses and their networks.
    """

    r = {}
    for network in networks:
        matches = reduce_on_network(value, network)
        for match in matches:
            match_networks = r.setdefault(match, [])
            match_networks.append(network)
    return r


class FilterModule(object):
    """IP address and network manipulation filters"""

    filter_map = {
        # IP addresses and networks
        "reduce_on_networks": _reduce_on_networks,
    }

    def filters(self):
        """ipaddr filter"""
        return self.filter_map
