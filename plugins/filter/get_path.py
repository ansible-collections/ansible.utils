# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


"""
flatten a complex object to dot bracket notation
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.errors import AnsibleFilterError
from jinja2.filters import environmentfilter

from ansible_collections.ansible.utils.plugins.module_utils.common.get_path import (
    get_path,
)
from ansible_collections.ansible.utils.plugins.lookup.get_path import (
    DOCUMENTATION,
)
from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
    AnsibleArgSpecValidator,
)


@environmentfilter
def _get_path(*args, **kwargs):
    """Retrieve the value in a variable using a path. [See examples](https://github.com/ansible-collections/ansible.utils/blob/main/docs/ansible.utils.get_path_lookup.rst)"""
    keys = ["environment", "var", "path"]
    data = dict(zip(keys, args))
    data.update(kwargs)
    environment = data.pop("environment")
    aav = AnsibleArgSpecValidator(
        data=data, schema=DOCUMENTATION, schema_format="doc", name="get_path",
    )
    valid, errors, updated_data = aav.validate()
    if not valid:
        raise AnsibleFilterError(errors)
    updated_data["environment"] = environment
    return get_path(**updated_data)


class FilterModule(object):
    """ path filters """

    def filters(self):
        return {"get_path": _get_path}
