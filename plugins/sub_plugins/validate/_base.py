"""
The base class for validator
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os

from importlib import import_module

from ansible.errors import AnsibleError
from ansible.module_utils.six import iteritems
from ansible.module_utils._text import to_text

from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
    check_argspec,
)

from ansible_collections.ansible.utils.plugins.module_utils.common.utils import (
    to_list,
)

try:
    import yaml

    try:
        from yaml import CSafeLoader as SafeLoader
    except ImportError:
        from yaml import SafeLoader
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


class ValidateBase(object):
    """The base class for data validators
    Provides a  _debug function to normalize debug output
    """

    def __init__(self, data, criteria, engine, plugin_vars=None, kwargs=None):
        self._data = data
        self._criteria = criteria
        self._engine = engine
        self._plugin_vars = plugin_vars if plugin_vars is not None else {}
        self._result = {}
        self._kwargs = kwargs if kwargs is not None else {}
        self._sub_plugin_options = {}

        cref = dict(zip(["corg", "cname", "plugin"], engine.split(".")))
        validatorlib = "ansible_collections.{corg}.{cname}.plugins.sub_plugins.validate.{plugin}".format(
            **cref
        )

        validatordoc = getattr(import_module(validatorlib), "DOCUMENTATION")
        if validatordoc:
            self._set_sub_plugin_options(validatordoc)

    def _set_sub_plugin_options(self, doc):
        params = {}
        try:
            argspec_obj = yaml.load(doc, SafeLoader)
        except Exception as exc:
            raise AnsibleError(
                "Error '{err}' while reading validate plugin {engine} documentation: '{argspec}'".format(
                    err=to_text(exc, errors="surrogate_or_strict"),
                    engine=self._engine,
                    argspec=doc,
                )
            )
        options = argspec_obj.get("options", {})

        if not options:
            return None

        for option_name, option_value in iteritems(options):

            option_var_name_list = option_value.get("vars", [])
            option_env_name_list = option_value.get("env", [])

            # check if plugin configuration option passed as kwargs
            # valid for lookup, filter, test plugins or pass through
            # variables if supported by the module.
            if option_name in self._kwargs:
                params[option_name] = self._kwargs[option_name]
                continue

            # check if plugin configuration option passed in task vars eg.
            #  vars:
            #  - name: ansible_validate_jsonschema_draft
            #  - name: ansible_validate_jsonschema_draft_type
            if option_var_name_list and (option_name not in params):
                for var_name_entry in to_list(option_var_name_list):
                    if not isinstance(var_name_entry, dict):
                        raise AnsibleError(
                            "invalid type '{var_name_type}' for the value of '{var_name_entry}' option,"
                            " should to be type dict".format(
                                var_name_type=type(var_name_entry),
                                var_name_entry=var_name_entry,
                            )
                        )
                    var_name = var_name_entry.get("name")
                    if var_name and var_name in self._plugin_vars:
                        params[option_name] = self._plugin_vars[var_name]
                        break

            # check if plugin configuration option as passed as enviornment  eg.
            # env:
            # - name: ANSIBLE_VALIDATE_JSONSCHEMA_DRAFT
            if option_env_name_list and (option_name not in params):
                for env_name_entry in to_list(option_env_name_list):
                    if not isinstance(env_name_entry, dict):
                        raise AnsibleError(
                            "invalid type '{env_name_entry_type}' for the value of '{env_name_entry}' option,"
                            " should to be type dict".format(
                                env_name_entry_type=type(env_name_entry),
                                env_name_entry=env_name_entry,
                            )
                        )
                    env_name = env_name_entry.get("name")
                    if env_name in os.environ:
                        params[option_name] = os.environ[env_name]
                        break

        valid, argspec_result, updated_params = check_argspec(
            yaml.dump(argspec_obj), self._engine, **params
        )
        if not valid:
            raise AnsibleError(
                "{argspec_result} with errors: {argspec_errors}".format(
                    argspec_result=argspec_result.get("msg"),
                    argspec_errors=argspec_result.get("errors"),
                )
            )

        if updated_params:
            self._sub_plugin_options = updated_params

    def _get_sub_plugin_options(self, name):
        return self._sub_plugin_options.get(name)
