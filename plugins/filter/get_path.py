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

from ansible_collections.ansible.utils.plugins.module_utils.common.path import (
    get_path,
)
from jinja2.filters import environmentfilter


from ansible_collections.ansible.utils.plugins.lookup.get_path import DOCUMENTATION
from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import AnsibleArgSpecValidator


@environmentfilter
def _get_path(*args, **kwargs):
    """Retrieve the value in a variable using a path. [See examples](https://github.com/ansible-collections/ansible.utils/blob/main/docs/ansible.utils.get_path_lookup.rst)"""
    keys = ['environment', 'var', 'path']
    spec = dict(zip(keys, args))
    spec.update(kwargs)
    aav = AnsibleArgSpecValidator(
        data=spec,
        schema=DOCUMENTATION,
        schema_format="doc",
        name='get_path',
    )
    valid, errors = aav.validate()
    if not valid:
        raise AnsibleFilterError(errors)
    return get_path(**spec)


class FilterModule(object):
    """ path filters """

    def filters(self):
        return {"to_paths": _to_paths, "get_path": _get_path}
