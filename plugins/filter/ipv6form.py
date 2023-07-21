# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
filter plugin file for ipaddr filters: ipv6form
"""
from __future__ import absolute_import, division, print_function

from functools import partial

from ansible.errors import AnsibleFilterError

from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
    AnsibleArgSpecValidator,
)
from ansible_collections.ansible.utils.plugins.plugin_utils.base.ipaddress_utils import (
    _need_ipaddress,
    ip_address,
)


__metaclass__ = type


try:
    from jinja2.filters import pass_environment
except ImportError:
    from jinja2.filters import environmentfilter as pass_environment


DOCUMENTATION = """
    name: ipv6form
    author: Ashwini Mhatre (@amhatre)
    version_added: "2.11.0"
    short_description: This filter is designed to convert ipv6 address in different formats. For example expand, compressetc.
    description:
        - This filter is designed to convert ipv6 addresses in different formats.
    options:
        value:
            description:
            - individual ipv6 address input for ipv6_format plugin.
            type: str
            required: True
        amount:
            type: str
            choice:
                ['compress', 'expand', 'x509']
            description: Different formats example. compress, expand, x509
"""

EXAMPLES = r"""
#### examples


"""

RETURN = """
  data:
    type: str
    description:
      - Returns result ipv6 address in expected format.
"""


@pass_environment
def _ipv6form(*args, **kwargs):
    """Convert the given data from json to xml."""
    keys = ["value", "format"]
    data = dict(zip(keys, args[1:]))
    data.update(kwargs)
    aav = AnsibleArgSpecValidator(data=data, schema=DOCUMENTATION, name="ipv6form")
    valid, errors, updated_data = aav.validate()
    if not valid:
        raise AnsibleFilterError(errors)
    return ipv6form(**updated_data)


@_need_ipaddress
def ipv6form(value, format):
    try:
        if format == "expand":
            return ip_address(value).exploded
        elif format == "compress":
            return ip_address(value).compressed
        elif format == "x509":
            return ip_address(value).exploded
    except ValueError:
        msg = "You must pass a valid IP address; {0} is invalid".format(value)
        raise AnsibleFilterError(msg)

    if not isinstance(amount, int):
        msg = ("You must pass an integer for arithmetic; " "{0} is not a valid integer").format(
            amount,
        )
        raise AnsibleFilterError(msg)

    return str(ip + amount)


class FilterModule(object):
    """IP address and network manipulation filters"""

    filter_map = {
        # This filter is designed to do ipv6 conversion in required format
        "ipv6form": _ipv6form,
    }

    def filters(self):
        """ipmath filter"""
        if HAS_NETADDR:
            return self.filter_map
        else:
            return dict((f, partial(_need_netaddr, f)) for f in self.filter_map)
