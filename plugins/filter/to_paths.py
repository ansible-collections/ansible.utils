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
from ansible_collections.ansible.utils.plugins.module_utils.common.to_paths import (
    to_paths,
)
from ansible_collections.ansible.utils.plugins.lookup.to_paths import (
    DOCUMENTATION,
)
from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
    AnsibleArgSpecValidator,
)


def _to_paths(*args, **kwargs):
    """Flatten a complex object into a dictionary of paths and values. [See examples](https://github.com/ansible-collections/ansible.utils/blob/main/docs/ansible.utils.to_paths_lookup.rst)"""
    keys = ["var", "prepend", "wantlist"]
    data = dict(zip(keys, args))
    data.update(kwargs)
    aav = AnsibleArgSpecValidator(
        data=data,
        schema=DOCUMENTATION,
        name="to_paths",
    )
    valid, errors, updated_data = aav.validate()
    if not valid:
        raise AnsibleFilterError(errors)
    return to_paths(**updated_data)


class FilterModule(object):
    """ path filters """

    def filters(self):
        return {"to_paths": _to_paths}
