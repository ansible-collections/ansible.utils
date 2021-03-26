# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys
import json
from copy import deepcopy

from ansible.module_utils.common._collections_compat import Mapping
from ansible.module_utils.six import iteritems
from ansible.module_utils.basic import missing_required_lib
from ansible.module_utils.six import string_types
from ansible.module_utils._text import to_native

try:
    HAS_LXML = True
    from lxml.etree import fromstring, XMLSyntaxError
    from lxml import etree

except ImportError:
    HAS_LXML = False
    from xml.etree.ElementTree import fromstring

    if sys.version_info < (2, 7):
        from xml.parsers.expat import ExpatError as XMLSyntaxError
    else:
        from xml.etree.ElementTree import ParseError as XMLSyntaxError


try:
    import xmltodict

    HAS_XMLTODICT = True
except ImportError:
    HAS_XMLTODICT = False


def sort_list(val):
    if isinstance(val, list):
        if isinstance(val[0], dict):
            sorted_keys = [tuple(sorted(dict_.keys())) for dict_ in val]
            # All keys should be identical
            if len(set(sorted_keys)) != 1:
                raise ValueError("dictionaries do not match")

            return sorted(
                val, key=lambda d: tuple(d[k] for k in sorted_keys[0])
            )
        return sorted(val)
    return val


def dict_merge(base, other):
    """Return a new dict object that combines base and other

    This will create a new dict object that is a combination of the key/value
    pairs from base and other.  When both keys exist, the value will be
    selected from other.

    If the value in base is a list, and the value in other is a list
    the base list will be extended with the values from the other list that were
    not already present in the base list

    If the value in base is a list, and the value in other is a list
    and the two have the same entries, the value from other will be
    used, preserving the order from the other list

    If the value in base is a list, and the value in other is not a list
    the value from other will be used

    :param base: dict object to serve as base
    :param other: dict object to combine with base

    :returns: new combined dict object
    """
    if not isinstance(base, dict):
        raise AssertionError("`base` must be of type <dict>")
    if not isinstance(other, dict):
        raise AssertionError("`other` must be of type <dict>")

    combined = dict()

    for key, value in iteritems(deepcopy(base)):
        if isinstance(value, dict):
            if key in other:
                item = other.get(key)
                if item is not None:
                    if isinstance(other[key], Mapping):
                        combined[key] = dict_merge(value, other[key])
                    else:
                        combined[key] = other[key]
                else:
                    combined[key] = item
            else:
                combined[key] = value
        elif isinstance(value, list):
            if key in other:
                item = other.get(key)
                if isinstance(item, list):
                    if sort_list(value) == sort_list(item):
                        combined[key] = item
                    else:
                        value.extend([i for i in item if i not in value])
                        combined[key] = value
                else:
                    combined[key] = item
            else:
                combined[key] = value
        else:
            if key in other:
                other_value = other.get(key)
                if other_value is not None:
                    if sort_list(base[key]) != sort_list(other_value):
                        combined[key] = other_value
                    else:
                        combined[key] = value
                else:
                    combined[key] = other_value
            else:
                combined[key] = value

    for key in set(other.keys()).difference(base.keys()):
        combined[key] = other.get(key)

    return combined


def to_list(val):
    if isinstance(val, (list, tuple, set)):
        return list(val)
    elif val is not None:
        return [val]
    else:
        return list()


def validate_data(data, fmt=None):
    """
    This function validates the data for given format (fmt).
    If the fmt is None it tires to guess the data format.
    Currently support data format checks are
    1) xml
    2) json
    :param data: The data which should be validated and normalised.
    :param fmt: This is an optional argument which indicated the format
    of the data. Valid values are "xml" and "json". If the value
    is None the format of the data will be guessed and returned in the output.
    :return:
        *  If the format identified is XML it returns the data format type
           which is "xml" in this case.

        *  If the format identified is JSON it returns data format type
           which is "json" in this case.

    """
    if data is None:
        return None, None

    if isinstance(data, string_types):
        data = data.strip()
        if (data.startswith("<") and data.endswith(">")) or fmt == "xml":
            try:
                result = fromstring(data)
                if fmt and fmt != "xml":
                    raise Exception(
                        "Invalid format '%s'. Expected format is 'xml' for data '%s'"
                        % (fmt, data)
                    )
                return "xml"
            except XMLSyntaxError as exc:
                if fmt == "xml":
                    raise Exception(
                        "'%s' XML validation failed with error '%s'"
                        % (
                            data,
                            to_native(exc, errors="surrogate_then_replace"),
                        )
                    )
                pass
            except Exception as exc:
                error = "'%s' recognized as XML but was not valid." % data
                raise Exception(
                    error + to_native(exc, errors="surrogate_then_replace")
                )
        elif (data.startswith("{") and data.endswith("}")) or fmt == "json":
            try:
                if fmt and fmt != "json":
                    raise Exception(
                        "Invalid format '%s'. Expected format is 'json' for data '%s'"
                        % (fmt, data)
                    )
                return "json"
            except (
                TypeError,
                getattr(json.decoder, "JSONDecodeError", ValueError),
            ) as exc:
                if fmt == "json":
                    raise Exception(
                        "'%s' JSON validation failed with error '%s'"
                        % (
                            data,
                            to_native(exc, errors="surrogate_then_replace"),
                        )
                    )
            except Exception as exc:
                error = "'%s' recognized as JSON but was not valid." % data
                raise Exception(
                    error + to_native(exc, errors="surrogate_then_replace")
                )
    elif isinstance(data, dict):
        if fmt and fmt != "json":
            raise Exception(
                "Invalid format '%s'. Expected format is 'json' for data '%s'"
                % (fmt, data)
            )

        try:
            result = json.loads(json.dumps(data))
            return "json"
        except (
            TypeError,
            getattr(json.decoder, "JSONDecodeError", ValueError),
        ) as exc:
            raise Exception(
                "'%s' JSON validation failed with error '%s'"
                % (data, to_native(exc, errors="surrogate_then_replace"))
            )
        except Exception as exc:
            error = "'%s' recognized as JSON but was not valid." % data
            raise Exception(
                error + to_native(exc, errors="surrogate_then_replace")
            )
