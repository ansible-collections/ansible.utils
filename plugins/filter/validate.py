from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    filter: validate
    author: Ganesh Nalawade (@ganeshrn)
    version_added: "1.0.0"
    short_description: Validate data with provided criteria
    description:
        - Validate C(data) with provided C(criteria) based on the validation C(engine).
    options:
      data:
        type: raw
        description:
        - A data that will be validated against C(criteria).
        - This option represents the value that is passed to filter plugin in pipe format.
          For example I(config_data|ansible.utils.validate()), in this case I(config_data)
          represents this option.
        - For the type of C(data) that represents this value refer documentation of individual validator plugins.
        required: True
      criteria:
        type: raw
        description:
        - The criteria used for validation of value that represents C(data) options.
        - This option represents the first argument passed in the filter plugin
          For example I(config_data|ansible.utils.validate(config_criteria)), in
          this case the value of I(config_criteria) represents this option.
        - For the type of C(criteria) that represents this value refer documentation of individual validator plugins.
        required: True
      engine:
        type: str
        description:
        - The name of the validator plugin to use.
        - This option can be passed in lookup plugin as a key, value pair
          For example I(config_data|ansible.utils.validate(config_criteria, engine='ansible.utils.jsonschema')), in
          this case the value I(ansible.utils.jsonschema) represents the engine to be use for data valdiation.
          If the value is not provided the default value that is I(ansible.uitls.jsonschema) will be used.
        - The value should be in fully qualified collection name format that is
          I(<org-name>.<collection-name>.<validator-plugin-name>).
        default: ansible.utils.jsonschema
    notes:
    - For the type of options C(data) and C(criteria) refer the individual C(validate) plugin
      documentation that is represented in the value of C(engine) option.
    - For additional plugin configuration options refer the individual C(validate) plugin
      documentation that is represented by the value of C(engine) option.
    - The plugin configuration option can be either passed as I(key=value) pairs within filter plugin
      or environment variables.
    - The precedence of the C(validate) plugin configurable option is the variable passed within filter plugin
      as I(key=value) pairs followed by the environment variables.
"""

EXAMPLES = r"""
- name: set facts for data and criteria
  set_fact:
    data: "{{ lookup('file', './validate/data/show_interfaces_iosxr.json')}}"
    criteria: "{{ lookup('file', './validate/criteria/jsonschema/show_interfaces_iosxr.json')}}"

- name: validate data in json format using jsonschema with by passing plugin configuration variable as key/value pairs
  ansible.builtin.set_fact:
    data_validilty: "{{ data|ansible.utils.validate(criteria, engine='ansible.utils.jsonschema', draft='draft7') }}"
"""

RETURN = """
  _raw:
    description:
      - If data is valid returns empty list
      - If data is invalid returns list of errors in data
"""

from copy import deepcopy

from ansible.errors import AnsibleError
from ansible.module_utils._text import to_native
from ansible_collections.ansible.utils.plugins.module_utils.validate.base import (
    load_validator,
)
from ansible_collections.ansible.utils.plugins.module_utils.common.utils import (
    to_list,
)
from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
    check_argspec,
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

ARGSPEC_CONDITIONALS = {}


def validate(*args, **kwargs):
    if len(args) < 2:
        raise AnsibleError(
            "Missing either 'data' or 'criteria' value in filter input,"
            "refer ansible.utils.validate filter plugin documentation for detials"
        )

    params = {"data": args[0], "criteria": args[1]}
    if kwargs.get("engine"):
        params.update({"engine": kwargs["engine"]})

    argspec = deepcopy(DOCUMENTATION)
    argspec_obj = yaml.load(argspec, SafeLoader)

    argspec_result, updated_params = check_argspec(
        yaml.dump(argspec_obj),
        "action",
        schema_conditionals=ARGSPEC_CONDITIONALS,
        **params
    )
    if argspec_result.get("failed"):
        raise AnsibleError(
            "%s with errors: %s"
            % (argspec_result.get("msg"), argspec_result.get("errors"))
        )

    validator_engine, validator_result = load_validator(
        engine=updated_params["engine"],
        data=updated_params["data"],
        criteria=updated_params["criteria"],
        kwargs=kwargs,
    )
    if validator_result.get("failed"):
        raise AnsibleError(
            "validate lookup plugin failed with errors: %s"
            % validator_result.get("msg")
        )

    try:
        result = validator_engine.validate()
    except Exception as exc:
        raise AnsibleError(
            "Unhandled exception from validator '{validator}'. Error: {err}".format(
                validator=updated_params["engine"], err=to_native(exc)
            )
        )

    return to_list(result.get("errors", []))


class FilterModule(object):
    """ index_of  """

    def filters(self):
        """a mapping of filter names to functions"""
        return {"validate": validate}
