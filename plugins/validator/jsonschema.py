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

from ansible_collections.ansible.utils.plugins.module_utils.common.utils import (
    to_list,
)

try:
    from jsonschema import Draft7Validator
    from jsonschema.exceptions import ValidationError

    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False

import epdb


def to_path(fpath):
    return ".".join(str(index) for index in fpath)


def json_path(absolute_path):
    path = '$'
    for elem in absolute_path:
        if isinstance(elem, int):
            path += '[' + str(elem) + ']'
        else:
            path += '.' + elem
    return path


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
            if isinstance(self._data, dict):
                self._data = json.loads(json.dumps(self._data))
            elif isinstance(self._data, string_types):
                self._data = json.loads(self._data)
            else:
                errors.append("Expected value of 'data' option is either dict or str, received type '%s'" % type(self._data))
        except TypeError as exe:
            errors.append("'data' option value is invalid. Failed to read with error '%s'" %
                          to_text(exe, errors="surrogate_then_replace"))

        try:
            criteria = []
            for item in to_list(self._criteria):
                if isinstance(item, dict):
                    criteria.append(json.loads(json.dumps(self._criteria)))
                elif isinstance(self._criteria, string_types):
                    criteria.append(json.loads(self._criteria))
                else:
                    errors.append("Expected value of 'criteria' option is either list of dict/str or dict or str, received type '%s'" % type(criteria))
            self._criteria = criteria
        except TypeError as exe:
            errors.append("'criteria' option value is invalid. Failed to read with error '%s'" %
                          to_text(exe, errors="surrogate_then_replace"))

        return errors

    def validate(self):
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
            self._validate_jsonschema()
        except Exception as exc:
            return {"errors": to_text(exc, errors="surrogate_then_replace")}

        return self._result

    def _validate_jsonschema(self):
        error_messages = None
        #epdb.st()
        for criteria in self._criteria:
            validator = Draft7Validator(criteria)
            validation_errors = sorted(
                validator.iter_errors(self._data), key=lambda e: e.path
            )

            if validation_errors:
                if "errors" not in self._result:
                    self._result["errors"] = []

                error_messages = []
                for validation_error in validation_errors:
                    if isinstance(validation_error, ValidationError):
                        error = {
                            "message": validation_error.message,
                            "data_path": to_path(
                                validation_error.absolute_path
                            ),
                            "json_path": json_path(validation_error.absolute_path),
                            "schema_path": to_path(
                                validation_error.relative_schema_path
                            ),
                            "relative_schema": validation_error.schema,
                            "expected": validation_error.validator_value,
                            "validator": validation_error.validator,
                            "found": validation_error.instance,
                        }
                        self._result["errors"].append(error)
                        error_message = "At '{schema_path}' {message}. ".format(
                            schema_path=error["schema_path"], message=error["message"]
                        )
                        error_messages.append(error_message)
        if error_messages:
            if "msg" not in self._result:
                self._result["msg"] = "\n".join(error_messages)
