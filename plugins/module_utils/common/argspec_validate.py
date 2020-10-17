# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Use AnsibleModule's argspec validation

def _check_argspec(self):
    aav = AnsibleArgSpecValidator(
        data=self._task.args,
        schema=DOCUMENTATION,
        schema_format="doc",
        schema_conditionals={},
        name=self._task.action,
    )
    valid, errors = aav.validate()
    if not valid:
        raise AnsibleActionFail(errors)

"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
import re
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ansible.utils.plugins.module_utils.common.utils import (
    dict_merge,
)
from ansible.module_utils.six import iteritems, string_types
from ansible.module_utils._text import to_bytes

try:
    import yaml

    try:
        from yaml import CSafeLoader as SafeLoader
    except ImportError:
        from yaml import SafeLoader
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

try:
    from ansible.module_utils.somefile import FutureBaseArgspecValidator

    HAS_ANSIBLE_ARG_SPEC_VALIDATOR = True
except ImportError:
    HAS_ANSIBLE_ARG_SPEC_VALIDATOR = False


OPTION_METADATA = (
    "type",
    "choices",
    "default",
    "required",
    "aliases",
    "elements",
    "fallback",
    "no_log",
    "apply_defaults",
    "deprecated_aliases",
    "removed_in_version",
)
OPTION_CONDITIONALS = (
    "mutually_exclusive",
    "required_one_of",
    "required_together",
    "required_by",
    "required_if",
)

VALID_ANSIBLEMODULE_ARGS = (
    "bypass_checks",
    "no_log",
    "add_file_common_args",
    "supports_check_mode",
) + OPTION_CONDITIONALS

BASE_ARG_AVAIL = 2.11


class MonkeyModule(AnsibleModule):
    """A derivative of the AnsibleModule used
    to just validate the data (task.args) against
    the schema(argspec)
    """

    def __init__(self, data, schema, name):
        self._errors = None
        self._valid = True
        self._schema = schema
        self.name = name
        self.params = data

    def fail_json(self, msg):
        """Replace the AnsibleModule fail_json here
        :param msg: The message for the failure
        :type msg: str
        """
        if self.name:
            msg = re.sub(
                r"\(basic\.pyc?\)",
                "'{name}'".format(name=self.name),
                msg,
            )
        self._valid = False
        self._errors = msg

    def _load_params(self):
        """This replaces the AnsibleModule _load_params
        fn because we already set self.params in init
        """
        pass

    def validate(self):
        """Instantiate the super, validating the schema
        against the data
        :return valid: if the data passed
        :rtype valid: bool
        :return errors: errors reported during validation
        :rtype errors: str
        """
        super(MonkeyModule, self).__init__(**self._schema)
        return self._valid, self._errors


class AnsibleArgSpecValidator:
    def __init__(
        self, data, schema, schema_format, schema_conditionals=None, name=None
    ):
        self._errors = ""
        self._valid = True
        self._name = name
        self._schema = schema
        self._schema_format = schema_format
        self._schema_conditionals = schema_conditionals
        self._data = data

    def _extract_schema_from_doc(self, doc_obj, temp_schema):
        """Extract the schema from a doc string
        :param doc_obj: The doc as a python obj
        :type doc_obj: dictionary
        :params temp_schema: The dict in which we stuff the schema parts
        :type temp_schema: dict
        """
        options_obj = doc_obj.get("options")
        for okey, ovalue in iteritems(options_obj):
            temp_schema[okey] = {}
            for metakey in list(ovalue):
                if metakey == "suboptions":
                    temp_schema[okey].update({"options": {}})
                    suboptions_obj = {"options": ovalue["suboptions"]}
                    self._extract_schema_from_doc(
                        suboptions_obj, temp_schema[okey]["options"]
                    )
                elif metakey in OPTION_METADATA + OPTION_CONDITIONALS:
                    temp_schema[okey].update({metakey: ovalue[metakey]})

    # TODO: Support extends_documentation_fragment
    def _convert_doc_to_schema(self):
        """Convert the doc string to an obj, was yaml
        add back other valid conditionals and params
        """
        doc_obj = yaml.load(self._schema, SafeLoader)
        temp_schema = {}
        self._extract_schema_from_doc(doc_obj, temp_schema)
        self._schema = {"argument_spec": temp_schema}
        for item in doc_obj:
            if item in VALID_ANSIBLEMODULE_ARGS:
                self._schema.update({item: doc_obj[item]})

    def _validate(self):
        """Validate the data gainst the schema
        convert doc string in argspec if necessary
        """
        if self._schema_format == "doc":
            self._convert_doc_to_schema()
        if self._schema_conditionals is not None:
            self.schema = dict_merge(self._schema, self._schema_conditionals)
        mm = MonkeyModule(
            data=self._data, schema=self._schema, name=self._name
        )
        return mm.validate()

    def validate(self):
        """The public validate method
        check for future argspec validation
        that is coming in 2.11, change the check according above
        """
        if HAS_ANSIBLE_ARG_SPEC_VALIDATOR:
            return self._validate()
        else:
            return self._validate()
