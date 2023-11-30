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

from ansible.plugins.callback import CallbackBase


__metaclass__ = type


from ansible.errors import AnsibleFilterError


def _raise_error(msg):
    """Raise an error message, prepend with filter name
    :param msg: The message
    :type msg: str
    :raises: AnsibleError
    """
    error = "Error when using filter plugin 'fact_diff': {msg}".format(msg=msg)
    raise AnsibleFilterError(error)


def fact_diff(before, after, plugin):
    """Compare two facts or variables and get a diff.
    :param before: The first fact to be used in the comparison.
    :type before: raw
    :param after: The second fact to be used in the comparison.
    :type after: raw
    :param plugin: The name of the plugin in collection format
    :type plugin: string
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
    return before, after, skip_lines


def run_diff(before, after, plugin):
    skip_lines = plugin["vars"].get("skip_lines")
    _check_valid_regexes(skip_lines=skip_lines)
    before, after, skip_lines = _xform(before, after, skip_lines=skip_lines)
    diff = CallbackBase()._get_diff({"before": before, "after": after})
    ansi_escape = re.compile(r"\x1B[@-_][0-?]*[ -/]*[@-~]")
    diff_text = ansi_escape.sub("", diff)
    result = list(diff_text.splitlines())
    return result
