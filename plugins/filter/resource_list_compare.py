from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: resource_list_compare
    author: Rohit Thakur (@rohitthakur2590)
    version_added: "2.4.0"
    short_description: Generate the final resource list combining/comparing base and provided resources
    description:
        - Generate the final list of resources after comparing with base list and provide list of resources/bangs.
    options:
      base:
        description: Specify the base list of supported network resources.
        type: list
        elements: str
      target:
        description: Specify the target list of resources.
        type: list
        elements: str
"""

EXAMPLES = r"""
- name: set facts for data and criteria
  set_fact:
    network_resources: "{{ network_resources_list['modules']|resource_list_compare(resources) }}"
"""

RETURN = """
  list:
    combined=['interfaces', 'l2_interfaces', 'l3_interfaces']
"""

from ansible.errors import AnsibleError, AnsibleFilterError
from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
    check_argspec,
)

ARGSPEC_CONDITIONALS = {}


def resource_list_compare(*args, **kwargs):
    if len(args) < 2:
        raise AnsibleFilterError(
            "Missing either 'base' or 'other value in filter input,"
            " refer 'ansible.network.resource_manager.resource_list_compare' filter plugin documentation for details"
        )

    params = {"base": args[0], "target": args[1]}

    valid, argspec_result, updated_params = check_argspec(
        DOCUMENTATION,
        "resource_list_compare filter",
        schema_conditionals=ARGSPEC_CONDITIONALS,
        **params
    )
    if not valid:
        raise AnsibleFilterError(
            "{argspec_result} with errors: {argspec_errors}".format(
                argspec_result=argspec_result.get("msg"),
                argspec_errors=argspec_result.get("errors"),
            )
        )
    base = params["base"]
    other = params["target"]
    if not isinstance(base, list):
        raise AssertionError("`base` must be of type 'list'")
    if not isinstance(other, list):
        raise AssertionError("`other` must be of type 'list'")

    combined = []
    alls = [x for x in other if x == "all"]
    bangs = [x[1:] for x in other if x.startswith("!")]
    rbangs = [x for x in other if x.startswith("!")]
    remain = [
        x for x in other if x not in alls and x not in rbangs and x in base
    ]
    unsupported = [
        x for x in other if x not in alls and x not in rbangs and x not in base
    ]

    if unsupported:
        raise AnsibleFilterError(
            "The following are unsupported: %s" % (",".join(unsupported))
        )

    if alls:
        combined = base
    for entry in bangs:
        if entry in combined:
            combined.remove(entry)
    for entry in remain:
        if entry not in combined:
            combined.append(entry)
    combined.sort()
    output = {"actionable": combined, "unsupported": unsupported}
    return output


class FilterModule(object):
    """ resource_list_compare  """

    def filters(self):
        """a mapping of filter names to functions"""
        return {"resource_list_compare": resource_list_compare}
