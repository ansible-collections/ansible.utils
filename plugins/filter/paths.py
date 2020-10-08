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
from ansible.module_utils.common._collections_compat import (
    Mapping,
    MutableMapping,
)

from ansible_collections.ansible.utils.plugins.module_utils.generate_paths import (
    generate_paths,
)
from jinja2.filters import environmentfilter


def to_paths(obj, prepend=None):
    return generate_paths(obj, prepend)


@environmentfilter
def get_path(environment, vars, path):
    string_to_variable = "{{ %s }}" % path
    return environment.from_string(string_to_variable).render(**vars)


class FilterModule(object):
    """ Network filter """

    def filters(self):
        return {"to_paths": to_paths, "get_path": get_path}
