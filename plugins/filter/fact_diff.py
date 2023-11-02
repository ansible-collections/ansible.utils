# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


"""
The fact_diff filter plugin
"""
from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
    name: fact_diff
    author: Ashwini Mhatre ((@amhatre))
    version_added: "2.12.0"
    short_description: Find the difference between currently set facts
    description:
        - Compare two facts or variables and get a diff.
    options:
        before:
            description:
            - The first fact to be used in the comparison.
            type: raw
            required: True
        after:
            description:
            - The second fact to be used in the comparison.
            type: raw
            required: True
        plugin:
            description:
            - Configure and specify the diff plugin to use
            type: dict
            default: {}
            suboptions:
                name:
                    description:
                    - The diff plugin to use, in fully qualified collection name format.
                    default: ansible.utils.native
                    type: str
                vars:
                    description:
                    - Parameters passed to the diff plugin.
                    type: dict
                    default: {}
                    suboptions:
                        skip_lines:
                            description:
                            - Skip lines matching these regular expressions.
                            - Matches will be removed prior to the diff.
                            - If the provided I(before) and I(after) are a string, they will be split.
                            - Each entry in each list will be cast to a string for the comparison
                            type: list
                            elements: str


    notes:
"""

EXAMPLES = """
"""
RETURN = """
  data:
    type: str
    description:
      - Returns values valid for a particular query.
"""
from ansible.errors import AnsibleFilterError

from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
    AnsibleArgSpecValidator,
)
from ansible_collections.ansible.utils.plugins.plugin_utils.fact_diff import fact_diff


try:
    from jinja2.filters import pass_environment
except ImportError:
    from jinja2.filters import environmentfilter as pass_environment


@pass_environment
def _fact_diff(*args, **kwargs):
    """Find the difference between currently set facts"""

    keys = ["before", "after", "plugin"]
    data = dict(zip(keys, args[1:]))
    data.update(kwargs)
    aav = AnsibleArgSpecValidator(data=data, schema=DOCUMENTATION, name="fact_diff")
    valid, errors, updated_data = aav.validate()
    if not valid:
        raise AnsibleFilterError(errors)
    res = fact_diff(**updated_data)
    import json

    res = str(res)
    return res


class FilterModule(object):
    """fact_diff"""

    def filters(self):
        """a mapping of filter names to functions"""
        return {"fact_diff": _fact_diff}
