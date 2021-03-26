#
# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

"""
The xml_to_json plugin code
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
from ansible.errors import AnsibleError


def _raise_error(msg):
    """Raise an error message, prepend with filter name
    :param msg: The message
    :type msg: str
    :raises: AnsibleError
    """
    error = "Error when using plugin 'xml_to_json': {msg}".format(msg=msg)
    raise AnsibleError(error)


def xml_to_json(data, engine):
    """Convert data which is in xml to json"
    :param data: The data passed in (data|xml_to_json(...))
    :type data: xml
    :param engine: Conversion library default=xml_to_dict
    """
    if engine == "xmltodict":
        import xmltodict

        try:
            res = json.dumps(xmltodict.parse(data))
        except Exception:
            _raise_error("Input Xml is not valid")
        return res
