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
from ansible.module_utils._text import to_native
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





def _run_test(entry, test, right, tests):
    """Run a test

    :param test: The test to run
    :type test: a lambda from the qual_map
    :param entry: The x for the lambda
    :type entry: str int or bool
    :param right: The y for the lamba
    :type right: str int bool or list
    :return: If the test passed
    :rtype: book
    """
    msg = (
        "Error encountered when testing value "
        "'{entry}' (type={entry_type}) against "
        "'{right}' (type={right_type}) with '{test}'. "
    ).format(
        entry=entry,
        entry_type=type(_to_well_known_type(entry)).__name__,
        right=right,
        right_type=type(_to_well_known_type(entry)).__name__,
        test=test,
    )

    if test.startswith("!"):
        invert = True
        test = test.lstrip("!")
        if test == "=":
            test = "=="
    elif test.startswith("not "):
        invert = True
        test = test.lstrip("not ")
    else:
        invert = False

    if not isinstance(right, list) and test == "in":
        right = [right]

    j2_test = tests.get(test)
    if not j2_test:
        msg = "{msg} Error was: the test '{test}' was not found.".format(
            msg=msg, test=test
        )
        _raise_error(msg)
    else:
        try:
            if right is None:
                result = j2_test(entry)
            else:
                result = j2_test(entry, right)
        except Exception as exc:
            msg = "{msg} Error was: {error}".format(
                msg=msg, error=to_native(exc)
            )
            _raise_error(msg)

    if invert:
        result = not result
    return result


def json_to_xml(
    data,
    tests=None,
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
