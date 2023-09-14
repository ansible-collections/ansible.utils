# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
filter plugin file for ipaddr filters: previous_nth_usable
"""
from __future__ import absolute_import, division, print_function

from functools import partial

from ansible.errors import AnsibleFilterError

from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
    AnsibleArgSpecValidator,
)
from ansible_collections.ansible.utils.plugins.plugin_utils.base.ipaddr_utils import (
    _first_last,
    _need_netaddr,
    ipaddr,
)


__metaclass__ = type


try:
    from jinja2.filters import pass_environment
except ImportError:
    from jinja2.filters import environmentfilter as pass_environment

try:
    import netaddr

    HAS_NETADDR = True
except ImportError:
    # in this case, we'll make the filters return error messages (see bottom)
    HAS_NETADDR = False
else:

    class mac_linux(netaddr.mac_unix):
        pass

    mac_linux.word_fmt = "%.2x"

DOCUMENTATION = """
    name: previous_nth_usable
    author: Ashwini Mhatre (@amhatre)
    version_added: "2.5.0"
    short_description: This filter returns the previous nth usable ip within a network described by value.
    description:
        - This filter returns the previous nth usable ip within a network described by value.
        - Use previous_nth_usable to find the previous nth usable IP address in relation to another within a range
    options:
        value:
            description:
            - subnets or individual address input for previous_nth_usable plugin
            type: str
            required: True
        offset:
            description:
            - index value
            - previous nth usable IP address
            type: int
    notes:
"""

EXAMPLES = r"""
#### examples
- name: previous_nth_usable returns the second usable IP address for the given IP range
  debug:
    msg: "{{ '192.168.122.10/24' | ansible.utils.previous_nth_usable(2) }}"

- name: If there is no usable address, it returns an empty string.
  debug:
    msg: "{{ '192.168.122.1/24' | ansible.utils.previous_nth_usable(2) }}"

# TASK [previous_nth_usable returns the second usable IP address for the given IP range] **************************
# task path: /Users/amhatre/ansible-collections/playbooks/test_previous_nth_usable.yaml:9
# Loading collection ansible.utils from /Users/amhatre/ansible-collections/collections/ansible_collections/ansible/utils
# ok: [localhost] => {
#     "msg": "192.168.122.8"
# }
#
# TASK [If there is no usable address, it returns an empty string.] *******************************************
# task path: /Users/amhatre/ansible-collections/playbooks/test_previous_nth_usable.yaml:14
# Loading collection ansible.utils from /Users/amhatre/ansible-collections/collections/ansible_collections/ansible/utils
# ok: [localhost] => {
#     "msg": ""
# }

"""

RETURN = """
  data:
    type: str
    description:
      - Returns the previous nth usable ip within a network described by value.
"""


@pass_environment
def _previous_nth_usable(*args, **kwargs):
    """This filter returns the previous nth usable ip within a network described by value."""
    keys = ["value", "offset"]
    data = dict(zip(keys, args[1:]))
    data.update(kwargs)
    aav = AnsibleArgSpecValidator(data=data, schema=DOCUMENTATION, name="previous_nth_usable")
    valid, errors, updated_data = aav.validate()
    if not valid:
        raise AnsibleFilterError(errors)
    return previous_nth_usable(**updated_data)


def previous_nth_usable(value, offset):
    """
    Returns the previous nth usable ip within a network described by value.
    """
    try:
        vtype = ipaddr(value, "type")
        if vtype == "address":
            v = ipaddr(value, "cidr")
        elif vtype == "network":
            v = ipaddr(value, "subnet")

        v = netaddr.IPNetwork(v)
    except Exception:
        return False

    if type(offset) is not int:
        raise AnsibleFilterError("Must pass in an integer")
    if v.size > 1:
        first_usable, last_usable = _first_last(v)
        nth_ip = int(netaddr.IPAddress(int(v.ip) - offset))
        if nth_ip >= first_usable and nth_ip <= last_usable:
            return str(netaddr.IPAddress(int(v.ip) - offset))


class FilterModule(object):
    """IP address and network manipulation filters"""

    filter_map = {
        # IP addresses and networks
        "previous_nth_usable": _previous_nth_usable,
    }

    def filters(self):
        """ipaddr filter"""
        if HAS_NETADDR:
            return self.filter_map
        else:
            return dict((f, partial(_need_netaddr, f)) for f in self.filter_map)
