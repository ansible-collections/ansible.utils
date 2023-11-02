#
# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

"""
The fact_diff plugin code
"""
from __future__ import absolute_import, division, print_function

import re

from importlib import import_module

from ansible.module_utils._text import to_native
from ansible.plugins.callback import CallbackBase


__metaclass__ = type


from ansible.errors import AnsibleFilterError


def _raise_error(msg):
    """Raise an error message, prepend with filter name
    :param msg: The message
    :type msg: str
    :raises: AnsibleError
    """
    error = "Error when using plugin 'from_xml': {msg}".format(msg=msg)
    raise AnsibleFilterError(error)


def fact_diff(before, after, plugin):
    """Convert data which is in xml to json"
    :param data: The data passed in (data|from_xml(...))
    :type data: xml
    :param engine: Conversion library default=xml_to_dict
    """
    result = run_diff(before, after, plugin)
    return result


def _check_valid_regexes(skip_lines):
    if skip_lines:
        for idx, regex in enumerate(skip_lines):
            try:
                skip_lines[idx] = re.compile(regex)
            except re.error as exc:
                msg = "The regex '{regex}', is not valid. The error was {err}.".format(
                    regex=regex,
                    err=str(exc),
                )
                _raise_error(msg)


def _xform(before, after, skip_lines):
    if skip_lines:
        if isinstance(before, str):
            before = before.splitlines()
        if isinstance(after, str):
            after = after.splitlines()
        before = [
            line for line in before if not any(regex.match(str(line)) for regex in skip_lines)
        ]
        after = [line for line in after if not any(regex.match(str(line)) for regex in skip_lines)]
    if isinstance(before, list):
        before = "\n".join(map(str, before)) + "\n"
    if isinstance(after, list):
        after = "\n".join(map(str, after)) + "\n"


def run_diff(before, after, plugin):
    skip_lines = plugin["vars"].get("skip_lines")
    _check_valid_regexes(skip_lines=skip_lines)
    _xform(before, after, skip_lines=skip_lines)
    diff = CallbackBase()._get_diff({"before": before, "after": after})
    ansi_escape = re.compile(r"\x1B[@-_][0-?]*[ -/]*[@-~]")
    diff_text = ansi_escape.sub("", diff)
    result = list(diff_text.splitlines())
    return result
