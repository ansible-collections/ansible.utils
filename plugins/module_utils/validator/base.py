"""
The base class for validator
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from importlib import import_module
from ansible.module_utils._text import to_native


def load_validator(engine, data, criteria, plugin_vars, cls_name="Validator", **kwargs):
    """
    Load the validator from engine name
    :param engine: Name of the validator engine in format <org-name>.<collection-name>.<validator-plugin>
    :param vars: Variables for validate plugins. The variable information for each validate plugins can
                 be referred in individual plugin documentation.
    :param cls_name: Base class name for validator plugin. Defaults to ``Validator``.
    :param kwargs: The base name of the class for validator plugin
    :return:
    """
    result = {}
    if len(engine.split(".")) != 3:
        result["failed"] = True
        result["msg"] = "Parser name should be provided as a full name including collection"
        return None, result

    cref = dict(
        zip(["corg", "cname", "plugin"], engine.split("."))
    )
    validatorlib = "ansible_collections.{corg}.{cname}.plugins.validator.{plugin}".format(
        **cref
    )
    try:
        validatorcls = getattr(import_module(validatorlib), cls_name)
        validator = validatorcls(
            data=data,
            criteria=criteria,
            plugin_vars=plugin_vars,
            kwargs=kwargs
        )
        return validator,  result
    except Exception as exc:
        result["failed"] = True
        result["msg"] = "Error loading validator: {err}".format(
            err=to_native(exc)
        )
        return None, result
