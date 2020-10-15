"""
The base class for validator
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.utils.display import Display


class ValditorBase(object):
    """ The base class for data validators
    Provides a  _debug function to normalize debug output
    """

    def __init__(self, args, vars, debug=None):
        self._debug = debug
        self._args = args
        self._vars = vars

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