# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


"""
The index_of plugin common code
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import xmltodict
import ast
from ansible_collections.ansible.utils.plugins.module_utils.common.utils import (
    validate_data,
)

# Note, this file can only be used on the control node
# where ansible is installed
# limit imports to filter and lookup plugins
try:
    from ansible.errors import AnsibleError
except ImportError:
    pass


def _raise_error(msg):
    """Raise an error message, prepend with filter name

    :param msg: The message
    :type msg: str
    :raises: AnsibleError
    """
    error = "Error when using plugin 'json_to_xml': {msg}".format(msg=msg)
    raise AnsibleError(error)

def json_to_xml(
    data
):
    """Convert data which is in json to xml"

    :param data: The data passed in (data|json_to_xml(...))
    :type data: xml
    """
    filter_type = validate_data(data, 'json')
    if filter_type == 'json':
        data = ast.literal_eval(data)
        res = xmltodict.unparse(data, pretty=True)
    else:
        _raise_error("Input json is not valid")
    return res
