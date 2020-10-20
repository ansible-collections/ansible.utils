# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


"""
The get_path lookup plugin
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
    lookup: validate
    author: Ganesh Nalawade (@ganeshrn)
    version_added: "1.0.0"
    short_description: Validate data with provided criteria 
    description:
        - Validate C(data) with provided C(criteria) based on the validation C(engine).
    options:
      _terms:
        description: 
        - The values below provided in the order C(data), C(criteria) and key, value pairs
          as optional arguments.
        required: True
      data:
        type: raw
        description:
        - A data that will be validated against C(criteria). 
          For the type of data refer documentation of individual validator plugins
        required: True
      criteria:
        type: raw
        description:
        - The criteria used for validation of C(data). For the type of criteria refer
          documentation of individual validator plugins.
        required: True
      engine:
        type: str
        description:
        - The name of the validator plugin to use.
        - This option can be passed in lookup plugin as a key, value pair
          For example I(lookup('ansible.utils.validate', data, criteria, engine='ansible.utils.jsonschema')), in
          this case the value I(ansible.utils.jsonschema) represents the engine to be use for data valdiation.
          If the value is not provided the default value that is I(ansible.uitls.jsonschema) will be used.
        - The value should be in fully qualified collection name format that is 
          I(<org-name>.<collection-name>.<validator-plugin-name>).
        default: ansible.utils.jsonschema
    notes:
"""

EXAMPLES = r"""
- name: set facts for data and criteria
  set_fact:
    data: "{{ lookup('file', './validate/data/show_interfaces_iosxr.json')}}"
    criteria: "{{ lookup('file', './validate/criteria/jsonschema/show_interfaces_iosxr.json')}}"
 
- name: validate data in json format using jsonschema with lookup plugin
  ansible.builtin.set_fact:
    data_criteria_checks: "{{ lookup('ansible.utils.validate', data, criteria, engine='ansible.utils.jsonschema', draft='draft7') }}"
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
from ansible.plugins.lookup import LookupBase
from ansible_collections.ansible.utils.plugins.module_utils.validator.base import (
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


class LookupModule(LookupBase):
    def run(self, terms, variables, **kwargs):
        if len(terms) < 2:
            raise AnsibleError("Missing either 'data' or 'criteria' value in lookup input,"
                               "refer ansible.utils.validate lookup plugin documentation for detials")

        params = {
            "data": terms[0],
            "criteria": terms[1],
        }
        if kwargs.get("engine"):
            params.update({"engine": kwargs["engine"]})

        argspec = deepcopy(DOCUMENTATION)
        argspec_obj = yaml.load(argspec, SafeLoader)
        argspec_obj["options"].pop("_terms", None)

        argspec_result, updated_params = check_argspec(yaml.dump(argspec_obj), "lookup", schema_conditionals=ARGSPEC_CONDITIONALS, **params)
        if argspec_result.get("failed"):
            raise AnsibleError('%s with errors: %s' % (argspec_result.get("msg"), argspec_result.get("errors")))

        validator_engine, validator_result = load_validator(engine=updated_params["engine"],
                                                data=updated_params["data"],
                                                criteria=updated_params["criteria"],
                                                plugin_vars=variables,
                                                kwargs=kwargs,
                                                )
        if validator_result.get("failed"):
            raise AnsibleError('validate lookup plugin failed with errors: %s' % validator_result.get("msg"))

        try:
            result = validator_engine.validate()
        except Exception as exc:
            raise AnsibleError(
                "Unhandled exception from validator '{validator}'. Error: {err}".format(
                    validator=updated_params["engine"], err=to_native(exc)
                )
            )

        return to_list(result.get("errors", []))
