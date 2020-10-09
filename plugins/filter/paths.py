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

from ansible_collections.ansible.utils.plugins.module_utils.path_utils import (
    to_paths,
    get_path,
)
from jinja2.filters import environmentfilter


def _to_paths(*args, **kwargs):
    """ Convert complex objects to paths. [See examples](https://github.com/ansible-collections/ansible.utils/blob/main/docs/ansible.utils.to_paths_lookup.rst)
    """
    return to_paths(*args, **kwargs)


@environmentfilter
def _get_path(*args, **kwargs):
    """ Get value using path. [See examples](https://github.com/ansible-collections/ansible.utils/blob/main/docs/ansible.utils.get_path_lookup.rst)
    """
    kwargs["environment"] = args[0]
    args = args[1:]
    return get_path(*args, **kwargs)


class FilterModule(object):
    """ path filters """

    def filters(self):
        return {"to_paths": _to_paths, "get_path": _get_path}
