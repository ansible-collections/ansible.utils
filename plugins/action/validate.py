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
from importlib import import_module

from ansible.errors import AnsibleActionFail
from ansible.module_utils._text import to_native, to_text, to_bytes
from ansible.module_utils import basic
from ansible.module_utils.connection import (
    Connection,
    ConnectionError as AnsibleConnectionError,
)
from ansible.plugins.action import ActionBase
from ansible_collections.ansible.utils.plugins.action.base import ActionModule as ActionUtilsModule

from ansible_collections.ansible.utils.plugins.modules.validate import (
    DOCUMENTATION,
)


# python 2.7 compat for FileNotFoundError
try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError


ARGSPEC_CONDITIONALS = {}

import epdb
class ActionModule(ActionUtilsModule):
    """ action module
    """

    VALIDATOR_CLS_NAME = "Validator"

    def __init__(self, *args, **kwargs):
        super(ActionModule, self).__init__(*args, **kwargs)
        self._validator_name = None

    def _extended_check_argspec(self):
        """ Check additional requirements for the argspec
        that cannot be covered using stnd techniques
        """
        errors = []
        if len(self._task.args["engine"].split(".")) != 3:
            msg = "Parser name should be provided as a full name including collection"
            errors.append(msg)
        if errors:
            self._result["failed"] = True
            self._result["msg"] = " ".join(errors)

    def _load_validator(self, task_vars):
        """ Load a validator from the fs

        :param task_vars: The vars provided when the task was run
        :type task_vars: dict
        :return: An instance of class Validator
        :rtype: Validator
        """
        cref = dict(
            zip(["corg", "cname", "plugin"], self._task.args["engine"].split("."))
        )
        validatorlib = "ansible_collections.{corg}.{cname}.plugins.validator.{plugin}".format(
            **cref
        )
        try:
            validatorcls = getattr(import_module(validatorlib), self.VALIDATOR_CLS_NAME)
            validator = validatorcls(
                task_args=self._task.args,
                task_vars=task_vars,
                debug=self._debug,
            )
            return validator
        except Exception as exc:
            self._result["failed"] = True
            self._result["msg"] = "Error loading validator: {err}".format(
                err=to_native(exc)
            )
            return None

    def run(self, tmp=None, task_vars=None):
        """ The std execution entry pt for an action plugin

        :param tmp: no longer used
        :type tmp: none
        :param task_vars: The vars provided when the task is run
        :type task_vars: dict
        :return: The results from the parser
        :rtype: dict
        """
        self._check_argspec(DOCUMENTATION, conditionals=ARGSPEC_CONDITIONALS)
        self._extended_check_argspec()
        if self._result.get("failed"):
            return self._result

        self._task_vars = task_vars
        self._playhost = task_vars.get("inventory_hostname")

        self._validator_engine = self._load_validator(task_vars)
        if self._result.get("failed"):
            return self._result
        #epdb.st()
        try:
            result = self._validator_engine.validate()
        except Exception as exc:
            raise AnsibleActionFail(
                "Unhandled exception from validator '{validator}'. Error: {err}".format(
                    validator=self._validator_engine, err=to_native(exc)
                )
            )

        if result.get("errors"):
            self._result["errors"] = result["errors"]
            self._result.update({"failed": True})
            if "msg" in result:
                self._result["msg"] = "Validation errors were found.\n" + result["msg"]
            else:
                self._result["msg"] = "Validation errors were found."
        else:
            self._result["msg"] = "all checks passed"
        return self._result
