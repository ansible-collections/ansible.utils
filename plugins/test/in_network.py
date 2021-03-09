# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The test plugin file for netaddr tests
"""

from __future__ import absolute_import, division, print_function
from ansible_collections.ansible.utils.plugins.module_utils.common.ipaddress_utils import (
    ip_network, _is_subnet_of, _need_ipaddress
)

__metaclass__ = type

DOCUMENTATION = """
    name: general
    author: Bradley A. Thornton (@cidrblock)
    version_added: "2.0.1"
"""

@_need_ipaddress
def _in_network(ip, network):
    """Test if an address or network is in a network<br/>`'10.1.1.1' is ansible.utils.in_network '10.0.0.0/8'`
    """
    try:
        return _is_subnet_of(ip_network(ip), ip_network(network))
    except Exception:
        return False

# print(_in_network('10.1.1.1', '10.0.0.0/8'))