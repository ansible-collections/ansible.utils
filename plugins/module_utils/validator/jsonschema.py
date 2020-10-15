"""
The base class for validator
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

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


def validate_jsonschema(schema, data):
    result = {}
    validator = Draft7Validator(schema)
    #epdb.st()
    validation_errors = sorted(
        validator.iter_errors(data), key=lambda e: e.path
    )

    if validation_errors:
        result["errors"] = []
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
                result["errors"].append(error)
                error_message = "At '{schema_path}' {message}. ".format(
                    schema_path=error["schema_path"], message=error["message"]
                )
                error_messages.append(error_message)
        if error_messages:
            result["msg"] = "\n".join(error_messages)

    return result
