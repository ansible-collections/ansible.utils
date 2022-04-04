#
# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

"""
The keep_keys plugin code
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.errors import AnsibleFilterError
import itertools


def _raise_error(filter, msg):
    """Raise an error message, prepend with filter name
    :param msg: The message
    :type msg: str
    :raises: AnsibleError
    """
    error = f"Error when using plugin 'consolidate': '{filter}' reported {msg}"
    raise AnsibleFilterError(error)


def fail_on_filter(validator_func):
    def update_err(*args, **kwargs):

        res, err = validator_func(*args, **kwargs)
        if err.get("match_key_err"):
            _raise_error("fail_missing_match_key", ", ".join(err["match_key_err"]))
        if err.get("match_val_err"):
            _raise_error("fail_missing_match_value", ", ".join(err["match_val_err"]))
        if err.get("duplicate_err"):
            _raise_error("fail_duplicate", ", ".join(err["duplicate_err"]))
        return res

    return update_err


@fail_on_filter
def check_missing_match_key_duplicate(
    data_sources, fail_missing_match_key, fail_duplicate
):
    """Validate the operation
    :param operation: The operation
    :type operation: str
    :raises: AnsibleFilterError
    """
    results, errors_match_key, errors_duplicate = [], [], []
    # Check for missing and duplicate match key
    for ds_idx, data_source in enumerate(data_sources):
        match_key = data_source["match_key"]
        ds_values = []

        for dd_idx, data_dict in enumerate(data_source["data"]):
            try:
                ds_values.append(data_dict[match_key])
            except KeyError:
                if fail_missing_match_key:
                    errors_match_key.append(
                        f"Missing match key '{match_key}' in data source {ds_idx} in list entry {dd_idx}"
                    )
                continue

        if sorted(set(ds_values)) != sorted(ds_values) and fail_duplicate:
            errors_duplicate.append(f"Duplicate values in data source {ds_idx}")
        results.append(set(ds_values))
    return results, {
        "match_key_err": errors_match_key,
        "duplicate_err": errors_duplicate,
    }


@fail_on_filter
def check_missing_match_values(results, fail_missing_match_value):
    errors_match_values = []
    all_values = set(itertools.chain.from_iterable(results))
    if fail_missing_match_value:
        for ds_idx, ds_values in enumerate(results):
            missing_match = all_values - ds_values
            if missing_match:
                errors_match_values.append(
                    f"Missing match value {', '.join(missing_match)} in data source {ds_idx}"
                )
    return all_values, {"match_val_err": errors_match_values}


def consolidate_facts(data_sources, all_values):
    consolidated_facts = {}
    for data_source in data_sources:
        match_key = data_source["match_key"]
        source = data_source["prefix"]
        data_dict = {d[match_key]: d for d in data_source["data"] if match_key in d}
        for value in sorted(all_values):
            if value not in consolidated_facts:
                consolidated_facts[value] = {}
            consolidated_facts[value][source] = data_dict.get(value, {})
    return consolidated_facts


def consolidate(
    data_source,
    fail_missing_match_key=False,
    fail_missing_match_value=False,
    fail_duplicate=False,
):
    """keep selective keys recursively from a given data"
    :param data: The data passed in (data|keep_keys(...))
    :type data: raw
    :param target: List of keys on with operation is to be performed
    :type data: list
    :type elements: string
    :param matching_parameter: matching type of the target keys with data keys
    :type data: str
    """
    # write code here
    key_sets = check_missing_match_key_duplicate(
        data_source, fail_missing_match_key, fail_duplicate
    )
    key_vals = check_missing_match_values(key_sets, fail_missing_match_value)
    datapr = consolidate_facts(data_source, key_vals)
    return datapr
