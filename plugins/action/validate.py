# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The action plugin file for validate
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.errors import AnsibleActionFail
from ansible.module_utils._text import to_native, to_text, to_bytes
from ansible.plugins.action import ActionBase

from ansible_collections.ansible.utils.plugins.modules.validate import (
    DOCUMENTATION,
)
from ansible_collections.ansible.utils.plugins.module_utils.validator.base import (
    load_validator,
)
from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
    check_argspec,
)

ARGSPEC_CONDITIONALS = {}


class ActionModule(ActionBase):
    """ action module
    """

    VALIDATOR_CLS_NAME = "Validator"

    def __init__(self, *args, **kwargs):
        super(ActionModule, self).__init__(*args, **kwargs)
        self._validator_name = None
        self._result = {}

    def _debug(self, name, msg):
        """ Output text using ansible's display

        :param msg: The message
        :type msg: str
        """
        msg = "<{phost}> {name} {msg}".format(
            phost=self._playhost, name=name, msg=msg
        )
        self._display.vvvv(msg)


    def run(self, tmp=None, task_vars=None):
        """ The std execution entry pt for an action plugin

        :param tmp: no longer used
        :type tmp: none
        :param task_vars: The vars provided when the task is run
        :type task_vars: dict
        :return: The results from the parser
        :rtype: dict
        """
        argspec_result, updated_params = check_argspec(DOCUMENTATION, "action", schema_conditionals=ARGSPEC_CONDITIONALS, **self._task.args)
        if argspec_result.get("failed"):
            return self._result

        self._task_vars = task_vars
        self._playhost = task_vars.get("inventory_hostname")

        self._validator_engine, validator_result = load_validator(engine=updated_params["engine"],
                                                data=updated_params["data"],
                                                criteria=updated_params["criteria"],
                                                plugin_vars=task_vars,
                                                )
        if validator_result.get("failed"):
            return validator_result

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
