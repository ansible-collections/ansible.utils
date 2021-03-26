#
# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

"""
The json_to_xml plugin
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import ast
from ansible.errors import AnsibleError


def _raise_error(msg):
    """Raise an error message, prepend with filter name

    :param msg: The message
    :type msg: str
    :raises: AnsibleError
    """
    error = "Error when using plugin 'json_to_xml': {msg}".format(msg=msg)
    raise AnsibleError(error)


def json_to_xml(data, engine):
    """Convert data which is in json to xml"

    :param data: The data passed in (data|json_to_xml(...))
    :type data: xml
    :param engine: Conversion library default=xmltodict
    """
    if engine == "xmltodict":
        import xmltodict

        try:
            data = ast.literal_eval(data)
            res = xmltodict.unparse(data, pretty=True)
        except Exception:
            _raise_error("Input json is not valid")
        return res
