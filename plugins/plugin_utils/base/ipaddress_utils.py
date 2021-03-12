# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The test plugin utils file for netaddr tests
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


import json
# import re

from ansible.errors import AnsibleError
from ansible.module_utils.basic import missing_required_lib
from ansible.module_utils.six import ensure_text
from functools import wraps


try:
    import ipaddress

    HAS_IPADDRESS = True
except ImportError:
    HAS_IPADDRESS = False


def ip_network(ip):
    """ PY2 compat shim, PY2 requires unicode
    """
    return ipaddress.ip_network(ensure_text(ip))


def ip_address(ip):
    """ PY2 compat shim, PY2 requires unicode
    """
    return ipaddress.ip_address(ensure_text(ip))


def _need_ipaddress(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not HAS_IPADDRESS:
            test = func.__name__.lstrip("_")
            msg = "'{test}' requires 'ipaddress' {stnd}".format(
                test=test,
                stnd=missing_required_lib("ipaddress").replace(
                    "module", "plugin"
                ),
            )
            raise AnsibleError(msg)
        return func(*args, **kwargs)

    return wrapper


def _is_subnet_of(network_a, network_b):
    try:
        if network_a._version != network_b._version:
            return False
        return (
            network_b.network_address <= network_a.network_address
            and network_b.broadcast_address >= network_a.broadcast_address
        )
    except Exception:
        return False


def _to_well_known_type(obj):
    """ Convert an ansible internal type to a well-known type
    ie AnsibleUnicode => str

    :param obj: the obj to convert
    :type obj: unknown
    """
    return json.loads(json.dumps(obj))


def _error_not_list(test, obj):
    tipe = _to_well_known_type(obj)
    if not isinstance(tipe, list):
        msg = "The test '{test}' requires a list, but {obj} was a '{type}'".format(
            test=test, obj=obj, type=type(tipe).__name__
        )
        raise AnsibleError(msg)

