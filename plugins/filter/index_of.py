# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


"""
The index_of filter plugin
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.ansible.utils.plugins.module_utils.common.index_of import (
    index_of,
)
from jinja2.filters import environmentfilter


@environmentfilter
def _index_of(*args, **kwargs):
    """Find the indicies of items in a list matching some criteria. [See examples](https://github.com/ansible-collections/ansible.utils/blob/main/docs/ansible.utils.index_of_lookup.rst)"""
    kwargs["tests"] = args[0].tests
    args = args[1:]
    return index_of(*args, **kwargs)


class FilterModule(object):
    """ index_of  """

    def filters(self):
        """a mapping of filter names to functions"""
        return {"index_of": _index_of}
