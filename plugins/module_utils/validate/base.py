"""
The base class for validator
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

try:
    from importlib import import_module
except ImportError:
    pass

from ansible.module_utils._text import to_native


def load_validator(
    engine, data, criteria, plugin_vars=None, cls_name="Validate", kwargs=None
):
    """
    Load the validate plugin from engine name
    :param engine: Name of the validate engine in format <org-name>.<collection-name>.<validate-plugin>
    :param vars: Variables for validate plugins. The variable information for each validate plugins can
                 be referred in individual plugin documentation.
    :param cls_name: Base class name for validate plugin. Defaults to ``Validate``.
    :param kwargs: The base name of the class for validate plugin
    :return:
    """
    result = {}
    if plugin_vars is None:
        plugin_vars = {}

    if kwargs is None:
        kwargs = {}

    if len(engine.split(".")) != 3:
        result["failed"] = True
        result[
            "msg"
        ] = "Parser name should be provided as a full name including collection"
        return None, result

    cref = dict(zip(["corg", "cname", "plugin"], engine.split(".")))
    validatorlib = "ansible_collections.{corg}.{cname}.plugins.validate.{plugin}".format(
        **cref
    )

    try:
        validatorcls = getattr(import_module(validatorlib), cls_name)
        validator = validatorcls(
            data=data,
            criteria=criteria,
            engine=engine,
            plugin_vars=plugin_vars,
            kwargs=kwargs,
        )
        return validator, result
    except Exception as exc:
        result["failed"] = True
        result[
            "msg"
        ] = "For engine '{engine}' error loading the corresponding validate plugin: {err}".format(
            engine=engine, err=to_native(exc)
        )
        return None, result
