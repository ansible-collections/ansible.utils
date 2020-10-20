# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


"""
The index_of filter plugin
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.errors import AnsibleFilterError
from jinja2.filters import environmentfilter
from ansible_collections.ansible.utils.plugins.module_utils.common.index_of import (
    index_of,
)
from ansible_collections.ansible.utils.plugins.lookup.index_of import (
    DOCUMENTATION,
)
from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
    AnsibleArgSpecValidator,
)


@environmentfilter
def _index_of(*args, **kwargs):
    """Find the indicies of items in a list matching some criteria. [See examples](https://github.com/ansible-collections/ansible.utils/blob/main/docs/ansible.utils.index_of_lookup.rst)"""

    keys = [
        "environment",
        "data",
        "test",
        "value",
        "key",
        "fail_on_missing",
        "wantlist",
    ]
    data = dict(zip(keys, args))
    data.update(kwargs)
    environment = data.pop("environment")
    aav = AnsibleArgSpecValidator(
        data=data,
        schema=DOCUMENTATION,
        schema_format="doc",
        name="index_of",
    )
    valid, errors, updated_data = aav.validate()
    if not valid:
        raise AnsibleFilterError(errors)
    updated_data['tests'] = environment.tests
    return index_of(**updated_data)


class FilterModule(object):
    """ index_of  """

    def filters(self):
        """a mapping of filter names to functions"""
        return {"index_of": _index_of}
