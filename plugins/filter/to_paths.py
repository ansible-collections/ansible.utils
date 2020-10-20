# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


"""
flatten a complex object to dot bracket notation
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type


from ansible_collections.ansible.utils.plugins.module_utils.common.path import (
    to_paths,
)


def _to_paths(*args, **kwargs):
    """Flatten a complex object into a dictionary of paths and values. [See examples](https://github.com/ansible-collections/ansible.utils/blob/main/docs/ansible.utils.to_paths_lookup.rst)"""
    return to_paths(*args, **kwargs)


class FilterModule(object):
    """ path filters """

    def filters(self):
        return {"to_paths": _to_paths}
