# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


"""
flatten a complex object to dot bracket notation
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import re
from ansible.module_utils.common._collections_compat import (
    Mapping,
    MutableMapping,
)

# Note, this file can only be used on the control node
# where ansible is installed
# limit imports to filter and lookup plugins
try:
    from ansible.errors import AnsibleError
except ImportError:
    pass


def get_path(var, path, environment, wantlist=False):
    """ Get the value of a path within an object

    :param var: The var from which the value is retrieved
    :type var: should be dict or list, but jinja can sort that out
    :param path: The path to get
    :type path: should be a string but jinja can sort that out
    :param environment: The jinja Environment
    :type environment: Environment
    :return: The result of the jinja evaluation
    :rtype: any
    """
    string_to_variable = "{{ %s }}" % path
    result = environment.from_string(string_to_variable).render(**var)
    if wantlist:
        return [result]
    return result


def to_paths(var, prepend=False, wantlist=False):
    if prepend:
        if not isinstance(prepend, str):
            raise AnsibleError("The value of 'prepend' must be a sting.")
        var = {prepend: var}

    out = {}

    def flatten(data, name=""):
        if isinstance(data, (dict, Mapping, MutableMapping)):
            for key, val in data.items():
                if name:
                    if re.match("^[a-zA-Z_][a-zA-Z0-9_]*$", key):
                        nname = name + ".{key}".format(key=key)
                    else:
                        nname = name + "['{key}']".format(key=key)
                else:
                    nname = key
                flatten(val, nname)
        elif isinstance(data, list):
            for idx, val in enumerate(data):
                flatten(val, "{name}[{idx}]".format(name=name, idx=idx))
        else:
            out[name] = data

    flatten(var)
    if wantlist:
        return [out]
    return out
