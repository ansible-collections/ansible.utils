# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The action plugin file for cli_parse
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json

from ansible.module_utils._text import to_text
from ansible.module_utils.basic import missing_required_lib
from ansible.module_utils.six import string_types

from ansible_collections.ansible.utils.plugins.validator import (
    ValditorBase,
)
from ansible_collections.ansible.utils.plugins.module_utils.validator.jsonschema import (
    validate_jsonschema,
)

try:
    import jsonschema
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False
import epdb

class Validator(ValditorBase):

    @staticmethod
    def _check_reqs():
        """ Check the prerequisites are installed for jsonschema

        :return dict: A dict with a list of errors
        """
        errors = []
        if not HAS_JSONSCHEMA:
            errors.append(missing_required_lib("jsonschema"))

        return errors

    def _check_args(self):
        """ Ensure specific args are set

        :return: A dict with a list of errors
        :rtype: dict
        """
        errors = []
        try:
            data = self._task_args["data"]
            if isinstance(data, dict):
                self._task_args["data"] = json.loads(json.dumps(data))
            elif isinstance(data, string_types):
                self._task_args["data"] = json.loads(data)
            else:
                errors.append("Expected value of 'data' option is either dict or str, received type '%s'" % type(data))
        except TypeError as exe:
            errors.append("'data' option value is invalid. Failed to read with error '%s'" %
                          to_text(exe, errors="surrogate_then_replace"))

        try:
            criteria = self._task_args["criteria"]
            if isinstance(criteria, dict):
                self._task_args["criteria"] = json.loads(json.dumps(criteria))
            elif isinstance(criteria, string_types):
                self._task_args["criteria"] = json.loads(criteria)
            else:
                errors.append("Expected value of 'criteria' option is either dict or str, received type '%s'" % type(criteria))
        except TypeError as exe:
            errors.append("'criteria' option value is invalid. Failed to read with error '%s'" %
                          to_text(exe, errors="surrogate_then_replace"))

        return errors

    def validate(self, *args, **kwargs):
        """ Std entry point for a validate execution

        :return: Errors or parsed text as structured data
        :rtype: dict

        :example:

        The parse function of a parser should return a dict:
        {"errors": [a list of errors]}
        or
        {"parsed": obj}
        """
        #epdb.st()
        errors = self._check_reqs()
        errors.extend(self._check_args())
        if errors:
            return {"errors": errors}

        try:
            self._result = validate_jsonschema(
                schema=self._task_args["criteria"], data=self._task_args["data"]
            )
        except Exception as exc:
            return {"errors": to_text(exc, errors="surrogate_then_replace")}

        return self._result
